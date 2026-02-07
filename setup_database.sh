#!/bin/bash
# Quick Start Script - Setup Database and Seed Data
# Usage: ./setup_database.sh

set -e  # Exit on error

echo "🚀 Blood Donor API - Database Setup"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file. Please update DATABASE_URL and other settings.${NC}"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Source .env
export $(grep -v '^#' .env | xargs)

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL..."
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo -e "${RED}❌ PostgreSQL is not running on localhost:5432${NC}"
    echo "   Start it with: sudo systemctl start postgresql"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL is running${NC}"
echo ""

# Check if database exists
DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
echo "🔍 Checking database: $DB_NAME"
if ! psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo -e "${YELLOW}⚠️  Database '$DB_NAME' does not exist${NC}"
    read -p "Create database? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        createdb $DB_NAME
        echo -e "${GREEN}✅ Database created${NC}"
    else
        echo -e "${RED}❌ Cannot proceed without database${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Database exists${NC}"
fi
echo ""

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo "   Create it with: python -m venv .venv"
    exit 1
fi

echo "🔧 Activating virtual environment..."
source .venv/bin/activate
echo ""

# Check current migration status
echo "🔍 Checking migration status..."
CURRENT_VERSION=$(alembic current 2>/dev/null | grep -oP '(?<=\(head\)|^)[a-f0-9]+' || echo "none")
echo "   Current version: $CURRENT_VERSION"
echo ""

# Run migrations
echo "🔄 Running migrations..."
alembic upgrade head
echo -e "${GREEN}✅ Migrations completed${NC}"
echo ""

# Check if database is already seeded
echo "🔍 Checking if database needs seeding..."
USER_COUNT=$(psql $DATABASE_URL -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null || echo "0")
USER_COUNT=$(echo $USER_COUNT | xargs)  # Trim whitespace

if [ "$USER_COUNT" -gt "0" ]; then
    echo -e "${YELLOW}⚠️  Database already has $USER_COUNT users${NC}"
    read -p "Skip seeding? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping seed..."
    else
        echo "🌱 Seeding database..."
        python seed_data.py
    fi
else
    echo "🌱 Seeding database with Philippine data..."
    python seed_data.py
fi
echo ""

# Verify schema
echo "🔍 Verifying schema..."
psql $DATABASE_URL -f verify_schema.sql > /dev/null 2>&1
echo -e "${GREEN}✅ Schema verified${NC}"
echo ""

# Show summary
echo "📊 Database Summary:"
psql $DATABASE_URL -t -c "
SELECT 
    'Users: ' || COUNT(*) FROM users
UNION ALL
SELECT 
    'Donor Registrations: ' || COUNT(*) FROM donor_registrations
UNION ALL
SELECT 
    'Donor Profiles: ' || COUNT(*) FROM donor_profiles
UNION ALL
SELECT 
    'Alerts: ' || COUNT(*) FROM alerts
UNION ALL
SELECT 
    'Notifications: ' || COUNT(*) FROM notifications;
"

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Start the API: uvicorn app.main:app --reload"
echo "  2. Visit docs: http://localhost:8000/docs"
echo "  3. Login with admin: 09171234567"
echo ""
