-- Seed data for Blood Donor API
-- Philippine-based realistic test data

-- 1. Create admin user
INSERT INTO users (full_name, contact_number, email, role, status, theme_preference, created_at)
VALUES ('Admin User', '09171234567', 'admin@blooddonor.ph', 'admin', 'active', 'system', NOW())
RETURNING id;

-- Store admin ID for later use (ID will be 1)

-- 2. Create donor registrations (approved)
INSERT INTO donor_registrations (full_name, contact_number, email, age, blood_type, municipality, availability, status, reviewed_by, reviewed_at, created_at)
VALUES 
('Juan Dela Cruz', '09151234567', 'juan.delacruz@email.com', 28, 'O+', 'Quezon City', 'available', 'approved', 1, NOW() - INTERVAL '2 days', NOW() - INTERVAL '5 days'),
('Maria Clara Santos', '09161234568', 'maria.santos@email.com', 32, 'A+', 'Manila', 'available', 'approved', 1, NOW() - INTERVAL '3 days', NOW() - INTERVAL '7 days'),
('Mark Anthony Bautista', '09171234569', 'mark.bautista@email.com', 25, 'B+', 'Cebu City', 'available', 'approved', 1, NOW() - INTERVAL '1 day', NOW() - INTERVAL '4 days'),
('Princess Joy Mendoza', '09261234570', 'princess.mendoza@email.com', 29, 'AB+', 'Davao City', 'available', 'approved', 1, NOW() - INTERVAL '2 days', NOW() - INTERVAL '6 days'),
('John Paul Villanueva', '09271234571', 'john.villanueva@email.com', 35, 'O-', 'Makati', 'available', 'approved', 1, NOW() - INTERVAL '1 day', NOW() - INTERVAL '3 days'),
('Mary Grace Fernandez', '09351234572', 'mary.fernandez@email.com', 27, 'A-', 'Pasig', 'recently_donated', 'approved', 1, NOW() - INTERVAL '3 days', NOW() - INTERVAL '8 days'),
('Angelo Miguel Torres', '09361234573', 'angelo.torres@email.com', 31, 'B-', 'Taguig', 'available', 'approved', 1, NOW() - INTERVAL '2 days', NOW() - INTERVAL '5 days'),
('Kristine Mae Ramos', '09451234574', 'kristine.ramos@email.com', 26, 'AB-', 'Caloocan', 'unavailable', 'approved', 1, NOW() - INTERVAL '1 day', NOW() - INTERVAL '4 days'),
('Joshua Emmanuel Cruz', '09551234575', 'joshua.cruz@email.com', 30, 'O+', 'Antipolo', 'available', 'approved', 1, NOW() - INTERVAL '2 days', NOW() - INTERVAL '6 days'),
('Angel Faith Gonzales', '09561234576', 'angel.gonzales@email.com', 24, 'A+', 'Cagayan de Oro', 'available', 'approved', 1, NOW() - INTERVAL '3 days', NOW() - INTERVAL '7 days');

-- 3. Create donor registrations (pending)
INSERT INTO donor_registrations (full_name, contact_number, email, age, blood_type, municipality, availability, status, created_at)
VALUES 
('Christian James Lopez', '09651234577', 'christian.lopez@email.com', 28, 'B+', 'Zamboanga City', 'available', 'pending', NOW() - INTERVAL '1 day'),
('Angelica Rose Aquino', '09751234578', 'angelica.aquino@email.com', 33, 'O+', 'Iloilo City', 'available', 'pending', NOW() - INTERVAL '2 days'),
('Francis Xavier Castillo', '09951234579', 'francis.castillo@email.com', 29, 'A+', 'Bacolod', 'available', 'pending', NOW() - INTERVAL '1 day');

-- 4. Create donor registrations (rejected)
INSERT INTO donor_registrations (full_name, contact_number, email, age, blood_type, municipality, availability, status, reviewed_by, reviewed_at, review_reason, created_at)
VALUES 
('Jasmine Nicole Flores', '09051234580', 'jasmine.flores@email.com', 22, 'B+', 'General Santos', 'available', 'rejected', 1, NOW() - INTERVAL '1 day', 'Incomplete medical history', NOW() - INTERVAL '3 days'),
('Rafael Antonio Morales', '09061234581', 'rafael.morales@email.com', 17, 'O+', 'Bacoor, Cavite', 'available', 'rejected', 1, NOW() - INTERVAL '2 days', 'Does not meet age requirement', NOW() - INTERVAL '4 days');

