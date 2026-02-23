# Common Places

**Owner:** Daiduong Dinh

## Overview

This feature allows users to save, retrieve, update, and delete frequently visited locations ("common places") such as Home, Work, Gym, etc. Each common place stores a name and an address, enabling quick selection during trip creation rather than re-entering addresses manually.

Key behaviors:

- Full CRUD lifecycle: create, read (single + list), update, delete
- Maximum of **4** common places per user
- Unique name enforcement per user (no duplicate names)
- Addresses are **always encrypted at rest** using Fernet symmetric encryption (NF2)
- All operations are scoped to the authenticated user (ownership enforced)

## Requirements Covered

### Functional

- **R3 – Prompting for Trip Details**
  - Common places allow users to quickly select saved start/end addresses when creating trips
  - Reduces manual data entry for routine trips

### Non-Functional

- **NF2:** Addresses must never be stored in plaintext — all addresses are encrypted via `encrypt_address()` before persistence and decrypted via `decrypt_address()` on retrieval

## Architecture & Design

### Layered Architecture

The feature follows the same layered pattern used throughout the backend:

```
Router → Service → Repository → Database
```

| Layer        | File                                         | Responsibility                                            |
|------------- |----------------------------------------------|-----------------------------------------------------------|
| **Router**   | `modules/common_places/router.py`            | HTTP endpoints, request/response handling, auth injection  |
| **Service**  | `modules/common_places/service.py`           | Business logic, validation, encryption, duplicate checks   |
| **Repository** | `modules/common_places/repository.py`      | Database queries via async SQLAlchemy                      |
| **Schemas**  | `modules/common_places/schemas.py`           | Pydantic DTOs for create, update, and response             |
| **Models**   | `modules/common_places/models.py`            | SQLAlchemy ORM model (`common_places` table)               |
| **Exceptions** | `modules/common_places/exceptions.py`      | Domain-specific error types                                |

### Data Model

**Table:** `common_places`

| Column       | Type              | Constraints                                                                 |
|------------- |-------------------|-----------------------------------------------------------------------------|
| `id`         | `UUID`            | Primary key, auto-generated                                                 |
| `user_id`    | `UUID`            | Foreign key → `users.id`, `ON DELETE CASCADE`, indexed                      |
| `name`       | `String(255)`     | Not null; unique per user (`uq_common_places_customization_name` constraint)|
| `address`    | `String(512)`     | Not null; stored as Fernet-encrypted ciphertext                             |
| `created_at` | `DateTime(tz)`    | Server default `now()`                                                      |
| `updated_at` | `DateTime(tz)`    | Server default `now()`, auto-updated on changes                             |

**Relationships:**

- `CommonPlace.user` → `User` (many-to-one, back-populated as `user.common_places`)

### Address Encryption

All addresses flow through the shared Fernet crypto utilities in `app/modules/trips/utils/crypto.py`:

- `encrypt_address(address)` — called **before** saving to the database (in `create` and `update`)
- `decrypt_address(token)` — called **when building responses** (in `CommonPlaceResponse.model_validate`)

This ensures addresses are **never stored in plaintext** (NF2 compliance).

---

## Endpoints

### POST `/common-places/`

Create a new common place.

**Request Body** (`CommonPlaceCreate`)

```json
{
  "name": "Home",
  "address": "123 Main St"
}
```

**Field Requirements**

| Field     | Required | Rules                    |
|-----------|----------|--------------------------|
| `name`    | Yes      | Cannot be empty/blank    |
| `address` | Yes      | Cannot be empty/blank    |

**Behavior**

1. Validates name and address are non-empty (after stripping whitespace)
2. Checks the user has fewer than 4 existing common places
3. Checks no existing common place has the same name for this user
4. Encrypts the address
5. Saves and returns the new common place

**Example Success Response**

```
200 OK
```

```json
{
  "user_id": "user-uuid",
  "id": "place-uuid",
  "name": "Home",
  "address": "123 Main St",
  "created_at": "2025-11-30T12:00:00Z",
  "updated_at": "2025-11-30T12:00:00Z"
}
```

**Errors**

| Status | Condition                               |
|--------|-----------------------------------------|
| `400`  | Name is required (empty/blank)          |
| `400`  | Address is required (empty/blank)       |
| `400`  | Maximum of 4 common places allowed      |
| `409`  | A common place with this name already exists |
| `500`  | Unexpected persistence error            |

---

### GET `/common-places/`

Returns all common places for the authenticated user.

**Success Response**

```
200 OK
```

