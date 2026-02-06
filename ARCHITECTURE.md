# Blood Donor API - FastAPI Backend Architecture

## 📁 Project Structure

```
blood-donor-api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app factory
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Environment variables & settings
│   │   ├── security.py           # JWT & password utilities
│   │   ├── logging.py            # Structured logging setup
│   │   └── celery_app.py         # Celery configuration
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py            # Database connection & session
│   │   └── dependencies.py       # Dependency injection
│   ├── models/                    # SQLAlchemy models
│   │   └── __init__.py
│   ├── schemas/                   # Pydantic schemas
│   │   └── __init__.py
│   ├── routers/                   # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── donors.py
│   │   ├── donor_registrations.py
│   │   ├── messages.py
│   │   ├── alerts.py
│   │   ├── notifications.py
│   │   ├── donations.py
│   │   └── reports.py
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── notification_service.py
│   │   ├── alert_service.py
│   │   └── donation_service.py
│   ├── middleware/                # Custom middleware
│   │   ├── __init__.py
│   │   └── exception_handler.py
│   └── utils/                     # Utility functions
│       └── __init__.py
├── alembic/                       # Database migrations
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── ...
├── logs/                          # Application logs
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
├── alembic.ini                   # Alembic configuration
└── main.py                       # Application entry point
```

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: Authentication tokens (python-jose)
- **Celery**: Distributed task queue
- **Redis**: Message broker and result backend
- **bcrypt**: Password hashing
- **Uvicorn**: ASGI server

## 🔧 Key Features Implemented

### 1. **Project Structure**
- Clean separation of concerns with dedicated modules
- Router-based organization for API endpoints
- Service layer for business logic
- Centralized configuration management

### 2. **Database Configuration**
- SQLAlchemy 2.0 with async support
- Connection pooling and session management
- Dependency injection for database sessions
- Alembic integration for migrations

### 3. **Authentication & Security**
- JWT-based authentication with access/refresh tokens
- Password hashing with bcrypt
- Role-based access control (admin, donor)
- Secure token verification utilities

### 4. **Environment Configuration**
- Environment-based settings management
- Support for development/production environments
- Database connection strings
- JWT secret key configuration
- CORS settings

### 5. **Error Handling**
- Centralized exception handling
- Custom exception classes
- Structured error responses
- Database error handling
- Validation error formatting

### 6. **Logging**
- Structured JSON logging
- Configurable log levels
- File and console output
- Request context logging
- Application performance monitoring

### 7. **Background Tasks**
- Celery configuration with Redis broker
- Task scheduling and periodic jobs
- Notification system support
- Alert processing

### 8. **API Structure**
- RESTful API design
- Versioned endpoints (/api/v1/)
- Automatic API documentation (OpenAPI/Swagger)
- Health check endpoint

## 🚀 Getting Started

### 1. **Environment Setup**
```bash
# Copy environment variables template
cp .env.example .env

# Edit with your configuration
# DATABASE_URL, SECRET_KEY, etc.
```

### 2. **Install Dependencies**
```bash
# Using uv (recommended)
uv sync

# Or pip
pip install -r requirements.txt
```

### 3. **Database Setup**
```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. **Run Development Server**
```bash
# Start FastAPI server
uvicorn app.main:app --reload

# Start Celery worker (separate terminal)
celery -A app.core.celery_app worker --loglevel=info

# Start Celery beat scheduler (another terminal)
celery -A app.core.celery_app beat --loglevel=info
```

## 📋 Next Steps

This architecture provides the foundation for implementing all the TODO items from the requirements:

1. ✅ **TODO 1** - Backend Architecture (Complete)
2. ⏳ **TODO 2** - Authentication System
3. ⏳ **TODO 3** - User & Preference Module
4. ⏳ **TODO 4** - Donor Registration Workflow
5. ⏳ **TODO 5** - Donor Management (Admin CRUD)
6. ⏳ **TODO 6** - Messages (Donor → Admin)
7. ⏳ **TODO 7** - Alerts & Notification Fan-Out
8. ⏳ **TODO 8** - Notifications Module
9. ⏳ **TODO 9** - Donations & Blood Requests
10. ⏳ **TODO 10** - Reports & Analytics
11. ⏳ **TODO 11** - Optional: Chatbot Proxy Endpoint
12. ⏳ **TODO 12** - Validation & Security Hardening

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- CORS middleware configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- Rate limiting support
- Environment-based configuration

## 📊 Production Considerations

- Structured logging for monitoring
- Health check endpoints
- Graceful error handling
- Database connection pooling
- Background task processing
- Configuration management
- Migration support

This architecture provides a solid, production-ready foundation for the blood donor coordination system backend.