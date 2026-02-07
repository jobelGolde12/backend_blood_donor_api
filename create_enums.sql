-- Create all PostgreSQL ENUMs for Blood Donor API
-- Run this BEFORE running Alembic migrations

-- User ENUMs
DO $$ BEGIN
    CREATE TYPE userrole AS ENUM ('admin', 'donor');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE userstatus AS ENUM ('active', 'inactive', 'suspended');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE themepreference AS ENUM ('light', 'dark', 'system');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- Donor ENUMs
DO $$ BEGIN
    CREATE TYPE bloodtype AS ENUM ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE availabilitystatus AS ENUM ('available', 'unavailable', 'recently_donated');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE registrationstatus AS ENUM ('pending', 'approved', 'rejected');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- Alert/Notification ENUMs
DO $$ BEGIN
    CREATE TYPE alerttype AS ENUM ('urgent_request', 'general_announcement', 'donation_drive');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE priority AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE notificationtype AS ENUM ('alert', 'message_reply', 'system');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- Donation ENUMs
DO $$ BEGIN
    CREATE TYPE urgencylevel AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- Verify ENUMs created
SELECT typname as enum_name FROM pg_type WHERE typtype = 'e' ORDER BY typname;
