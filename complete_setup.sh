#!/bin/bash
# Complete setup script

set -e

echo "🚀 Blood Donor API - Complete Setup"
echo "====================================="
echo ""

# Update .env
echo "📝 Updating .env file..."
cat > .env << 'EOF'
# Database - Use the DATABASE_URL provided by Render in production
# For local development, use the format below
DATABASE_URL=postgresql://blood_donor_user:blood_donor_pass@localhost:5432/blood_donor_db

# JWT
SECRET_KEY=dev-secret-key-change-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
APP_NAME=Blood Donor API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8081"]

# Redis
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
EOF

echo "✅ .env updated"
echo ""

# Activate venv
source .venv/bin/activate

# Run migrations
echo "🔄 Running migrations..."
alembic upgrade head
echo "✅ Migrations complete"
echo ""

# Seed data
echo "🌱 Seeding database..."
python seed_data.py
echo "✅ Seed complete"
echo ""

# Show summary
echo "📊 Database Summary:"
docker exec -it blood_donor_db psql -U blood_donor_user -d blood_donor_db -t -c "
SELECT 'Users: ' || COUNT(*) FROM users
UNION ALL
SELECT 'Registrations: ' || COUNT(*) FROM donor_registrations
UNION ALL
SELECT 'Donors: ' || COUNT(*) FROM donor_profiles
UNION ALL
SELECT 'Alerts: ' || COUNT(*) FROM alerts;
"

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📖 Access Points:"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Database (Adminer): http://localhost:8082"
echo "   - Admin Login: 09171234567"
echo ""
echo "🚀 Start API: uvicorn app.main:app --reload"