-- 5. Create donor users (for approved registrations)
INSERT INTO users (full_name, contact_number, email, role, status, theme_preference, created_at)
VALUES 
('Juan Dela Cruz', '09151234567', 'juan.delacruz@email.com', 'donor', 'active', 'light', NOW() - INTERVAL '2 days'),
('Maria Clara Santos', '09161234568', 'maria.santos@email.com', 'donor', 'active', 'dark', NOW() - INTERVAL '3 days'),
('Mark Anthony Bautista', '09171234569', 'mark.bautista@email.com', 'donor', 'active', 'system', NOW() - INTERVAL '1 day'),
('Princess Joy Mendoza', '09261234570', 'princess.mendoza@email.com', 'donor', 'active', 'light', NOW() - INTERVAL '2 days'),
('John Paul Villanueva', '09271234571', 'john.villanueva@email.com', 'donor', 'active', 'dark', NOW() - INTERVAL '1 day'),
('Mary Grace Fernandez', '09351234572', 'mary.fernandez@email.com', 'donor', 'active', 'system', NOW() - INTERVAL '3 days'),
('Angelo Miguel Torres', '09361234573', 'angelo.torres@email.com', 'donor', 'active', 'light', NOW() - INTERVAL '2 days'),
('Kristine Mae Ramos', '09451234574', 'kristine.ramos@email.com', 'donor', 'active', 'dark', NOW() - INTERVAL '1 day'),
('Joshua Emmanuel Cruz', '09551234575', 'joshua.cruz@email.com', 'donor', 'active', 'system', NOW() - INTERVAL '2 days'),
('Angel Faith Gonzales', '09561234576', 'angel.gonzales@email.com', 'donor', 'active', 'light', NOW() - INTERVAL '3 days');

-- 6. Create donor profiles (user_id 2-11, registration_id 1-10)
INSERT INTO donor_profiles (user_id, registration_id, age, blood_type, municipality, availability, created_at)
VALUES 
(2, 1, 28, 'O+', 'Quezon City', 'available', NOW() - INTERVAL '2 days'),
(3, 2, 32, 'A+', 'Manila', 'available', NOW() - INTERVAL '3 days'),
(4, 3, 25, 'B+', 'Cebu City', 'available', NOW() - INTERVAL '1 day'),
(5, 4, 29, 'AB+', 'Davao City', 'available', NOW() - INTERVAL '2 days'),
(6, 5, 35, 'O-', 'Makati', 'available', NOW() - INTERVAL '1 day'),
(7, 6, 27, 'A-', 'Pasig', 'recently_donated', NOW() - INTERVAL '3 days'),
(8, 7, 31, 'B-', 'Taguig', 'available', NOW() - INTERVAL '2 days'),
(9, 8, 26, 'AB-', 'Caloocan', 'unavailable', NOW() - INTERVAL '1 day'),
(10, 9, 30, 'O+', 'Antipolo', 'available', NOW() - INTERVAL '2 days'),
(11, 10, 24, 'A+', 'Cagayan de Oro', 'available', NOW() - INTERVAL '3 days');

-- 7. Create messages
INSERT INTO messages (donor_profile_id, subject, content, is_closed, created_at)
VALUES 
(1, 'Question about donation eligibility', 'Hello admin, I would like to inquire about donation schedule. Thank you!', false, NOW() - INTERVAL '1 day'),
(3, 'Update my contact information', 'Hello admin, I would like to inquire about my donor status. Thank you!', false, NOW() - INTERVAL '2 days'),
(5, 'When is the next blood drive?', 'Hello admin, I would like to inquire about blood drive locations. Thank you!', true, NOW() - INTERVAL '3 days'),
(7, 'I want to donate but have concerns', 'Hello admin, I would like to inquire about eligibility requirements. Thank you!', false, NOW() - INTERVAL '1 day'),
(9, 'Availability update needed', 'Hello admin, I would like to inquire about donation schedule. Thank you!', true, NOW() - INTERVAL '2 days');

