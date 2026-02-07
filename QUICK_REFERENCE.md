# Quick Reference Card

## 🚀 One-Command Setup
```bash
./setup_database.sh
```

## 📋 Manual Commands

### Run Migrations
```bash
source .venv/bin/activate
alembic upgrade head
```

### Seed Database
```bash
python seed_data.py
```

### Verify Schema
```bash
psql -U blood_donor_user -d blood_donor_db -f verify_schema.sql
```

### Check Migration Status
```bash
alembic current
alembic history
```

### Rollback
```bash
alembic downgrade -1        # One step back
alembic downgrade 003       # To specific version
alembic downgrade base      # Remove all
```

## 🗄️ Database Schema

### ENUMs (8 total)
- `bloodtype` - A+, A-, B+, B-, AB+, AB-, O+, O-
- `availabilitystatus` - available, unavailable, recently_donated
- `registrationstatus` - pending, approved, rejected
- `alerttype` - urgent_request, general_announcement, donation_drive
- `priority` - low, medium, high, critical
- `notificationtype` - alert, message_reply, system
- `userrole` - ADMIN, DONOR
- `userstatus` - ACTIVE, INACTIVE, SUSPENDED
- `themepreference` - light, dark, system
- `urgencylevel` - low, medium, high, critical

### Tables (8 total)
1. `users` - Authentication and profiles
2. `donor_registrations` - Registration submissions
3. `donor_profiles` - Approved donor profiles
4. `messages` - Donor-to-admin messages
5. `alerts` - Admin-created alerts
6. `notifications` - User notifications
7. `donations` - Donation history
8. `blood_requests` - Blood request tracking

## 🔗 Key Relationships

```
users (admin) ──┬─> donor_registrations.reviewed_by
                ├─> alerts.created_by
                ├─> notifications.user_id
                └─> blood_requests.created_by

users (donor) ──> donor_profiles.user_id (unique)

donor_profiles ──┬─> messages.donor_profile_id
                 └─> donations.donor_profile_id

donor_registrations ──> donor_profiles.registration_id

alerts ──> notifications.alert_id (nullable)
```

## 🌱 Seed Data Summary

After seeding, you'll have:
- **1** admin user (09171234567)
- **20** donor registrations
  - 14 approved (70%)
  - 4 pending (20%)
  - 2 rejected (10%)
- **14** donor profiles
- **8** messages
- **5** alerts
- **~87** notifications

## 🇵🇭 Sample Data

### Admin Login
- Contact: `09171234567`
- Email: `admin@blooddonor.ph`

### Sample Donor Names
- Juan Dela Cruz
- Maria Clara Santos
- Mark Anthony Bautista
- Princess Joy Mendoza

### Sample Municipalities
- Quezon City, Manila, Cebu City
- Davao City, Makati, Pasig

### Sample Alerts
- "Urgent O+ Blood Needed – Philippine General Hospital"
- "Red Cross Mobile Blood Drive – Quezon City"

## 🔍 Useful SQL Queries

### Count All Records
```sql
SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'registrations', COUNT(*) FROM donor_registrations
UNION ALL SELECT 'profiles', COUNT(*) FROM donor_profiles
UNION ALL SELECT 'messages', COUNT(*) FROM messages
UNION ALL SELECT 'alerts', COUNT(*) FROM alerts
UNION ALL SELECT 'notifications', COUNT(*) FROM notifications;
```

### Check Registration Status
```sql
SELECT status, COUNT(*) 
FROM donor_registrations 
GROUP BY status;
```

### Blood Type Distribution
```sql
SELECT blood_type, COUNT(*) 
FROM donor_profiles 
GROUP BY blood_type 
ORDER BY COUNT(*) DESC;
```

### Unread Notifications
```sql
SELECT u.full_name, COUNT(*) as unread
FROM notifications n
JOIN users u ON n.user_id = u.id
WHERE n.is_read = false
GROUP BY u.full_name;
```

## 🚨 Troubleshooting

### PostgreSQL not running
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### Database doesn't exist
```bash
createdb blood_donor_db
# or
sudo -u postgres psql -c "CREATE DATABASE blood_donor_db;"
```

### Migration out of sync
```bash
alembic current
alembic stamp head  # Force sync
```

### Reset database completely
```bash
alembic downgrade base
dropdb blood_donor_db
createdb blood_donor_db
alembic upgrade head
python seed_data.py
```

## 📚 Documentation Files

- `MIGRATION_GUIDE.md` - Complete migration guide
- `MIGRATION_IMPLEMENTATION.md` - Implementation summary
- `README.md` - API documentation
- `seed_data.py` - Seed script
- `verify_schema.sql` - Verification queries
- `setup_database.sh` - Automated setup

## 🎯 Next Steps

1. ✅ Run migrations
2. ✅ Seed database
3. ✅ Verify schema
4. 🚀 Start API: `uvicorn app.main:app --reload`
5. 📖 Visit docs: `http://localhost:8000/docs`
6. 🔐 Test login with admin credentials
