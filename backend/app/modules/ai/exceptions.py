class AiAssistantError(Exception):
    """Base class for AI assistant errors."""


class AiConfigError(AiAssistantError):
    """Raised when AI settings are missing or invalid."""


class AiProviderError(AiAssistantError):
    """Raised when the LLM provider request fails."""


class WeatherProviderError(AiAssistantError):
    """Raised when weather provider request fails."""