-- 8. Create alerts
INSERT INTO alerts (title, message, alert_type, priority, target_audience, send_now, sent_at, created_by, created_at)
VALUES 
('Urgent O+ Blood Needed – Philippine General Hospital', 'We urgently need O+ blood donors for emergency surgery patients at PGH. Please respond if available.', 'urgent_request', 'critical', '{"blood_types": ["O+"], "municipalities": ["Manila", "Quezon City", "Makati"]}', true, NOW() - INTERVAL '1 day', 1, NOW() - INTERVAL '1 day'),
('Red Cross Mobile Blood Drive – Quezon City', 'Join us this Saturday at SM North EDSA for our quarterly blood donation drive. Free snacks and health screening!', 'donation_drive', 'medium', '{"municipalities": ["Quezon City", "Caloocan", "Valenzuela"]}', true, NOW() - INTERVAL '2 days', 1, NOW() - INTERVAL '2 days'),
('AB- Blood Urgently Required – St. Luke''s Medical Center', 'Critical need for AB- blood type. Patient requires immediate transfusion. Contact us ASAP.', 'urgent_request', 'critical', '{"blood_types": ["AB-", "AB+"]}', true, NOW() - INTERVAL '3 days', 1, NOW() - INTERVAL '3 days'),
('Thank You to All Our Donors!', 'We''ve reached 1,000 successful donations this year. Thank you for saving lives!', 'general_announcement', 'low', NULL, true, NOW() - INTERVAL '5 days', 1, NOW() - INTERVAL '5 days'),
('Blood Donation Camp – Cebu City', 'Free blood donation camp at Ayala Center Cebu this weekend. Walk-ins welcome!', 'donation_drive', 'medium', '{"municipalities": ["Cebu City", "Mandaue", "Lapu-Lapu"]}', false, NULL, 1, NOW() - INTERVAL '1 day');

-- 9. Create notifications
INSERT INTO notifications (user_id, title, message, notification_type, is_read, alert_id, created_at)
VALUES 
-- Alert notifications to donors
(2, 'Urgent O+ Blood Needed – Philippine General Hospital', 'We urgently need O+ blood donors for emergency surgery patients at PGH. Please respond if available.', 'alert', false, 1, NOW() - INTERVAL '1 day'),
(10, 'Urgent O+ Blood Needed – Philippine General Hospital', 'We urgently need O+ blood donors for emergency surgery patients at PGH. Please respond if available.', 'alert', true, 1, NOW() - INTERVAL '1 day'),
(2, 'Red Cross Mobile Blood Drive – Quezon City', 'Join us this Saturday at SM North EDSA for our quarterly blood donation drive. Free snacks and health screening!', 'alert', false, 2, NOW() - INTERVAL '2 days'),
(9, 'AB- Blood Urgently Required – St. Luke''s Medical Center', 'Critical need for AB- blood type. Patient requires immediate transfusion. Contact us ASAP.', 'alert', false, 3, NOW() - INTERVAL '3 days'),
(3, 'Thank You to All Our Donors!', 'We''ve reached 1,000 successful donations this year. Thank you for saving lives!', 'alert', true, 4, NOW() - INTERVAL '5 days'),
-- System notifications
(2, 'Welcome to Blood Donor Network!', 'Thank you for registering as a blood donor. Your profile has been approved.', 'system', true, NULL, NOW() - INTERVAL '2 days'),
(3, 'Welcome to Blood Donor Network!', 'Thank you for registering as a blood donor. Your profile has been approved.', 'system', false, NULL, NOW() - INTERVAL '3 days'),
(4, 'Welcome to Blood Donor Network!', 'Thank you for registering as a blood donor. Your profile has been approved.', 'system', true, NULL, NOW() - INTERVAL '1 day');

-- Show summary
SELECT 'Users' as table_name, COUNT(*) as count FROM users
UNION ALL SELECT 'Donor Registrations', COUNT(*) FROM donor_registrations
UNION ALL SELECT 'Donor Profiles', COUNT(*) FROM donor_profiles
UNION ALL SELECT 'Messages', COUNT(*) FROM messages
UNION ALL SELECT 'Alerts', COUNT(*) FROM alerts
UNION ALL SELECT 'Notifications', COUNT(*) FROM notifications;
