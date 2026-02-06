# Blood Donor API

Production-ready FastAPI backend for blood donor coordination system.

## Features

- ✅ JWT Authentication with refresh tokens
- ✅ Role-based access control (admin, donor)
- ✅ Donor registration workflow with admin approval
- ✅ Donor management with filtering and search
- ✅ Messaging system (donor to admin)
- ✅ Alert creation with notification fan-out
- ✅ Donation tracking and blood requests
- ✅ Reports and analytics
- ✅ Rate limiting
- ✅ Philippine mobile number validation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Migrations

```bash
alembic upgrade head
```

### 4. Start Server

```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

## API Documentation

Interactive API docs: `http://localhost:8000/docs`

### Authentication

**POST /api/v1/auth/login** - Login with contact number  
**POST /api/v1/auth/refresh** - Refresh access token  
**POST /api/v1/auth/logout** - Logout

### User Profile

**GET /api/v1/users/me** - Get current user profile  
**PUT /api/v1/users/me** - Update profile  
**PUT /api/v1/users/me/preferences** - Update theme preference

### Donor Registration

**POST /api/v1/donor-registrations** - Submit registration (public)  
**GET /api/v1/donor-registrations** - List registrations (admin)  
**PATCH /api/v1/donor-registrations/{id}** - Approve/reject (admin)

### Donor Management

**GET /api/v1/donors** - List donors with filters  
**GET /api/v1/donors/{id}** - Get donor details  
**PATCH /api/v1/donors/{id}** - Update donor (admin)  
**PATCH /api/v1/donors/{id}/availability** - Update availability (admin)  
**DELETE /api/v1/donors/{id}** - Soft delete donor (admin)

### Messages

**POST /api/v1/messages** - Send message to admin (donor)  
**GET /api/v1/messages** - List messages (admin)  
**PATCH /api/v1/messages/{id}/close** - Close message (admin)

### Alerts & Notifications

**POST /api/v1/alerts** - Create alert (admin)  
**GET /api/v1/alerts** - List alerts (admin)  
**POST /api/v1/alerts/{id}/send** - Send scheduled alert (admin)  
**GET /api/v1/notifications** - List user notifications  
**GET /api/v1/notifications/unread-count** - Get unread count  
**PATCH /api/v1/notifications/{id}/read** - Mark as read  
**PATCH /api/v1/notifications/read-all** - Mark all as read  
**DELETE /api/v1/notifications/{id}** - Delete notification

### Donations & Requests

**GET /api/v1/donations/donations** - List donations (admin)  
**POST /api/v1/donations/donations** - Record donation (admin)  
**GET /api/v1/donations/requests** - List blood requests  
**POST /api/v1/donations/requests** - Create blood request (admin)

### Reports

**GET /api/v1/reports/summary** - Summary statistics (admin)  
**GET /api/v1/reports/blood-type-distribution** - Blood type distribution (admin)  
**GET /api/v1/reports/monthly-donations** - Monthly donation stats (admin)  
**GET /api/v1/reports/availability-trend** - Availability trend (admin)

## Database Schema

### Users
- Authentication and profile data
- Roles: admin, donor
- Theme preferences

### Donor Registrations
- Pending, approved, or rejected
- Creates donor profile on approval

### Donor Profiles
- Linked to user account
- Blood type, municipality, availability

### Messages
- Donor to admin communication
- Can be closed by admin

### Alerts
- Created by admin
- Target audience filtering
- Immediate or scheduled sending

### Notifications
- Generated from alerts
- Per-user delivery
- Read/unread tracking

### Donations
- Donation history
- Updates donor availability

### Blood Requests
- Patient information
- Urgency levels
- Hospital details

## Project Structure

```
app/
├── core/           # Config, security, logging
├── db/             # Database session and dependencies
├── middleware/     # Exception handlers
├── models/         # SQLAlchemy models
├── routers/        # API endpoints
├── schemas/        # Pydantic schemas
├── services/       # Business logic
└── utils/          # Utilities
```

## Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token lifetime (default: 30)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token lifetime (default: 7)

## Development

### Run Tests
```bash
pytest
```

### Format Code
```bash
black app/
isort app/
```

### Lint
```bash
flake8 app/
mypy app/
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Set `ENVIRONMENT=production`
3. Use strong `SECRET_KEY`
4. Configure proper `ALLOWED_ORIGINS`
5. Use production database
6. Run with gunicorn:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

MIT