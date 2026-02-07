-- Complete database schema creation
-- Run this to create all tables

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    contact_number VARCHAR NOT NULL,
    email VARCHAR,
    role userrole NOT NULL,
    status userstatus NOT NULL,
    theme_preference themepreference NOT NULL DEFAULT 'system',
    hashed_refresh_token VARCHAR,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users(id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_contact_number ON users(contact_number);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- Donor registrations table
CREATE TABLE IF NOT EXISTS donor_registrations (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    contact_number VARCHAR NOT NULL,
    email VARCHAR,
    age INTEGER NOT NULL,
    blood_type bloodtype NOT NULL,
    municipality VARCHAR NOT NULL,
    availability availabilitystatus NOT NULL,
    status registrationstatus NOT NULL,
    review_reason TEXT,
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_donor_registrations_contact_number ON donor_registrations(contact_number);

-- Donor profiles table
CREATE TABLE IF NOT EXISTS donor_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    registration_id INTEGER NOT NULL REFERENCES donor_registrations(id),
    age INTEGER NOT NULL,
    blood_type bloodtype NOT NULL,
    municipality VARCHAR NOT NULL,
    availability availabilitystatus NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_donor_profiles_user_id ON donor_profiles(user_id);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    donor_profile_id INTEGER NOT NULL REFERENCES donor_profiles(id),
    subject VARCHAR NOT NULL,
    content TEXT NOT NULL,
    is_closed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    message TEXT NOT NULL,
    alert_type alerttype NOT NULL,
    priority priority NOT NULL,
    target_audience JSON,
    send_now BOOLEAN NOT NULL DEFAULT TRUE,
    schedule_at TIMESTAMPTZ,
    sent_at TIMESTAMPTZ,
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR NOT NULL,
    message TEXT NOT NULL,
    notification_type notificationtype NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    alert_id INTEGER REFERENCES alerts(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_notifications_user_id ON notifications(user_id);

-- Donations table
CREATE TABLE IF NOT EXISTS donations (
    id SERIAL PRIMARY KEY,
    donor_profile_id INTEGER NOT NULL REFERENCES donor_profiles(id),
    donation_date DATE NOT NULL,
    blood_type bloodtype NOT NULL,
    units INTEGER NOT NULL DEFAULT 1,
    location VARCHAR NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Blood requests table
CREATE TABLE IF NOT EXISTS blood_requests (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR NOT NULL,
    blood_type bloodtype NOT NULL,
    units_needed INTEGER NOT NULL,
    urgency urgencylevel NOT NULL,
    hospital VARCHAR NOT NULL,
    contact_number VARCHAR NOT NULL,
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alembic version table
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

DELETE FROM alembic_version;
INSERT INTO alembic_version VALUES ('005');

-- Verify tables created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;
