import json
from typing import Any
from uuid import UUID

import httpx

from app.config import settings
from app.modules.ai.exceptions import AiConfigError, AiProviderError, WeatherProviderError
from app.modules.ai.schemas import RoutePointDTO, TripAssistantRequestDTO, TripAssistantResponseDTO
from app.modules.trips.exceptions import TripNotFoundError
from app.modules.trips.repository import TripRepo
from app.modules.trips.utils.crypto import decrypt_address


WEATHER_CODE_DESCRIPTIONS: dict[int, str] = {
    0: "clear",
    1: "mostly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "foggy",
    51: "light drizzle",
    53: "drizzle",
    55: "heavy drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    80: "rain showers",
    81: "rain showers",
    82: "heavy rain showers",
    95: "thunderstorm",
}


class AiAssistantService:
    def __init__(self, trip_repo: TripRepo):
        self.trip_repo = trip_repo

    async def get_route_weather(
        self,
        current_location: RoutePointDTO | None,
        destination_location: RoutePointDTO | None,
    ) -> str | None:
        points: list[tuple[str, RoutePointDTO]] = []
        if current_location:
            points.append(("Current location", current_location))
        if destination_location:
            points.append(("Destination", destination_location))

        if not points:
            return None

        parts: list[str] = []
        for label, point in points:
            parts.append(await self._fetch_weather_point(label, point))
        return " | ".join(parts)

    async def ask_trip_assistant(self, user_id: UUID, payload: TripAssistantRequestDTO) -> TripAssistantResponseDTO:
        trip_context = await self._load_trip_context(user_id, payload.trip_id) if payload.trip_id else {}
        weather_summary = await self.get_route_weather(payload.current_location, payload.destination_location)
        missing_details = self._infer_missing_details(trip_context)

        if not settings.AI_AGENT_ENABLED:
            return self._fallback_response(payload.message, weather_summary, missing_details)

        if not settings.OPENAI_API_KEY:
            raise AiConfigError("OPENAI_API_KEY must be set when AI_AGENT_ENABLED=true")

        ai_result = await self._call_openai(payload, trip_context, weather_summary, missing_details)
        return TripAssistantResponseDTO(
            assistant_message=ai_result.get("assistant_message", "I could not generate a response."),
            suggested_category=ai_result.get("suggested_category"),
            missing_details=ai_result.get("missing_details") or missing_details,
            weather_summary=weather_summary,
            ai_enabled=True,
        )

    async def _load_trip_context(self, user_id: UUID, trip_id: UUID) -> dict[str, Any]:
        trip = await self.trip_repo.get(trip_id, user_id)
        if not trip:
            raise TripNotFoundError("Trip not found or not owned by user")

        return {
            "id": str(trip.id),
            "status": str(trip.status),
            "start_address": decrypt_address(trip.start_address_encrypted) if trip.start_address_encrypted else None,
            "end_address": decrypt_address(trip.end_address_encrypted) if trip.end_address_encrypted else None,
            "purpose": trip.purpose,
            "miles": trip.miles,
            "scheduled_start_at": trip.scheduled_start_at.isoformat() if trip.scheduled_start_at else None,
            "scheduled_end_at": trip.scheduled_end_at.isoformat() if trip.scheduled_end_at else None,
            "rate_category_id": str(trip.rate_category_id),
        }

    async def _fetch_weather_point(self, label: str, point: RoutePointDTO) -> str:
        params = {
            "latitude": point.lat,
            "longitude": point.lon,
            "current": "temperature_2m,weather_code,wind_speed_10m,precipitation",
        }

        try:
            async with httpx.AsyncClient(timeout=settings.WEATHER_TIMEOUT_SECONDS) as client:
                response = await client.get(settings.WEATHER_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise WeatherProviderError("Failed to fetch weather data") from exc

        current = data.get("current") or {}
        weather_code = current.get("weather_code")
        description = WEATHER_CODE_DESCRIPTIONS.get(weather_code, "unknown")
        temp = current.get("temperature_2m")
        wind = current.get("wind_speed_10m")
        precip = current.get("precipitation")
        return f"{label}: {description}, {temp}C, wind {wind} km/h, precip {precip} mm"

    def _infer_missing_details(self, trip_context: dict[str, Any]) -> list[str]:
        if not trip_context:
            return []

        missing: list[str] = []
        if not trip_context.get("start_address"):
            missing.append("start_address")
        if not trip_context.get("end_address"):
            missing.append("end_address")
        if not trip_context.get("purpose"):
            missing.append("purpose")
        if trip_context.get("status") == "scheduled" and not trip_context.get("scheduled_end_at"):
            missing.append("scheduled_end_at")
        return missing

    def _fallback_response(
        self,
        message: str,
        weather_summary: str | None,
        missing_details: list[str],
    ) -> TripAssistantResponseDTO:
        suggested_category = self._simple_category_suggestion(message)
        prompt = "AI assistant is disabled. "
        if missing_details:
            prompt += f"Please provide: {', '.join(missing_details)}."
        else:
            prompt += "All key trip fields look present."
        return TripAssistantResponseDTO(
            assistant_message=prompt,
            suggested_category=suggested_category,
            missing_details=missing_details,
            weather_summary=weather_summary,
            ai_enabled=False,
        )

    def _simple_category_suggestion(self, text: str) -> str | None:
        lower = text.lower()
        if any(keyword in lower for keyword in ["client", "meeting", "office", "work"]):
            return "Business"
        if any(keyword in lower for keyword in ["medical", "hospital", "doctor"]):
            return "Medical"
        if any(keyword in lower for keyword in ["charity", "volunteer"]):
            return "Charity"
        return None

    async def _call_openai(
        self,
        payload: TripAssistantRequestDTO,
        trip_context: dict[str, Any],
        weather_summary: str | None,
        missing_details: list[str],
    ) -> dict[str, Any]:
        url = f"{settings.OPENAI_BASE_URL.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        system_prompt = (
            "You are a trip assistant. Return JSON only with keys: "
            "assistant_message (string), suggested_category (string or null), "
            "missing_details (array of strings). "
            "If required trip details are missing, ask concise follow-up questions. "
            "If possible, suggest one trip category."
        )

        user_payload = {
            "message": payload.message,
            "trip_context": trip_context,
            "weather_summary": weather_summary,
            "known_missing_details": missing_details,
            "metadata": payload.metadata,
        }

        body = {
            "model": settings.OPENAI_MODEL,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_payload)},
            ],
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise AiProviderError("Failed to call AI provider") from exc

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        try:
            parsed = self._parse_json_content(content)
        except ValueError as exc:
            raise AiProviderError("AI provider returned malformed JSON") from exc
        if not isinstance(parsed, dict):
            raise AiProviderError("AI provider response was not valid JSON")
        return parsed

    def _parse_json_content(self, content: str) -> dict[str, Any]:
        raw = content.strip()
        if raw.startswith("```"):
            lines = raw.splitlines()
            if len(lines) >= 3:
                raw = "\n".join(lines[1:-1]).strip()
        return json.loads(raw)
