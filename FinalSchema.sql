-- =====================================================
-- RETAIL BANKING SCHEMA 
-- =====================================================

-- Drop existing tables if they exist (in correct order due to FK dependencies)
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE LOCKER_RENTAL CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE LOCKER CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE LOAN_REPAYMENT CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE LOAN_ACCOUNT CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE LOAN_APPLICATION CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE LOAN_TYPE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE CARD CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- Drop TRANSACTION first (it might have different name due to previous errors)
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE BANK_TRANSACTION CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE "TRANSACTION" CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ACCOUNT_HOLDER CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ACCOUNT CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ACCOUNT_TYPE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE USER_AUTH CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE CUSTOMER CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE BRANCH CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- Drop sequences
BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE customer_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE user_auth_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE branch_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE account_type_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE account_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE transaction_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE card_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE loan_type_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE loan_application_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE loan_account_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE loan_repayment_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE locker_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE locker_rental_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- =====================================================
-- CREATE SEQUENCES
-- =====================================================

CREATE SEQUENCE customer_seq START WITH 1001 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE user_auth_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE branch_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE account_type_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE account_seq START WITH 50001 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE transaction_seq START WITH 100001 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE card_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE loan_type_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE loan_application_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE loan_account_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE loan_repayment_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE locker_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE locker_rental_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;



-- =====================================================
-- TABLE: CUSTOMER
-- =====================================================
CREATE TABLE CUSTOMER(
     CUSTOMER_ID INT PRIMARY KEY,
     CNIC VARCHAR2(13) NOT NULL UNIQUE CHECK(LENGTH(CNIC) = 13),
     FIRST_NAME VARCHAR2(30) NOT NULL,
     LAST_NAME VARCHAR2(30) NOT NULL,
     DATE_OF_BIRTH DATE NOT NULL,
     AGE INT, --will be calculated by trigger
     PHONE_NUMBER VARCHAR2(15) CHECK (LENGTH(PHONE_NUMBER) = 11), -- Changed to 11 for Pakistani numbers
     ADDRESS VARCHAR2(100),
     EMAIL VARCHAR2(100) UNIQUE
);

-- Create index on EMAIL for faster lookups
CREATE INDEX idx_customer_email ON CUSTOMER(EMAIL);

-- =====================================================
-- TABLE: USER_AUTH
-- =====================================================
CREATE TABLE USER_AUTH(
    USER_ID INT PRIMARY KEY,
    CUSTOMER_ID INT NOT NULL UNIQUE,
    PASSWORD_HASH VARCHAR2(255) NOT NULL,
    STATUS VARCHAR2(20) DEFAULT 'Active' CHECK (STATUS IN ('Active', 'Locked', 'Suspended')),
    CONSTRAINT FK_USER_CUST FOREIGN KEY (CUSTOMER_ID) 
    REFERENCES CUSTOMER(CUSTOMER_ID) ON DELETE CASCADE
);

-- =====================================================
-- TABLE: BRANCH
-- =====================================================
CREATE TABLE BRANCH(
    BRANCH_ID INT PRIMARY KEY,
    BRANCH_NAME VARCHAR2(50) NOT NULL UNIQUE,
    LOCATION VARCHAR2(50)
);

-- =====================================================
-- TABLE: ACCOUNT_TYPE
-- =====================================================
CREATE TABLE ACCOUNT_TYPE(
   TYPE_ID INT PRIMARY KEY,
   TYPE_NAME VARCHAR2(40) NOT NULL UNIQUE,
   MIN_BALANCE DECIMAL(15,2) DEFAULT 0,
   MONTHLY_FEE DECIMAL(10,2) DEFAULT 0
);

-- =====================================================
-- TABLE: ACCOUNT
-- ===========================================
CREATE TABLE ACCOUNT(
   ACCOUNT_ID INT PRIMARY KEY,
   BRANCH_ID INT NOT NULL,
   TYPE_ID INT NOT NULL,
   ACCOUNT_NUMBER VARCHAR2(20) NOT NULL UNIQUE,
   BALANCE DECIMAL(15,2) DEFAULT 0 CHECK (BALANCE >= 0),
   ACCOUNT_MODE VARCHAR2(20) CHECK (ACCOUNT_MODE IN ('Individual', 'Joint')),
   STATUS VARCHAR2(20) DEFAULT 'Active' CHECK (STATUS IN ('Active', 'Dormant', 'Frozen', 'Closed')),
   OPENED_DATE DATE DEFAULT SYSDATE,
   CONSTRAINT FK_ACC_BRANCH FOREIGN KEY (BRANCH_ID) 
   REFERENCES BRANCH(BRANCH_ID),
   CONSTRAINT FK_ACC_TYPE FOREIGN KEY (TYPE_ID) 
   REFERENCES ACCOUNT_TYPE(TYPE_ID)
);

