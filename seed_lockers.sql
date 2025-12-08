-- =====================================================
-- SEED DATA FOR LOCKERS
-- =====================================================
-- Run this script to populate the LOCKER table with available lockers.
-- Assumption: Branch IDs 1, 2, 3 exist (from Banking.schema2.sql).

-- Branch 1 (Main Branch)
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (1, 'L-101', 'Small', 5000, 'Available');
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (1, 'L-102', 'Small', 5000, 'Available');
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (1, 'L-103', 'Medium', 8000, 'Available');
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (1, 'L-104', 'Medium', 8000, 'Available');
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (1, 'L-105', 'Large', 12000, 'Available');

-- Branch 2 (North Branch)
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (2, 'L-201', 'Small', 5000, 'Available');
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (2, 'L-202', 'Medium', 8000, 'Available');

-- Branch 3 (South Branch)
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (3, 'L-301', 'Small', 5000, 'Available');
INSERT INTO LOCKER (BRANCH_ID, LOCKER_NUMBER, LOCKER_SIZE, ANNUAL_FEE, STATUS) VALUES (3, 'L-302', 'Large', 12000, 'Available');

COMMIT;

SELECT 'Locker seed data inserted successfully!' as Status FROM dual;
