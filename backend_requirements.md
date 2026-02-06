✅ TODO 1 (Already implemented) — Analyze and Formalize Backend Architecture

Prompt to AI:

Design a production-ready FastAPI backend architecture for a blood donor coordination system.

Requirements:

Use FastAPI

Use PostgreSQL

Use SQLAlchemy (2.0 style) or SQLModel

Use Alembic for migrations

Use Pydantic for request/response schemas

Implement JWT authentication (access + refresh tokens)

Role-based access control (admin, donor)

Tasks:

Define project folder structure (routers, models, schemas, services, core, db).

Define dependency injection for DB sessions.

Configure environment variables using .env.

Implement centralized exception handling.

Implement structured logging.

Prepare base configuration for background tasks (Celery or FastAPI background tasks).

Output:

Proposed folder structure

Base app setup code

Database connection config

Auth scaffolding

✅ TODO 2 (Already implemented) — Implement Authentication System

Prompt to AI:

Implement JWT-based authentication in FastAPI for the following:

Endpoints:

POST /auth/login

POST /auth/refresh

POST /auth/logout

Requirements:

Login using full_name + contact_number OR OTP-ready structure.

Issue access token (short-lived) and refresh token (long-lived).

Store hashed refresh tokens in DB.

Implement role-based access control (admin, donor).

Protect endpoints using dependency injection.

Add rate limiting for login endpoint.

Output:

Models

Schemas

Router implementation

JWT utilities

Password hashing utilities

Example responses

✅ TODO 3 (Already implemented) — Implement User & Preference Module

Prompt to AI:

Implement user profile management.

Endpoints:

GET /users/me

PUT /users/me

PUT /users/me/preferences

Requirements:

Store user info (name, contact, email, role, status).

Store theme preferences (light, dark, system).

Restrict access to authenticated users.

Validate Philippine mobile numbers.

Ensure only owner can update their profile.

Output:

SQLAlchemy models

Pydantic schemas

Router

Validation logic

✅ TODO 4 — Implement Donor Registration Workflow

Prompt to AI:

Implement donor self-registration and admin review workflow.

Endpoints:

POST /donor-registrations

GET /donor-registrations (admin)

PATCH /donor-registrations/{id}

Requirements:

Registration defaults to "pending".

Approved registrations create donor_profile record.

Rejected registrations store review reason.

Prevent duplicate contact numbers.

Validate:

Age (1–120)

Blood type enum

Availability enum

Output:

Models

Schemas

Approval service logic

Status transition validation

✅ TODO 5 — Implement Donor Management (Admin CRUD)

Prompt to AI:

Implement donor management module.

Endpoints:

GET /donors

GET /donors/{id}

POST /donors (admin)

PATCH /donors/{id}

PATCH /donors/{id}/availability

DELETE /donors/{id} (soft delete)

Requirements:

Filtering by:

blood_type

municipality

availability

search query (name or contact)

Pagination support.

Only approved donors appear in public listing.

Soft delete logic.

Track updated_at timestamps.

Output:

Query builder logic

Pagination response format

Availability state validation rules

✅ TODO 6 — Implement Messages (Donor → Admin)

Prompt to AI:

Implement messaging module.

Endpoints:

POST /messages

GET /messages (admin)

Requirements:

Donors can send message to admin.

Admin can mark message as closed.

Messages linked to donor_profile.

Generate notification for admin on new message.

Output:

Models

Schemas

Notification trigger logic

✅ TODO 7 — Implement Alerts & Notification Fan-Out

Prompt to AI:

Implement alert creation and notification fan-out system.

Endpoints:

POST /alerts

GET /alerts

POST /alerts/{id}/send

Requirements:

Support:

alert_type enum

priority enum

target_audience JSON filters

If send_now = true → generate notifications immediately.

If scheduled → store schedule_at and process later.

Fan-out notifications to matching donors.

Create notification records per user.

Output:

Alert model

Notification model

Background processing logic

Audience filter query logic

✅ TODO 8 — Implement Notifications Module

Prompt to AI:

Implement notification system.

Endpoints:

GET /notifications

PATCH /notifications/{id}/read

PATCH /notifications/read-all

DELETE /notifications/{id}

Requirements:

Return unread count.

Support filtering by:

type

is_read

Soft delete notifications.

Restrict to owner user.

Output:

Query filters

Ownership enforcement

Optimized unread count logic

✅ TODO 9 — Implement Donations & Blood Requests

Prompt to AI:

Implement donation tracking and blood request management.

Endpoints:

GET /donations

POST /donations

GET /requests

POST /requests

Requirements:

Link donations to donor_profile.

Update donor availability after donation.

Track urgency levels.

Support filtering by date range.

Output:

Models

Business rules for availability transition

Validation logic

✅ TODO 10 — Implement Reports & Analytics

Prompt to AI:

Implement reporting endpoints.

Endpoints:

GET /reports/summary

GET /reports/blood-type-distribution

GET /reports/monthly-donations

GET /reports/availability-trend

Requirements:

Accept date range filters.

Support municipality filter.

Use optimized aggregation queries.

Return structured JSON for charts.

Output:

Aggregation queries

Example response format

Performance considerations

✅ TODO 11 — Optional: Chatbot Proxy Endpoint

Prompt to AI:

Implement secure chatbot proxy endpoint:

Endpoint:

POST /chatbot/respond

Requirements:

Forward request to OpenRouter API.

Keep API key server-side.

Rate limit per user.

Log usage.

Return streamed or standard response.

Output:

Proxy route

Error handling

Rate limiting logic

✅ TODO 12 — Implement Validation & Security Hardening

Prompt to AI:

Apply production-grade validation and security:

Requirements:

Validate PH contact number format.

Enforce enum constraints.

Add CORS configuration for Expo.

Add rate limiting (login + chatbot).

Sanitize search queries.

Add audit fields (created_at, updated_at).

Implement soft delete across major entities.

Output:

Middleware

Validators

Security notes

Final checklist

If you follow this TODO list step-by-step, you basically go from:

“Mocked React Native app”

to

“Production-grade FastAPI backend with real architecture.”

If you want, I can also turn this into:

🚀 A GitHub Issues board format

📋 Scrum sprint breakdown

🧱 Or a prioritized MVP-only version (so you don’t overbuild)

Tell me how serious this deployment is going to be.

The fash api is a separate project for backend right?

Yes. 100% yes.

FastAPI should be a separate project from your React Native + Expo app.

Think of it like this:

📱 React Native (Expo) → Frontend app

⚙️ FastAPI → Backend API server

🗄️ Database → PostgreSQL (or whatever you choose)

They live in different folders, different runtimes, sometimes even different servers.

🧠 Typical Setup

You’ll usually structure it like:

blood-donor-system/
│
├── mobile-app/        → React Native + Expo project
│
└── backend/           → FastAPI project


Or even completely separate GitHub repos:

blood-donor-mobile

blood-donor-api

Both are valid.

Why It Should Be Separate

Because:

Different runtime

Expo → JavaScript / TypeScript

FastAPI → Python

Different deployment

Expo → EAS / Play Store / App Store