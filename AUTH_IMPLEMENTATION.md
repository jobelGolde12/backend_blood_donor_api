# Authentication System (TODO 2)

## Overview
JWT-based authentication with access and refresh tokens, role-based access control, and rate limiting.

## Endpoints

### POST /api/v1/auth/login
Login using Philippine mobile number.

**Rate Limit:** 5 requests/minute

**Request:**
```json
{
  "contact_number": "09123456789"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Status Codes:**
- 200: Success
- 401: Invalid credentials
- 403: Account not active
- 429: Rate limit exceeded

### POST /api/v1/auth/refresh
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Status Codes:**
- 200: Success
- 401: Invalid or expired refresh token

### POST /api/v1/auth/logout
Logout by invalidating refresh token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

## Token Details

### Access Token
- **Lifetime:** 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Type:** JWT with `type: "access"`
- **Payload:** `{"sub": "<user_id>", "role": "<role>", "exp": <timestamp>, "type": "access"}`

### Refresh Token
- **Lifetime:** 7 days (configurable via `REFRESH_TOKEN_EXPIRE_DAYS`)
- **Type:** JWT with `type: "refresh"`
- **Storage:** Hashed in database (`users.hashed_refresh_token`)
- **Payload:** `{"sub": "<user_id>", "exp": <timestamp>, "type": "refresh"}`

## Role-Based Access Control

### Roles
- `admin`: Full system access
- `donor`: Donor-specific access

### Dependencies

**Require any authenticated user:**
```python
from app.core.dependencies import get_current_user

@router.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"user_id": user.id}
```

**Require admin:**
```python
from app.core.dependencies import get_current_admin

@router.get("/admin-only")
async def admin_route(user: User = Depends(get_current_admin)):
    return {"admin_id": user.id}
```

**Require donor:**
```python
from app.core.dependencies import get_current_donor

@router.get("/donor-only")
async def donor_route(user: User = Depends(get_current_donor)):
    return {"donor_id": user.id}
```

## Security Features

1. **Rate Limiting:** Login endpoint limited to 5 requests/minute per IP
2. **Token Validation:** Tokens verified for signature, expiration, and type
3. **Refresh Token Rotation:** New refresh token issued on each refresh
4. **Hashed Storage:** Refresh tokens hashed before database storage
5. **Account Status Check:** Only active users can authenticate
6. **Philippine Number Validation:** Contact numbers validated against PH format

## Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    contact_number VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE,
    role userrole NOT NULL DEFAULT 'DONOR',
    status userstatus NOT NULL DEFAULT 'ACTIVE',
    hashed_refresh_token VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TYPE userrole AS ENUM ('ADMIN', 'DONOR');
CREATE TYPE userstatus AS ENUM ('ACTIVE', 'INACTIVE', 'SUSPENDED');
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migration:
```bash
alembic upgrade head
```

3. Configure environment variables in `.env`:
```env
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Example Usage

### Login Flow
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"contact_number": "09123456789"}'

# Use access token
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>"

# Refresh when access token expires
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'

# Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer <access_token>"
```

## Files Created

- `app/models/user.py` - User model with refresh token storage
- `app/schemas/auth.py` - Auth request/response schemas
- `app/routers/auth.py` - Auth endpoints (login, refresh, logout)
- `app/core/dependencies.py` - Auth dependencies for route protection
- `alembic/versions/001_create_users_table.py` - Database migration
- Updated `app/main.py` - Added rate limiting support
- Updated `requirements.txt` - Added slowapi

## Notes

- OTP functionality can be added later by extending the login endpoint
- Password-based auth can be added by adding `hashed_password` field to User model
- Consider adding refresh token blacklist for enhanced security
- Rate limiting uses in-memory storage; use Redis for production