-- =====================================================
-- TABLE: ACCOUNT_HOLDER (Bridge Table of CUSTOMER and ACCOUNT)
-- =====================================================
CREATE TABLE ACCOUNT_HOLDER(
   ACCOUNT_ID INT,
   CUSTOMER_ID INT,
   HOLDER_TYPE VARCHAR2(25) NOT NULL CHECK (HOLDER_TYPE IN ('Primary', 'Secondary', 'Joint')),
   CONSTRAINT AH_PK PRIMARY KEY (ACCOUNT_ID, CUSTOMER_ID),
   CONSTRAINT FK_AH_ACC FOREIGN KEY (ACCOUNT_ID) 
   REFERENCES ACCOUNT(ACCOUNT_ID) ON DELETE CASCADE,
   CONSTRAINT FK_AH_CUST FOREIGN KEY (CUSTOMER_ID) 
   REFERENCES CUSTOMER(CUSTOMER_ID) ON DELETE CASCADE
);

-- =====================================================
-- TABLE: TRANSACTION
-- ===================================================
CREATE TABLE BANK_TRANSACTION(
   TRANSACTION_ID INT PRIMARY KEY,
   ACCOUNT_ID INT NOT NULL,
   RECIPIENT_ACCOUNT_ID INT NOT NULL,
   RECIPIENT_ACCOUNT_NAME VARCHAR2(100) NOT NULL,
   TRANSACTION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   AMOUNT DECIMAL(15,2) NOT NULL CHECK (AMOUNT > 0),
   TRANSACTION_TYPE VARCHAR2(20) NOT NULL CHECK (TRANSACTION_TYPE IN ('Deposit', 'Transfer', 'Fee', 'Withdrawal')), -- Added Withdrawal
   TRANSACTION_MODE VARCHAR2(30) CHECK (TRANSACTION_MODE IN ('Cash', 'Cheque', 'Online', 'Mobile')), -- Changed from MODE
   BALANCE_REMAINING DECIMAL(15,2) NOT NULL,
   CONSTRAINT FK_TRN_ACC FOREIGN KEY (ACCOUNT_ID) 
   REFERENCES ACCOUNT(ACCOUNT_ID) ON DELETE CASCADE
);
-- =====================================================
-- TABLE: CARD
-- ===================================================
CREATE TABLE CARD(
   CARD_ID INT PRIMARY KEY,
   ACCOUNT_ID INT NOT NULL,
   CARD_NUMBER VARCHAR2(16) NOT NULL UNIQUE CHECK(LENGTH(CARD_NUMBER) = 16),
   CARD_TYPE VARCHAR2(20) NOT NULL CHECK (CARD_TYPE IN ('Debit', 'Credit', 'Prepaid')),
   ISSUED_DATE DATE DEFAULT SYSDATE,
   EXPIRY_DATE DATE NOT NULL,
   STATUS VARCHAR2(20) DEFAULT 'Active' CHECK (STATUS IN ('Active', 'Blocked', 'Expired', 'Lost', 'Stolen')),
   DAILY_LIMIT DECIMAL(10,2) CHECK (DAILY_LIMIT > 0),
   CONSTRAINT FK_CARD_ACC FOREIGN KEY (ACCOUNT_ID) 
   REFERENCES ACCOUNT(ACCOUNT_ID) ON DELETE CASCADE,
   CONSTRAINT CHK_CARD_EXPIRY CHECK (EXPIRY_DATE > ISSUED_DATE)
);
-- =====================================================
-- TABLE: LOAN_TYPE
-- ===================================================
CREATE TABLE LOAN_TYPE(
   LOAN_TYPE_ID INT PRIMARY KEY,
   TYPE_NAME VARCHAR2(40) NOT NULL UNIQUE CHECK (TYPE_NAME IN ('Housing', 'Car')),
   PROFIT_RATE DECIMAL(5,2) NOT NULL CHECK (PROFIT_RATE > 0),
   MAX_DURATION_MONTHS INT NOT NULL CHECK (MAX_DURATION_MONTHS > 0),
   MIN_AMOUNT DECIMAL(15,2),
   MAX_AMOUNT DECIMAL(15,2)
);
-- =====================================================
-- TABLE: LOAN APPLICATION
-- ===================================================
CREATE TABLE LOAN_APPLICATION(
   APPLICATION_ID INT PRIMARY KEY,
   CUSTOMER_ID INT NOT NULL,
   BRANCH_ID INT NOT NULL,
   LOAN_TYPE_ID INT NOT NULL,
   REQUESTED_AMOUNT DECIMAL(15,2) NOT NULL CHECK (REQUESTED_AMOUNT > 0),
   STATUS VARCHAR2(30) DEFAULT 'Pending' CHECK (STATUS IN ('Pending', 'Under Review', 'Approved', 'Rejected')),
   APPLICATION_DATE DATE DEFAULT SYSDATE,
   EVALUATION_DATE DATE,
   CONSTRAINT FK_LAPP_CUST FOREIGN KEY (CUSTOMER_ID) 
   REFERENCES CUSTOMER(CUSTOMER_ID),
   CONSTRAINT FK_LAPP_BRANCH FOREIGN KEY (BRANCH_ID) 
   REFERENCES BRANCH(BRANCH_ID),
   CONSTRAINT FK_LAPP_TYPE FOREIGN KEY (LOAN_TYPE_ID) 
   REFERENCES LOAN_TYPE(LOAN_TYPE_ID)
);

