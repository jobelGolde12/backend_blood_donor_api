# User & Preference Module (TODO 3)

## Overview
User profile management with theme preferences and validation.

## Endpoints

### GET /api/v1/users/me
Get current user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "full_name": "Juan Dela Cruz",
  "contact_number": "09123456789",
  "email": "juan@example.com",
  "role": "donor",
  "status": "active",
  "theme_preference": "system",
  "created_at": "2026-02-06T10:00:00Z",
  "updated_at": "2026-02-06T10:30:00Z"
}
```

### PUT /api/v1/users/me
Update current user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "full_name": "Juan P. Dela Cruz",
  "contact_number": "09987654321",
  "email": "juan.new@example.com"
}
```

**Response:** Same as GET /users/me

**Validation:**
- Contact number must be valid PH format (09XXXXXXXXX or +639XXXXXXXXX)
- Contact number must be unique
- Email must be unique
- Only owner can update their profile

### PUT /api/v1/users/me/preferences
Update user theme preferences.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "theme_preference": "dark"
}
```

**Response:** Same as GET /users/me

**Valid themes:** `light`, `dark`, `system`

## Validation Rules

### Philippine Mobile Number
- Format: `09XXXXXXXXX` or `+639XXXXXXXXX`
- Must be exactly 11 digits (09) or 13 characters (+639)
- Validated on profile update

### Email
- Must be valid email format
- Must be unique across all users
- Optional field

### Theme Preference
- Must be one of: `light`, `dark`, `system`
- Defaults to `system` on user creation

## Security

- All endpoints require authentication
- Users can only view/update their own profile
- Contact number and email uniqueness enforced at database level
- Duplicate checks performed before update

## Database Changes

Added `theme_preference` column to `users` table:
```sql
ALTER TABLE users ADD COLUMN theme_preference themepreference NOT NULL DEFAULT 'system';
CREATE TYPE themepreference AS ENUM ('light', 'dark', 'system');
```

## Example Usage

```bash
# Get profile
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>"

# Update profile
curl -X PUT http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan P. Dela Cruz",
    "email": "juan@example.com"
  }'

# Update theme preference
curl -X PUT http://localhost:8000/api/v1/users/me/preferences \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"theme_preference": "dark"}'
```

## Files Created/Modified

- Updated `app/models/user.py` - Added ThemePreference enum and field
- `app/schemas/user.py` - User schemas with validation
- `app/routers/users.py` - User profile endpoints
- `alembic/versions/002_add_theme_preference.py` - Database migration

## Setup

Run migration:
```bash
alembic upgrade head
```
