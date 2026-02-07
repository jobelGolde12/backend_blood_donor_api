-- Quick Database Verification Script
-- Run after migrations: psql -U blood_donor_user -d blood_donor_db -f verify_schema.sql

\echo '=== CHECKING ENUMS ==='
SELECT typname as enum_name 
FROM pg_type 
WHERE typtype = 'e' 
ORDER BY typname;

\echo ''
\echo '=== CHECKING TABLES ==='
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

\echo ''
\echo '=== CHECKING FOREIGN KEYS ==='
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS references_table,
    ccu.column_name AS references_column
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name, kcu.column_name;

\echo ''
\echo '=== CHECKING INDEXES ==='
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

\echo ''
\echo '=== CHECKING UNIQUE CONSTRAINTS ==='
SELECT
    tc.table_name,
    kcu.column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'UNIQUE'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name, kcu.column_name;

\echo ''
\echo '=== RECORD COUNTS (after seeding) ==='
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'donor_registrations', COUNT(*) FROM donor_registrations
UNION ALL
SELECT 'donor_profiles', COUNT(*) FROM donor_profiles
UNION ALL
SELECT 'messages', COUNT(*) FROM messages
UNION ALL
SELECT 'alerts', COUNT(*) FROM alerts
UNION ALL
SELECT 'notifications', COUNT(*) FROM notifications
UNION ALL
SELECT 'donations', COUNT(*) FROM donations
UNION ALL
SELECT 'blood_requests', COUNT(*) FROM blood_requests
ORDER BY table_name;

\echo ''
\echo '=== SAMPLE DATA CHECK ==='
\echo 'Admin users:'
SELECT id, full_name, contact_number, role FROM users WHERE role = 'ADMIN';

\echo ''
\echo 'Donor registration status distribution:'
SELECT status, COUNT(*) as count 
FROM donor_registrations 
GROUP BY status 
ORDER BY status;

\echo ''
\echo 'Blood type distribution:'
SELECT blood_type, COUNT(*) as count 
FROM donor_profiles 
GROUP BY blood_type 
ORDER BY blood_type;

\echo ''
\echo 'Alert priorities:'
SELECT priority, COUNT(*) as count 
FROM alerts 
GROUP BY priority 
ORDER BY priority;

\echo ''
\echo '=== SCHEMA VERIFICATION COMPLETE ==='
