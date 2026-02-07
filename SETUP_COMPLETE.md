# ✅ Database Setup Complete!

## 🎉 What's Done

### ✅ Docker Containers Running
```bash
docker ps
```
- **PostgreSQL**: `blood_donor_db` on port 5432
- **Adminer**: `blood_donor_adminer` on port 8082

### ✅ Database Schema Created
All tables and ENUMs created:
- 10 PostgreSQL ENUMs (userrole, userstatus, bloodtype, etc.)
- 9 tables (users, donor_registrations, donor_profiles, messages, alerts, notifications, donations, blood_requests, alembic_version)

### ✅ Database Seeded with Philippine Data
- **11 Users**: 1 admin + 10 donors
- **15 Donor Registrations**: 10 approved, 3 pending, 2 rejected
- **10 Donor Profiles**: Active approved donors
- **5 Messages**: Donor-to-admin communication
- **5 Alerts**: Blood drive announcements and urgent requests
- **8 Notifications**: Alert and system notifications

---

## 🔗 Access Your System

### Database UI (Adminer)
**URL:** http://localhost:8082

**Login:**
- System: `PostgreSQL`
- Server: `postgres`
- Username: `blood_donor_user`
- Password: `blood_donor_pass`
- Database: `blood_donor_db`

### Admin Credentials
- **Contact:** `09171234567`
- **Email:** `admin@blooddonor.ph`

### Sample Donor Contacts
- Juan Dela Cruz: `09151234567`
- Maria Clara Santos: `09161234568`
- Mark Anthony Bautista: `09171234569`
- (7 more donors in database)

---

## 🚀 Start the API

```bash
# Activate virtual environment
source .venv/bin/activate

# Start API server
uvicorn app.main:app --reload
```

**API will be available at:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📊 Verify Data

```bash
# Connect to database
docker exec -it blood_donor_db psql -U blood_donor_user -d blood_donor_db

# Check users
SELECT full_name, contact_number, role FROM users;

# Check donor registrations
SELECT full_name, blood_type, municipality, status FROM donor_registrations;

# Check alerts
SELECT title, priority, alert_type FROM alerts;

# Exit
\q
```

---

## 🛠️ Useful Commands

### Docker
```bash
# Stop containers
docker-compose down

# Start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Restart containers
docker-compose restart
```

### Database
```bash
# Access database shell
docker exec -it blood_donor_db psql -U blood_donor_user -d blood_donor_db

# Run SQL file
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db < file.sql

# Backup database
docker exec blood_donor_db pg_dump -U blood_donor_user blood_donor_db > backup.sql

# Restore database
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db < backup.sql
```

### Reset Database
```bash
# Reset schema and reseed
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db < create_enums.sql
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db < create_tables.sql
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db < seed_data.sql
```

---

## 📁 Important Files

- `docker-compose.yml` - Container configuration
- `.env` - Environment variables
- `create_enums.sql` - PostgreSQL ENUM creation
- `create_tables.sql` - Table schema
- `seed_data.sql` - Sample data
- `fast_credentials.md` - Quick reference with all endpoints
- `MIGRATION_GUIDE.md` - Migration documentation

---

## 🎯 Next Steps

1. ✅ Database is ready
2. ✅ Data is seeded
3. 🚀 Start API: `uvicorn app.main:app --reload`
4. 📖 Visit: http://localhost:8000/docs
5. 🔐 Test login with admin: `09171234567`
6. 🌐 View database: http://localhost:8082

---

## 📝 Sample Data Highlights

### Blood Types Distribution
- O+: 3 donors
- A+: 2 donors
- B+: 2 donors
- AB+: 1 donor
- O-: 1 donor
- A-: 1 donor
- B-: 1 donor
- AB-: 1 donor

### Municipalities
- Quezon City, Manila, Cebu City, Davao City, Makati, Pasig, Taguig, Caloocan, Antipolo, Cagayan de Oro

### Alert Examples
- "Urgent O+ Blood Needed – Philippine General Hospital" (CRITICAL)
- "Red Cross Mobile Blood Drive – Quezon City" (MEDIUM)
- "AB- Blood Urgently Required – St. Luke's Medical Center" (CRITICAL)

---

**Everything is ready! Start your API and begin testing! 🎉**