```json
[
  {
    "user_id": "user-uuid",
    "id": "place-uuid-1",
    "name": "Home",
    "address": "123 Main St",
    "created_at": "...",
    "updated_at": "..."
  },
  {
    "user_id": "user-uuid",
    "id": "place-uuid-2",
    "name": "Work",
    "address": "456 Office Blvd",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

Returns an empty array `[]` if the user has no common places.

---

### GET `/common-places/{place_id}`

Retrieve a single common place by ID.

**Path Parameter**

| Parameter  | Type | Required | Notes                    |
|------------|------|----------|--------------------------|
| `place_id` | UUID | Yes      | Must belong to the user  |

**Success Response**

```
200 OK
```

```json
{
  "user_id": "user-uuid",
  "id": "place-uuid",
  "name": "Home",
  "address": "123 Main St",
  "created_at": "...",
  "updated_at": "..."
}
```

**Errors**

| Status | Condition                                   |
|--------|---------------------------------------------|
| `404`  | Common place not found or not owned by user |

---

### PATCH `/common-places/{place_id}`

Update an existing common place. Supports partial updates.

**Path Parameter**

| Parameter  | Type | Required | Notes                    |
|------------|------|----------|--------------------------|
| `place_id` | UUID | Yes      | Must belong to the user  |

**Request Body** (`CommonPlaceUpdate`)

All fields are optional — only send what you want to change:

```json
{
  "name": "Updated Name"
}
```

```json
{
  "address": "789 New Address"
}
```

```json
{
  "name": "Updated Name",
  "address": "789 New Address"
}
```

**Field Requirements**

| Field     | Rules                                     |
|-----------|-------------------------------------------|
| `name`    | Optional; cannot be empty/blank if provided |
| `address` | Optional; cannot be empty/blank if provided |

**Behavior**

1. Fetches the existing common place (must exist and belong to user)
2. If `name` is provided and differs from the current name, checks for duplicates
3. If `address` is provided, encrypts the new address
4. Commits and returns the updated common place

**Errors**

| Status | Condition                                        |
|--------|--------------------------------------------------|
| `400`  | Name cannot be empty                             |
| `400`  | Address cannot be empty                          |
| `404`  | Common place not found or not owned by user      |
| `409`  | A common place with this name already exists     |
| `500`  | Unexpected persistence error                     |

---

### DELETE `/common-places/{place_id}`

Delete a common place.

**Path Parameter**

| Parameter  | Type | Required | Notes                    |
|------------|------|----------|--------------------------|
| `place_id` | UUID | Yes      | Must belong to the user  |

**Success Response**

```
204 No Content
```

**Errors**

| Status | Condition                                   |
|--------|---------------------------------------------|
| `404`  | Common place not found or not owned by user |

---

## Error Handling

All endpoint exceptions are caught by the centralized `error_handler` decorator and mapped to HTTP status codes:

| Exception                      | HTTP Status | When Raised                            |
|-------------------------------|-------------|----------------------------------------|
| `InvalidCommonPlaceDataError` | `400`       | Empty name or address                  |
| `MaxCommonPlacesError`        | `400`       | User already has 4 common places       |
| `DuplicateCommonPlaceError`   | `409`       | Name already taken for this user       |
| `CommonPlaceNotFoundError`    | `404`       | Place doesn't exist or wrong owner     |
| `CommonPlacePersistenceError` | `500`       | Unexpected database error              |

---

## Permissions & Privacy

- **Authentication required** — all endpoints use `get_current_user` dependency
- **User ownership enforced** — every query filters by `user_id == current_user.id`
- **Address encryption** — addresses are encrypted via Fernet before storage and decrypted only in API responses (NF2)

---

## Testing

Testing has been completed across all four layers with comprehensive unit tests:

### Unit Tests — What's Covered

| Test File              | Tests | Coverage                                                           |
|------------------------|-------|--------------------------------------------------------------------|
| `test_service.py`      | 11    | Create (success, max limit, duplicate name, integrity error), get all, get one (success, not found), update (success, duplicate name, not found), delete (success, not found) |
| `test_router.py`       | 11    | All 5 endpoints tested for success and error cases; verifies HTTP status codes, service delegation, and response schema validation |
| `test_repository.py`   | 8     | Create, get by ID (found/not found), get all (found/empty), get by name (found/not found), update, delete |
| `test_schemas.py`      | 6     | Create (valid, missing fields), Update (all/partial/empty), Response (valid, model_validate with decryption mock, missing fields) |

All tests mock the encryption layer to isolate business logic from cryptography concerns.

---

## Known Issues / Notes

- The `name` uniqueness constraint (`uq_common_places_customization_name`) uses a legacy naming convention referencing "customization" — this does not affect behavior but may be confusing when inspecting the database schema directly.
- The maximum of 4 common places is enforced **at the service layer** (not as a database constraint), so it could theoretically be bypassed if the service is not used.
