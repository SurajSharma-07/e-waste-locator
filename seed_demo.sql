USE ewaste_locator;

-- IMPORTANT:
-- These are DEMONSTRATION records only.
-- They are intentionally marked Pending and are NOT claims that these
-- facilities are certified/authorized. Replace them with verified records
-- from an authoritative source before presenting the project as real data.

INSERT INTO facilities
(name, address, city, state, pincode, latitude, longitude, contact, email,
 operating_hours, accepted_categories, verification_status, verification_source,
 last_verified, website, notes)
VALUES
('Demo E-Waste Facility A',
 'Demo Address 1, Mumbai',
 'Mumbai', 'Maharashtra', '400001',
 18.9388, 72.8354, '0000000000', 'demo@example.com',
 'Mon-Sat, 10:00 AM-6:00 PM',
 'Mobile Phones,Laptops,Computers,Batteries,Appliances',
 'Pending', 'Replace with authoritative verification source', NULL, NULL,
 'Demo record for development/testing only.'),

('Demo E-Waste Facility B',
 'Demo Address 2, Mumbai',
 'Mumbai', 'Maharashtra', '400050',
 19.0607, 72.8362, '0000000000', 'demo2@example.com',
 'Mon-Fri, 9:00 AM-5:00 PM',
 'Mobile Phones,Computers,Appliances',
 'Pending', 'Replace with authoritative verification source', NULL, NULL,
 'Demo record for development/testing only.'),

('Demo E-Waste Facility C',
 'Demo Address 3, Thane',
 'Thane', 'Maharashtra', '400601',
 19.2183, 72.9781, '0000000000', 'demo3@example.com',
 'Mon-Sat, 10:00 AM-6:00 PM',
 'Laptops,Batteries,Appliances',
 'Pending', 'Replace with authoritative verification source', NULL, NULL,
 'Demo record for development/testing only.');