-- =====================================================
-- TABLE: LOCKER
-- ===================================================
CREATE TABLE LOCKER(
   LOCKER_ID INT PRIMARY KEY,
   BRANCH_ID INT NOT NULL,
   LOCKER_NUMBER VARCHAR2(20) NOT NULL,
   LOCKER_SIZE VARCHAR2(20) CHECK (LOCKER_SIZE IN ('Small', 'Medium', 'Large')),
   ANNUAL_FEE DECIMAL(10,2),
   STATUS VARCHAR2(30) DEFAULT 'Available' CHECK (STATUS IN ('Available', 'Occupied', 'Under Maintenance')),  
   CONSTRAINT FK_LOCKER_BRANCH FOREIGN KEY (BRANCH_ID) 
   REFERENCES BRANCH(BRANCH_ID),
   CONSTRAINT UQ_LOCKER_NUM UNIQUE (BRANCH_ID, LOCKER_NUMBER)
);

-- =====================================================
-- TABLE: LOCKER_RENTAL
-- ===================================================
CREATE TABLE LOCKER_RENTAL(
   RENTAL_ID INT PRIMARY KEY,
   LOCKER_ID INT NOT NULL,
   ACCOUNT_ID INT NOT NULL,
   START_DATE DATE DEFAULT SYSDATE,
   END_DATE DATE NOT NULL,
   STATUS VARCHAR2(20) DEFAULT 'Active' CHECK (STATUS IN ('Active', 'Expired', 'Cancelled')),
   CONSTRAINT FK_RENTAL_LOCKER FOREIGN KEY (LOCKER_ID) 
   REFERENCES LOCKER(LOCKER_ID),
   CONSTRAINT FK_RENTAL_ACC FOREIGN KEY (ACCOUNT_ID) 
   REFERENCES ACCOUNT(ACCOUNT_ID) ON DELETE CASCADE,
   CONSTRAINT CHK_RENTAL_DATES CHECK (END_DATE > START_DATE)
);

-- =====================================================
-- CREATE TRIGGERS 
-- =====================================================

-- Auto-increment trigger
CREATE OR REPLACE TRIGGER customer_bir
    BEFORE INSERT ON CUSTOMER FOR EACH ROW
BEGIN
    IF :new.CUSTOMER_ID IS NULL THEN
        SELECT customer_seq.NEXTVAL INTO :new.CUSTOMER_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER user_auth_bir
    BEFORE INSERT ON USER_AUTH FOR EACH ROW
BEGIN
    IF :new.USER_ID IS NULL THEN
        SELECT user_auth_seq.NEXTVAL INTO :new.USER_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER branch_bir
    BEFORE INSERT ON BRANCH FOR EACH ROW
BEGIN
    IF :new.BRANCH_ID IS NULL THEN
        SELECT branch_seq.NEXTVAL INTO :new.BRANCH_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER account_type_bir
    BEFORE INSERT ON ACCOUNT_TYPE FOR EACH ROW
BEGIN
    IF :new.TYPE_ID IS NULL THEN
        SELECT account_type_seq.NEXTVAL INTO :new.TYPE_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER account_bir
    BEFORE INSERT ON ACCOUNT FOR EACH ROW
BEGIN
    IF :new.ACCOUNT_ID IS NULL THEN
        SELECT account_seq.NEXTVAL INTO :new.ACCOUNT_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER transaction_bir
    BEFORE INSERT ON BANK_TRANSACTION FOR EACH ROW
BEGIN
    IF :new.TRANSACTION_ID IS NULL THEN
        SELECT transaction_seq.NEXTVAL INTO :new.TRANSACTION_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER card_bir
    BEFORE INSERT ON CARD FOR EACH ROW
