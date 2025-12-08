-- =====================================================
-- SCHEMA UPDATE FOR LOAN AND LOCKER LOGIC
-- =====================================================

-- 2. Auto-Close Loan on Zero Balance 
CREATE OR REPLACE TRIGGER close_loan_on_zero_balance 
    AFTER UPDATE OF BALANCE_REMAINING ON LOAN_ACCOUNT 
    FOR EACH ROW 
BEGIN 
    IF :new.BALANCE_REMAINING <= 0 AND :old.BALANCE_REMAINING > 0 THEN 
        UPDATE LOAN_ACCOUNT 
        SET STATUS = 'Closed', 
            ACTUAL_END_DATE = SYSDATE 
        WHERE LOAN_ACCOUNT_ID = :new.LOAN_ACCOUNT_ID; 
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

-- 6. REPAY_INSTALLMENT Procedure 
CREATE OR REPLACE PROCEDURE REPAY_INSTALLMENT( 
    p_loan_account_id INT, 
    p_amount          DECIMAL, 
    p_principal       DECIMAL, 
    p_profit          DECIMAL 
) AS 
BEGIN 
    INSERT INTO LOAN_REPAYMENT ( 
        LOAN_ACCOUNT_ID, AMOUNT_PAID, 
        PRINCIPAL_COMPONENT, PROFIT_COMPONENT 
    ) 
    VALUES ( 
        p_loan_account_id, p_amount, 
        p_principal, p_profit 
    ); 
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
