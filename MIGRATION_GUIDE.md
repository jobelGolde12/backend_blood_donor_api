# Database Migration & Seeding Guide

## 📋 Prerequisites

1. **PostgreSQL installed and running**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   
   # Start PostgreSQL if not running
   sudo systemctl start postgresql
   ```

2. **Database created**
   ```bash
   # Create database
   sudo -u postgres psql -c "CREATE DATABASE blood_donor_db;"
   
   # Create user (if needed)
   sudo -u postgres psql -c "CREATE USER blood_donor_user WITH PASSWORD 'your_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE blood_donor_db TO blood_donor_user;"
   ```

3. **Environment configured**
   ```bash
   # Copy and edit .env file
   cp .env.example .env
   # Update DATABASE_URL in .env
   ```

## 🔄 Migration Execution

### Step 1: Verify Migration Files

Your migrations are already created:
- ✅ `001_create_users_table.py` - Users with roles and status
- ✅ `002_add_theme_preference.py` - Theme preference enum
- ✅ `003_create_donor_tables.py` - Donor registrations and profiles
- ✅ `004_create_messages_notifications.py` - Messaging and alerts
- ✅ `005_create_donations_requests.py` - Donations and blood requests

### Step 2: Run Migrations

```bash
# Activate virtual environment
source .venv/bin/activate

# Check current migration status
alembic current

# Run all pending migrations
alembic upgrade head

# Verify migrations applied
alembic current
# Should show: 005 (head)
```

### Step 3: Verify Database Schema

```bash
# Connect to database
psql -U blood_donor_user -d blood_donor_db

# List all tables
\dt

# List all enums
\dT+

# Check specific table structure
\d donor_registrations
\d donor_profiles
\d alerts
\d notifications

# Exit psql
\q
```

## 🌱 Seeding Data

### Run Seed Script

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Run seed script
python seed_data.py
```

### Expected Output

```
🚀 Starting database seed...
🌱 Seeding database with Philippine data...
✅ Created admin user (ID: 1)
✅ Created 20 registrations
✅ Created 14 donor users and profiles
✅ Created messages
✅ Created 5 alerts
✅ Created 87 notifications

🎉 Database seeded successfully!

📊 Summary:
   - 1 admin user
   - 20 donor registrations
   - 14 approved donors
   - 5 alerts
   - 87 notifications
```

### Seed Data Includes

**Admin User:**
- Contact: 09171234567
- Email: admin@blooddonor.ph
- Role: ADMIN

**Donor Registrations (20):**
- Filipino names (Juan Dela Cruz, Maria Santos, etc.)
- PH mobile numbers (09XX format)
- Philippine municipalities (Quezon City, Cebu, Davao, etc.)
- Mixed statuses: 70% approved, 20% pending, 10% rejected
- Realistic blood type distribution

**Alerts (5):**
- "Urgent O+ Blood Needed – Philippine General Hospital" (CRITICAL)
- "Red Cross Mobile Blood Drive – Quezon City" (MEDIUM)
- "AB- Blood Urgently Required – St. Luke's Medical Center" (CRITICAL)
- "Thank You to All Our Donors!" (LOW)
- "Blood Donation Camp – Cebu City" (MEDIUM)

**Notifications:**
- Alert notifications sent to matching donors
- System welcome notifications
- Mixed read/unread status

## 🔍 Migration Details

### Migration 003: Donor System

**ENUMs Created:**
```sql
CREATE TYPE bloodtype AS ENUM ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-');
CREATE TYPE availabilitystatus AS ENUM ('available', 'unavailable', 'recently_donated');
CREATE TYPE registrationstatus AS ENUM ('pending', 'approved', 'rejected');
```

**Tables:**
- `donor_registrations` - Pending/approved/rejected registrations
- `donor_profiles` - Active donor profiles linked to users

**Key Features:**
- Foreign key: `reviewed_by` → `users.id`
- Foreign key: `user_id` → `users.id` (unique)
- Foreign key: `registration_id` → `donor_registrations.id`
- Index on `contact_number`
- Unique index on `donor_profiles.user_id`

### Migration 004: Messaging & Notifications

**ENUMs Created:**
```sql
CREATE TYPE alerttype AS ENUM ('urgent_request', 'general_announcement', 'donation_drive');
CREATE TYPE priority AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE notificationtype AS ENUM ('alert', 'message_reply', 'system');
```

**Tables:**
- `messages` - Donor-to-admin communication
- `alerts` - Admin-created alerts with targeting
- `notifications` - Per-user notification delivery

**Key Features:**
- Foreign key: `donor_profile_id` → `donor_profiles.id`
- Foreign key: `created_by` → `users.id`
- Foreign key: `user_id` → `users.id`
- Foreign key: `alert_id` → `alerts.id` (nullable)
- Index on `notifications.user_id`
- Boolean defaults: `server_default='false'`
- JSON field for `target_audience`

## 🔄 Rollback Instructions

### Rollback One Migration
```bash
alembic downgrade -1
```

### Rollback to Specific Version
```bash
alembic downgrade 003
```

### Rollback All Migrations
```bash
alembic downgrade base
```

### Downgrade Safety

All migrations include proper downgrade logic:
- Tables dropped in reverse dependency order
- ENUMs dropped AFTER dependent tables
- Indexes dropped before tables
- Foreign keys handled automatically

## ✅ Verification Queries

```sql
-- Check all tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Check all enums
SELECT typname FROM pg_type 
WHERE typtype = 'e' 
ORDER BY typname;

-- Count records
SELECT 'users' as table_name, COUNT(*) FROM users
UNION ALL
SELECT 'donor_registrations', COUNT(*) FROM donor_registrations
UNION ALL
SELECT 'donor_profiles', COUNT(*) FROM donor_profiles
UNION ALL
SELECT 'messages', COUNT(*) FROM messages
UNION ALL
SELECT 'alerts', COUNT(*) FROM alerts
UNION ALL
SELECT 'notifications', COUNT(*) FROM notifications;

-- Check foreign key constraints
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name;
```

## 🚨 Troubleshooting

### Issue: "relation already exists"
```bash
# Check what's in the database
alembic current

# If migrations are out of sync, stamp the current version
alembic stamp head
```

### Issue: "type already exists"
The migrations use `CREATE TYPE` without `IF NOT EXISTS`. If you need to re-run:
```sql
-- Drop enums manually (after dropping dependent tables)
DROP TYPE IF EXISTS bloodtype CASCADE;
DROP TYPE IF EXISTS availabilitystatus CASCADE;
DROP TYPE IF EXISTS registrationstatus CASCADE;
DROP TYPE IF EXISTS alerttype CASCADE;
DROP TYPE IF EXISTS priority CASCADE;
DROP TYPE IF EXISTS notificationtype CASCADE;
```

### Issue: Foreign key constraint violation
Ensure migrations run in order:
1. 001 - users table first
2. 002 - theme preference
3. 003 - donor tables (depends on users)
4. 004 - messages/notifications (depends on donor_profiles)
5. 005 - donations (depends on donor_profiles)

## 📝 Notes

- All timestamps are timezone-aware (`DateTime(timezone=True)`)
- ENUMs are PostgreSQL-native (not SQLAlchemy fallback)
- Boolean fields use `server_default` for database-level defaults
- Indexes created for frequently queried columns
- Unique constraints enforced at database level
- Seed data uses realistic Philippine context