BEGIN
    IF :new.CARD_ID IS NULL THEN
        SELECT card_seq.NEXTVAL INTO :new.CARD_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER loan_type_bir
    BEFORE INSERT ON LOAN_TYPE FOR EACH ROW
BEGIN
    IF :new.LOAN_TYPE_ID IS NULL THEN
        SELECT loan_type_seq.NEXTVAL INTO :new.LOAN_TYPE_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER loan_application_bir
    BEFORE INSERT ON LOAN_APPLICATION FOR EACH ROW
BEGIN
    IF :new.APPLICATION_ID IS NULL THEN
        SELECT loan_application_seq.NEXTVAL INTO :new.APPLICATION_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER loan_account_bir
    BEFORE INSERT ON LOAN_ACCOUNT FOR EACH ROW
BEGIN
    IF :new.LOAN_ACCOUNT_ID IS NULL THEN
        SELECT loan_account_seq.NEXTVAL INTO :new.LOAN_ACCOUNT_ID FROM dual;
    END IF;
END;
/

/

CREATE OR REPLACE TRIGGER locker_bir
    BEFORE INSERT ON LOCKER FOR EACH ROW
BEGIN
    IF :new.LOCKER_ID IS NULL THEN
        SELECT locker_seq.NEXTVAL INTO :new.LOCKER_ID FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER locker_rental_bir
    BEFORE INSERT ON LOCKER_RENTAL FOR EACH ROW
BEGIN
    IF :new.RENTAL_ID IS NULL THEN
        SELECT locker_rental_seq.NEXTVAL INTO :new.RENTAL_ID FROM dual;
    END IF;
END;
/

-- Business Logic Triggers
CREATE OR REPLACE TRIGGER calculate_age_trigger
    BEFORE INSERT OR UPDATE OF DATE_OF_BIRTH ON CUSTOMER
    FOR EACH ROW
BEGIN
    :new.AGE := TRUNC(MONTHS_BETWEEN(SYSDATE, :new.DATE_OF_BIRTH) / 12);
END;
/

CREATE OR REPLACE TRIGGER generate_account_number
    BEFORE INSERT ON ACCOUNT
    FOR EACH ROW
BEGIN
    IF :new.ACCOUNT_NUMBER IS NULL THEN
        SELECT 'ACC' || TO_CHAR(account_seq.NEXTVAL) 
        INTO :new.ACCOUNT_NUMBER FROM dual;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER generate_card_number
    BEFORE INSERT ON CARD
    FOR EACH ROW
BEGIN
    IF :new.CARD_NUMBER IS NULL THEN
        SELECT LPAD(card_seq.NEXTVAL, 16, '0') 
        INTO :new.CARD_NUMBER FROM dual;
    END IF;
END;
/

/

-- =====================================================
-- INSERT SAMPLE DATA 
-- =====================================================

--  Branches
INSERT INTO BRANCH (BRANCH_NAME, LOCATION) VALUES ('Main Branch', 'City Center');
INSERT INTO BRANCH (BRANCH_NAME, LOCATION) VALUES ('North Branch', 'North Area');
INSERT INTO BRANCH (BRANCH_NAME, LOCATION) VALUES ('South Branch', 'South Area');

--  Account Types
INSERT INTO ACCOUNT_TYPE (TYPE_NAME, MIN_BALANCE, MONTHLY_FEE) 
VALUES ('Savings Account', 1000, 0);
INSERT INTO ACCOUNT_TYPE (TYPE_NAME, MIN_BALANCE, MONTHLY_FEE) 
VALUES ('Current Account', 5000, 100);
INSERT INTO ACCOUNT_TYPE (TYPE_NAME, MIN_BALANCE, MONTHLY_FEE) 
VALUES ('Islamic Account', 2000, 0);

--  Loan Types
INSERT INTO LOAN_TYPE (TYPE_NAME, PROFIT_RATE, MAX_DURATION_MONTHS, MIN_AMOUNT, MAX_AMOUNT)
VALUES ('Housing', 5.5, 360, 500000, 50000000);
INSERT INTO LOAN_TYPE (TYPE_NAME, PROFIT_RATE, MAX_DURATION_MONTHS, MIN_AMOUNT, MAX_AMOUNT)
VALUES ('Car', 7.2, 60, 500000, 5000000);

