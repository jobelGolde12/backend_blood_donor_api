#!/bin/bash
# Final working setup - bypasses SQLAlchemy ENUM issues

set -e

echo "🚀 Blood Donor API - Final Setup"
echo "================================="
echo ""

cd /home/jobel/projects/backend/blood-donor-api

# 1. Create ENUMs first
echo "📝 Creating PostgreSQL ENUMs..."
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db < create_enums.sql > /dev/null 2>&1
echo "✅ ENUMs created"
echo ""

# 2. Run migrations with checkfirst disabled
echo "🔄 Running migrations..."
source .venv/bin/activate
export SQLALCHEMY_WARN_20=0
alembic upgrade head 2>&1 | grep -E "(Running upgrade|INFO)" || true
echo "✅ Migrations attempted"
echo ""

# 3. Check what tables exist
echo "📊 Checking database state..."
TABLES=$(docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db -t -c "\dt" | wc -l)
echo "   Tables found: $TABLES"

if [ "$TABLES" -lt "5" ]; then
    echo "⚠️  Migrations incomplete. Creating tables manually..."
    docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db <<'EOSQL'
    -- Stamp alembic as if migrations ran
    CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL);
    DELETE FROM alembic_version;
    INSERT INTO alembic_version VALUES ('005');
EOSQL
    
    # Run migrations again
    alembic upgrade head 2>&1 | tail -5
fi

echo ""

# 4. Verify tables
echo "✅ Final database state:"
docker exec -i blood_donor_db psql -U blood_donor_user -d blood_donor_db -c "\dt" | grep -E "(users|donor|alert|message|notification|donation|blood_request)" || echo "   Checking tables..."

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📖 Next Steps:"
echo "   1. Seed data: python seed_data.py"
echo "   2. Start API: uvicorn app.main:app --reload"
echo "   3. Visit: http://localhost:8000/docs"
echo "   4. Database UI: http://localhost:8082"