--  10 Customers (with ages over 18)
INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('1234567890123', 'Ahmed', 'Khan', TO_DATE('1990-01-15', 'YYYY-MM-DD'), '03001234567', 'House 1, Street 2, Karachi', 'ahmed.khan@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('2345678901234', 'Fatima', 'Ali', TO_DATE('1985-05-20', 'YYYY-MM-DD'), '03011234568', 'House 3, Street 4, Lahore', 'fatima.ali@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('3456789012345', 'Usman', 'Malik', TO_DATE('1982-08-10', 'YYYY-MM-DD'), '03021234569', 'House 5, Street 6, Islamabad', 'usman.malik@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('4567890123456', 'Ayesha', 'Rehman', TO_DATE('1988-12-05', 'YYYY-MM-DD'), '03031234570', 'House 7, Street 8, Rawalpindi', 'ayesha.rehman@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('5678901234567', 'Bilal', 'Ahmed', TO_DATE('1985-03-25', 'YYYY-MM-DD'), '03041234571', 'House 9, Street 10, Faisalabad', 'bilal.ahmed@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('6789012345678', 'Sara', 'Khan', TO_DATE('1991-07-14', 'YYYY-MM-DD'), '03051234572', 'House 11, Street 12, Peshawar', 'sara.khan@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('7890123456789', 'Omar', 'Shah', TO_DATE('1987-11-30', 'YYYY-MM-DD'), '03061234573', 'House 13, Street 14, Quetta', 'omar.shah@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('8901234567890', 'Zainab', 'Hussain', TO_DATE('1983-04-18', 'YYYY-MM-DD'), '03071234574', 'House 15, Street 16, Multan', 'zainab.hussain@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('9012345678901', 'Kamran', 'Butt', TO_DATE('1979-09-22', 'YYYY-MM-DD'), '03081234575', 'House 17, Street 18, Gujranwala', 'kamran.butt@example.com');

INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL) 
VALUES ('0123456789012', 'Nadia', 'Akhtar', TO_DATE('1984-06-08', 'YYYY-MM-DD'), '03091234576', 'House 19, Street 20, Sialkot', 'nadia.akhtar@example.com');

-- Insert User Auth for customers (using actual customer IDs that were generated)
INSERT INTO USER_AUTH (CUSTOMER_ID, PASSWORD_HASH, STATUS) 
SELECT CUSTOMER_ID, '$2b$12$p/8tjQynfnXRPujl1wCzI.siIYrqdfMxsl0JqWtZnG9Ws8lJip14S', 'Active' 
FROM CUSTOMER;

COMMIT;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Verify tables were created
SELECT table_name FROM user_tables ORDER BY table_name;

-- Verify customer data with ages
SELECT CUSTOMER_ID, FIRST_NAME, LAST_NAME, CNIC, AGE FROM CUSTOMER;

-- Verify user auth data
SELECT u.USER_ID, c.FIRST_NAME, c.LAST_NAME, u.STATUS 
FROM USER_AUTH u 
JOIN CUSTOMER c ON u.CUSTOMER_ID = c.CUSTOMER_ID;

SELECT 'Retail Banking Schema setup completed successfully!' AS status FROM dual;

-- =====================================================
-- SCHEMA UPDATE FOR LOAN AND LOCKER LOGIC
-- =====================================================

-- 2. Auto-Close Loan on Zero Balance 
CREATE OR REPLACE TRIGGER close_loan_when_balance_zero
AFTER UPDATE OF BALANCE ON ACCOUNT
FOR EACH ROW
DECLARE
    v_customer_id NUMBER;
BEGIN
    -- Only run when balance becomes zero (was greater before)
    IF :new.BALANCE = 0 AND :old.BALANCE > 0 THEN

        -- Get customer ID
        SELECT CUSTOMER_ID 
        INTO v_customer_id
        FROM ACCOUNT_HOLDER
        WHERE ACCOUNT_ID = :new.ACCOUNT_ID
          AND HOLDER_TYPE = 'Primary';

        -- Update ONLY PENDING or APPROVED loan applications
        UPDATE LOAN_APPLICATION
        SET STATUS = 'Closed',
            EVALUATION_DATE = SYSDATE
        WHERE CUSTOMER_ID = v_customer_id
          AND STATUS IN ('Pending', 'Under Review', 'Approved');
    END IF;

END;
/
-- 3. Locker Status Management Triggers 

-- 3A. Mark locker as Occupied: 
CREATE OR REPLACE TRIGGER locker_set_occupied 
    AFTER INSERT ON LOCKER_RENTAL 
    FOR EACH ROW 
BEGIN 
    UPDATE LOCKER 
    SET STATUS = 'Occupied' 
    WHERE LOCKER_ID = :new.LOCKER_ID; 
END; 
/

-- 3B. Mark locker as Available: 
CREATE OR REPLACE TRIGGER locker_set_available 
    AFTER UPDATE OF STATUS ON LOCKER_RENTAL 
    FOR EACH ROW 
BEGIN 
    IF :new.STATUS IN ('Expired', 'Cancelled') THEN 
        UPDATE LOCKER 
        SET STATUS = 'Available' 
        WHERE LOCKER_ID = :new.LOCKER_ID; 
    END IF; 
END; 
/

-- 5. APPLY_LOAN Procedure 
CREATE OR REPLACE PROCEDURE APPLY_LOAN( 
    p_customer_id INT, 
    p_branch_id   INT, 
    p_type_id     INT, 
    p_amount      DECIMAL 
) AS 
BEGIN 
    INSERT INTO LOAN_APPLICATION (CUSTOMER_ID, BRANCH_ID, LOAN_TYPE_ID, REQUESTED_AMOUNT) 
    VALUES (p_customer_id, p_branch_id, p_type_id, p_amount); 
END; 
/



-- 7. RENT_LOCKER Procedure 
CREATE OR REPLACE PROCEDURE RENT_LOCKER( 
    p_locker_id  INT, 
    p_account_id INT, 
    p_end_date   DATE 
) AS 
BEGIN 
    INSERT INTO LOCKER_RENTAL (LOCKER_ID, ACCOUNT_ID, END_DATE) 
    VALUES (p_locker_id, p_account_id, p_end_date); 
END; 
/

COMMIT;

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


CREATE OR REPLACE PROCEDURE CREATE_USER (
    p_full_name       IN VARCHAR2,
    p_email           IN VARCHAR2,
    p_password        IN VARCHAR2,
    p_cnic            IN VARCHAR2 DEFAULT NULL,
    p_phone           IN VARCHAR2 DEFAULT NULL,
    p_address         IN VARCHAR2 DEFAULT NULL,
    p_dob             IN DATE DEFAULT NULL,
    p_card_number     IN VARCHAR2 DEFAULT NULL,
    p_initial_balance IN NUMBER DEFAULT 50000,
    p_user_id         OUT NUMBER
)
AS
    v_customer_id   NUMBER;
    v_user_id       NUMBER;
    v_account_id    NUMBER;
    v_branch_id     NUMBER;
    v_type_id       NUMBER;
    v_first_name    VARCHAR2(50);
    v_last_name     VARCHAR2(50);

    -- Local variables (we can assign to these)
    v_cnic          VARCHAR2(20);
    v_phone         VARCHAR2(20);
    v_address       VARCHAR2(200);
    v_dob           DATE;
    v_card          VARCHAR2(30);
BEGIN
    ----------------------------------------------------
    -- Name split
    ----------------------------------------------------
    v_first_name := REGEXP_SUBSTR(p_full_name, '^\S+');
    v_last_name  := NVL(REGEXP_SUBSTR(p_full_name, '\s(.+)$', 1, 1), '');

    ----------------------------------------------------
    -- Default CNIC
    ----------------------------------------------------
    IF p_cnic IS NULL THEN
        v_cnic := TO_CHAR(TRUNC(DBMS_RANDOM.VALUE(1000000000000, 9999999999999)));
    ELSE
        v_cnic := p_cnic;
    END IF;

    ----------------------------------------------------
    -- Default DOB = 18 years ago
    ----------------------------------------------------
    IF p_dob IS NULL THEN
        v_dob := ADD_MONTHS(SYSDATE, -216);
    ELSE
        v_dob := p_dob;
    END IF;

    ----------------------------------------------------
    -- Clean / default phone
    ----------------------------------------------------
    IF p_phone IS NULL THEN
        v_phone := '03000000000';
    ELSE
        v_phone := REGEXP_REPLACE(p_phone, '[^0-9]', '');
    END IF;

    ----------------------------------------------------
    -- Default address
    ----------------------------------------------------
    v_address := NVL(p_address, 'Not provided');

    ----------------------------------------------------
    -- Auto-generate card number
    ----------------------------------------------------
    IF p_card_number IS NULL THEN
        v_card := TO_CHAR(TRUNC(DBMS_RANDOM.VALUE(1000000000000000, 9999999999999999)));
    ELSE
        v_card := p_card_number;
    END IF;

    ----------------------------------------------------
    -- Get default branch
    ----------------------------------------------------
    SELECT BRANCH_ID INTO v_branch_id
    FROM BRANCH WHERE ROWNUM = 1;

    ----------------------------------------------------
    -- Get Savings Account type
    ----------------------------------------------------
    SELECT TYPE_ID INTO v_type_id
    FROM ACCOUNT_TYPE WHERE TYPE_NAME = 'Savings Account';

    ----------------------------------------------------
    -- Insert CUSTOMER
    ----------------------------------------------------
    INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL)
    VALUES (v_cnic, v_first_name, v_last_name, v_dob, v_phone, v_address, p_email)
    RETURNING CUSTOMER_ID INTO v_customer_id;

    ----------------------------------------------------
    -- Insert USER_AUTH
    ----------------------------------------------------
    INSERT INTO USER_AUTH (CUSTOMER_ID, PASSWORD_HASH, STATUS)
    VALUES (v_customer_id, p_password, 'Active')
    RETURNING USER_ID INTO v_user_id;

    ----------------------------------------------------
    -- Insert ACCOUNT
    ----------------------------------------------------
    INSERT INTO ACCOUNT (BRANCH_ID, TYPE_ID, BALANCE, ACCOUNT_MODE, STATUS)
    VALUES (v_branch_id, v_type_id, p_initial_balance, 'Individual', 'Active')
    RETURNING ACCOUNT_ID INTO v_account_id;

    ----------------------------------------------------
    -- Insert ACCOUNT_HOLDER
    ----------------------------------------------------
    INSERT INTO ACCOUNT_HOLDER (ACCOUNT_ID, CUSTOMER_ID, HOLDER_TYPE)
    VALUES (v_account_id, v_customer_id, 'Primary');

    ----------------------------------------------------
    -- Insert CARD
    ----------------------------------------------------
    INSERT INTO CARD (ACCOUNT_ID, CARD_NUMBER, CARD_TYPE, EXPIRY_DATE, STATUS, DAILY_LIMIT)
    VALUES (v_account_id, v_card, 'Debit', ADD_MONTHS(SYSDATE, 60), 'Active', 100000);

    p_user_id := v_user_id;
END;
/

CREATE OR REPLACE PROCEDURE UPDATE_BALANCE (
    p_user_id IN NUMBER,
    p_new_balance IN NUMBER
)
AS
BEGIN
    UPDATE ACCOUNT a
    SET a.BALANCE = p_new_balance
    WHERE a.ACCOUNT_ID = (
        SELECT ah.ACCOUNT_ID
        FROM ACCOUNT_HOLDER ah
        JOIN USER_AUTH ua 
            ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
        WHERE ua.USER_ID = p_user_id AND ah.HOLDER_TYPE='Primary'
    );
END;
/
CREATE OR REPLACE PROCEDURE ADD_BALANCE (
    p_user_id IN NUMBER,
    p_amount IN NUMBER
)
AS
BEGIN
    UPDATE ACCOUNT a
    SET a.BALANCE = a.BALANCE + p_amount
    WHERE a.ACCOUNT_ID = (
        SELECT ah.ACCOUNT_ID
        FROM ACCOUNT_HOLDER ah
        JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
        WHERE ua.USER_ID = p_user_id AND ah.HOLDER_TYPE='Primary'
    );
END;
/
CREATE OR REPLACE PROCEDURE SUB_BALANCE (
    p_user_id IN NUMBER,
    p_amount IN NUMBER
)
AS
BEGIN
    UPDATE ACCOUNT a
    SET a.BALANCE = a.BALANCE - p_amount
    WHERE a.ACCOUNT_ID = (
        SELECT ah.ACCOUNT_ID
        FROM ACCOUNT_HOLDER ah
        JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
        WHERE ua.USER_ID = p_user_id AND ah.HOLDER_TYPE='Primary'
    );
END;
CREATE OR REPLACE PROCEDURE CREATE_TRANSACTION (
    p_user_id            IN NUMBER,
    p_recipient_name     IN VARCHAR2,
    p_recipient_card     IN VARCHAR2,
    p_amount             IN NUMBER,
    p_type               IN VARCHAR2,
    p_transaction_id     OUT NUMBER
)
AS
    v_sender_acc       NUMBER;
    v_rec_acc          NUMBER;
    v_balance          NUMBER;
    v_clean_card       VARCHAR2(30);
    v_db_name          VARCHAR2(200);
    v_norm_db_name     VARCHAR2(200);
    v_norm_input_name  VARCHAR2(200);
BEGIN
    ----------------------------------------------------
    -- Clean card number
    ----------------------------------------------------
    v_clean_card := REGEXP_REPLACE(p_recipient_card, '[^0-9]', '');

    ----------------------------------------------------
    -- Get sender account
    ----------------------------------------------------
    SELECT a.ACCOUNT_ID, a.BALANCE 
    INTO v_sender_acc, v_balance
    FROM ACCOUNT a
    JOIN ACCOUNT_HOLDER ah ON a.ACCOUNT_ID = ah.ACCOUNT_ID
    JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
    WHERE ua.USER_ID = p_user_id
      AND ah.HOLDER_TYPE = 'Primary';

    ----------------------------------------------------
    -- If DEPOSIT, sender = receiver
    ----------------------------------------------------
    IF UPPER(p_type) = 'DEPOSIT' THEN
        v_rec_acc := v_sender_acc;

    ELSE
        ----------------------------------------------------
        -- Get recipient details
        ----------------------------------------------------
        SELECT c.ACCOUNT_ID,
               cust.FIRST_NAME || ' ' || cust.LAST_NAME
        INTO v_rec_acc, v_db_name
        FROM CARD c
        JOIN ACCOUNT_HOLDER ah ON c.ACCOUNT_ID = ah.ACCOUNT_ID
        JOIN CUSTOMER cust ON cust.CUSTOMER_ID = ah.CUSTOMER_ID
        WHERE REGEXP_REPLACE(c.CARD_NUMBER, '[^0-9]', '') = v_clean_card
          AND c.STATUS = 'Active';

        ----------------------------------------------------
        -- Normalize both names (REMOVE spaces, LOWERCASE)
        ----------------------------------------------------
        v_norm_db_name :=
            LOWER(REPLACE(REGEXP_REPLACE(v_db_name, '\s+', ''), ' ', ''));

        v_norm_input_name :=
            LOWER(REPLACE(REGEXP_REPLACE(TRIM(p_recipient_name), '\s+', ''), ' ', ''));

        ----------------------------------------------------
        -- Validate name (SUPER FLEXIBLE NOW)
        ----------------------------------------------------
        IF v_norm_input_name IS NULL OR LENGTH(v_norm_input_name) < 2 THEN
            RAISE_APPLICATION_ERROR(-20002, 'Invalid recipient name.');
        END IF;

        IF INSTR(v_norm_db_name, v_norm_input_name) = 0 THEN
            RAISE_APPLICATION_ERROR(-20002,
                'Recipient card name does not match.');
        END IF;

    END IF;

    ----------------------------------------------------
    -- Insert Transaction
    ----------------------------------------------------
    INSERT INTO BANK_TRANSACTION (
        ACCOUNT_ID,
        RECIPIENT_ACCOUNT_ID,
        RECIPIENT_ACCOUNT_NAME,
        AMOUNT,
        TRANSACTION_TYPE,
        TRANSACTION_MODE,
        BALANCE_REMAINING
    )
    VALUES (
        v_sender_acc,
        v_rec_acc,
        p_recipient_name,
        p_amount,
        p_type,
        'Online',
        CASE 
            WHEN UPPER(p_type) = 'DEPOSIT' THEN v_balance + p_amount
            ELSE v_balance - p_amount
        END
    )
    RETURNING TRANSACTION_ID INTO p_transaction_id;
   COMMIT;
END;
/



select *from customer;
select *from card;
select *from bank_transaction;
-- CHECK your rentals first
SELECT * FROM LOCKER_RENTAL;
UPDATE LOCKER_RENTAL
SET START_DATE = DATE '2020-01-01',
    END_DATE   = DATE '2025-12-09'
WHERE RENTAL_ID = 5;

COMMIT;

UPDATE LOCKER_RENTAL
SET STATUS = 'Expired'
WHERE END_DATE <= SYSDATE 
  AND STATUS = 'Active';

COMMIT;


CREATE TABLE EXPIRED_RENTAL_QUEUE (
    RENTAL_ID NUMBER PRIMARY KEY
);

CREATE OR REPLACE TRIGGER trg_collect_expired_rentals
AFTER UPDATE OF STATUS ON LOCKER_RENTAL
FOR EACH ROW
WHEN (NEW.STATUS = 'Expired')
BEGIN
    INSERT INTO EXPIRED_RENTAL_QUEUE (RENTAL_ID)
    VALUES (:NEW.RENTAL_ID);
END;
/
CREATE OR REPLACE TRIGGER trg_cleanup_expired_rentals
AFTER UPDATE ON LOCKER_RENTAL
BEGIN
    -- Make the locker available again
    UPDATE LOCKER
    SET STATUS = 'Available'
    WHERE LOCKER_ID IN (
        SELECT LOCKER_ID
        FROM LOCKER_RENTAL
        WHERE RENTAL_ID IN (SELECT RENTAL_ID FROM EXPIRED_RENTAL_QUEUE)
    );

    -- Delete expired rentals
    DELETE FROM LOCKER_RENTAL
    WHERE RENTAL_ID IN (SELECT RENTAL_ID FROM EXPIRED_RENTAL_QUEUE);

    -- Clear temp queue
    DELETE FROM EXPIRED_RENTAL_QUEUE;
END;
/
select *from customer;
select *from card;

