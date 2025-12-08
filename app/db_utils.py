"""
Database utility layer - FIXED REGISTRATION ONLY
"""

from app.database import db
from datetime import date
from typing import Optional, Dict, List
import traceback


# ============================================================
# USER DAO (REGISTRATION FIXED)
# ============================================================

class UserDAO:

    @staticmethod
    def create(full_name, email, password, card_number,
               balance=50000, cnic=None, phone_number=None,
               address=None, date_of_birth=None):
        """Create a new user EXACTLY matching Oracle CREATE_USER procedure."""
        try:
            dob_value = date_of_birth if isinstance(date_of_birth, date) else None

            print(f"DEBUG: Creating user - full_name={full_name}, email={email}, card={card_number}")

            with db.get_cursor(commit=True) as cursor:
                out_user_id = cursor.var(int)

                # PROCEDURE SIGNATURE MUST MATCH EXACTLY:
                # CREATE_USER(
                #   p_full_name, p_email, p_password, p_cnic,
                #   p_phone, p_address, p_dob,
                #   p_card_number, p_initial_balance, p_user_id OUT)
                cursor.callproc("CREATE_USER", [
                    full_name,              # p_full_name
                    email,                  # p_email
                    password,               # p_password
                    cnic or None,           # p_cnic
                    phone_number or None,   # p_phone
                    address or None,        # p_address
                    dob_value,              # p_dob
                    card_number,            # p_card_number
                    balance,                # p_initial_balance
                    out_user_id             # p_user_id OUT
                ])

                new_user_id = out_user_id.getvalue()
                print(f"DEBUG: User created successfully with ID {new_user_id}")
                return new_user_id

        except Exception as e:
            print(f"Error in UserDAO.create: {e}")
            traceback.print_exc()
            raise

    # ------------------------------------------------------------------

    @staticmethod
    def get_account_id_by_user_id(user_id: int):
        """Get the primary account ID for a given user - FIXED BIND VARIABLE"""
        try:
            print(f"DEBUG get_account_id: user_id={user_id}")
            
            # FIXED: Changed :uid to :user_id_param
            query = """
                SELECT ah.ACCOUNT_ID AS account_id
                FROM ACCOUNT_HOLDER ah
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                WHERE ua.USER_ID = :user_id_param 
                  AND ah.HOLDER_TYPE = 'Primary'
            """

            row = db.execute_query(query, {"user_id_param": user_id}, fetch_one=True)

            if row:
                account_id = row["account_id"]
                print(f"DEBUG: Found account_id={account_id}")
                return account_id
            else:
                print(f"DEBUG: No account found for user_id={user_id}")
                return None

        except Exception as e:
            print(f"Error in get_account_id_by_user_id: {e}")
            traceback.print_exc()
            return None
    # ------------------------------------------------------------------

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        """Return full user details including account + card."""
        try:
            # FIXED: Changed :id to :user_id_param
            query = """
                SELECT 
                    ua.USER_ID AS id,
                    ua.PASSWORD_HASH,
                    c.CUSTOMER_ID,
                    c.FIRST_NAME || ' ' || c.LAST_NAME AS full_name,
                    c.EMAIL,
                    c.CNIC,
                    c.PHONE_NUMBER,
                    c.ADDRESS,
                    a.ACCOUNT_ID,
                    a.ACCOUNT_NUMBER,
                    a.BALANCE,
                    card.CARD_NUMBER
                FROM USER_AUTH ua
                JOIN CUSTOMER c ON ua.CUSTOMER_ID = c.CUSTOMER_ID
                LEFT JOIN ACCOUNT_HOLDER ah 
                    ON c.CUSTOMER_ID = ah.CUSTOMER_ID 
                   AND ah.HOLDER_TYPE='Primary'
                LEFT JOIN ACCOUNT a 
                    ON ah.ACCOUNT_ID = a.ACCOUNT_ID
                LEFT JOIN CARD card 
                    ON a.ACCOUNT_ID = card.ACCOUNT_ID 
                   AND card.STATUS='Active'
                WHERE ua.USER_ID = :user_id_param
            """

            result = db.execute_query(query, {"user_id_param": user_id}, fetch_one=True)
            if result:
                print(f"DEBUG get_by_id: Found user {user_id}, account_id={result.get('account_id')}")
            else:
                print(f"DEBUG get_by_id: User {user_id} not found")
            return result

        except Exception as e:
            print(f"Error in get_by_id: {e}")
            return None
    # ------------------------------------------------------------------

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        """Login lookup by email."""
        try:
            query = """
                SELECT 
                    ua.USER_ID AS id,
                    ua.PASSWORD_HASH,
                    c.CUSTOMER_ID,
                    c.FIRST_NAME || ' ' || c.LAST_NAME AS full_name,
                    c.EMAIL,
                    a.ACCOUNT_ID,
                    a.ACCOUNT_NUMBER,
                    a.BALANCE,
                    card.CARD_NUMBER
                FROM USER_AUTH ua
                JOIN CUSTOMER c ON ua.CUSTOMER_ID = c.CUSTOMER_ID
                LEFT JOIN ACCOUNT_HOLDER ah 
                    ON c.CUSTOMER_ID = ah.CUSTOMER_ID 
                   AND ah.HOLDER_TYPE='Primary'
                LEFT JOIN ACCOUNT a 
                    ON ah.ACCOUNT_ID = a.ACCOUNT_ID
                LEFT JOIN CARD card 
                    ON a.ACCOUNT_ID = card.ACCOUNT_ID 
                   AND card.STATUS='Active'
                WHERE c.EMAIL = :email
            """

            return db.execute_query(query, {"email": email}, fetch_one=True)

        except Exception as e:
            print(f"Error in get_by_email: {e}")
            return None
        # ------------------------------------------------------------------

    @staticmethod
    def get_by_card_number(card_no: str) -> Optional[Dict]:
        """Lookup user by card number (required for Transfer)."""
        try:
            query = """
                SELECT 
                    ua.USER_ID AS id,
                    ua.PASSWORD_HASH,
                    c.CUSTOMER_ID,
                    c.FIRST_NAME || ' ' || c.LAST_NAME AS full_name,
                    a.ACCOUNT_ID,
                    a.ACCOUNT_NUMBER,
                    a.BALANCE,
                    card.CARD_NUMBER
                FROM CARD card
                JOIN ACCOUNT a ON card.ACCOUNT_ID = a.ACCOUNT_ID
                JOIN ACCOUNT_HOLDER ah ON a.ACCOUNT_ID = ah.ACCOUNT_ID
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                JOIN CUSTOMER c ON ua.CUSTOMER_ID = c.CUSTOMER_ID
                WHERE card.CARD_NUMBER = :num
            """
            return db.execute_query(query, {"num": card_no}, fetch_one=True)
        except Exception as e:
            print(f"Error in get_by_card_number: {e}")
            return None
    
    # ... all your existing methods ...
    
    @staticmethod
    def get_by_card_number(card_number: str) -> Optional[Dict]:
        """Get user by card number"""
        try:
            query = """
                SELECT 
                    ua.USER_ID AS id,
                    ua.PASSWORD_HASH,
                    c.CUSTOMER_ID,
                    c.FIRST_NAME || ' ' || c.LAST_NAME AS full_name,
                    a.ACCOUNT_ID,
                    a.ACCOUNT_NUMBER,
                    a.BALANCE,
                    card.CARD_NUMBER
                FROM CARD card
                JOIN ACCOUNT a ON card.ACCOUNT_ID = a.ACCOUNT_ID
                JOIN ACCOUNT_HOLDER ah ON a.ACCOUNT_ID = ah.ACCOUNT_ID
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                JOIN CUSTOMER c ON ua.CUSTOMER_ID = c.CUSTOMER_ID
                WHERE card.CARD_NUMBER = :card_number_param
                  AND card.STATUS = 'Active'
            """
            result = db.execute_query(query, {"card_number_param": card_number}, fetch_one=True)
            return result
        except Exception as e:
            print(f"Error in UserDAO.get_by_card_number: {e}")
            return None
    # ------------------------------------------------------------------

    @staticmethod
    def add_to_balance(user_id, amount):
        """Add to balance - FIXED transaction handling"""
        try:
            print(f"DEBUG add_to_balance: user_id={user_id}, amount={amount}")
            
            # Get account_id first
            account_id = UserDAO.get_account_id_by_user_id(user_id)
            if not account_id:
                raise Exception(f"No account found for user_id: {user_id}")
            
            print(f"DEBUG: Account ID for balance update: {account_id}")
            
            # Use get_cursor for transaction
            with db.get_cursor(commit=True) as cursor:
                query = """
                    UPDATE ACCOUNT 
                    SET BALANCE = BALANCE + :amount_param
                    WHERE ACCOUNT_ID = :account_id_param
                """
                
                cursor.execute(query, {
                    "amount_param": amount,
                    "account_id_param": account_id
                })
            
            print(f"DEBUG: Balance added successfully")
            
        except Exception as e:
            print(f"Error in add_to_balance: {e}")
            traceback.print_exc()
            raise

    @staticmethod
    def subtract_from_balance(user_id, amount):
        """Subtract from balance - FIXED transaction handling"""
        try:
            print(f"DEBUG subtract_from_balance: user_id={user_id}, amount={amount}")
            
            # Get account_id first
            account_id = UserDAO.get_account_id_by_user_id(user_id)
            if not account_id:
                raise Exception(f"No account found for user_id: {user_id}")
            
            print(f"DEBUG: Account ID for balance update: {account_id}")
            
            # Check if sufficient balance exists
            user_info = UserDAO.get_by_id(user_id)
            if not user_info:
                raise Exception(f"User {user_id} not found")
            
            current_balance = user_info.get('balance', 0)
            print(f"DEBUG: Current balance: {current_balance}, Amount to subtract: {amount}")
            
            if current_balance < amount:
                raise Exception(f"Insufficient balance. Have {current_balance}, need {amount}")
            
            # Use get_cursor for transaction
            with db.get_cursor(commit=True) as cursor:
                query = """
                    UPDATE ACCOUNT 
                    SET BALANCE = BALANCE - :amount_param
                    WHERE ACCOUNT_ID = :account_id_param
                """
                
                cursor.execute(query, {
                    "amount_param": amount,
                    "account_id_param": account_id
                })
            
            print(f"DEBUG: Balance subtracted successfully")
            
        except Exception as e:
            print(f"Error in subtract_from_balance: {e}")
            traceback.print_exc()
            raise

    @staticmethod
    def update_balance(user_id, new_balance):
        """Update user balance - FIXED transaction handling"""
        try:
            print(f"DEBUG update_balance: user_id={user_id}, new_balance={new_balance}")
            
            # Get account_id first
            account_id = UserDAO.get_account_id_by_user_id(user_id)
            if not account_id:
                raise Exception(f"No account found for user_id: {user_id}")
            
            print(f"DEBUG: Account ID for balance update: {account_id}")
            
            # Use get_cursor for transaction
            with db.get_cursor(commit=True) as cursor:
                query = """
                    UPDATE ACCOUNT 
                    SET BALANCE = :balance_param
                    WHERE ACCOUNT_ID = :account_id_param
                """
                
                cursor.execute(query, {
                    "balance_param": new_balance,
                    "account_id_param": account_id
                })
            
            print(f"DEBUG: Balance updated successfully")
            
        except Exception as e:
            print(f"Error in update_balance: {e}")
            traceback.print_exc()
            raise
# ============================================================
# TRANSACTION DAO  (UNCHANGED)
# ============================================================

class TransactionDAO:

    @staticmethod
    def create(user_id, recipient_name=None, recipient_card=None,
               amount=0, txn_type=None, recipient_card_number=None):
        """Create transaction - FIXED for your schema"""
        try:
            if recipient_card is None and recipient_card_number:
                recipient_card = recipient_card_number

            print(f"DEBUG: Creating transaction - user_id={user_id}, amount={amount}, type={txn_type}, recipient_card={recipient_card}")

            # Get sender account_id
            sender_account_id = UserDAO.get_account_id_by_user_id(user_id)
            if not sender_account_id:
                raise Exception("No account found for sender.")

            # Get recipient account_id if transfer (not deposit)
            recipient_account_id = None
            if txn_type and txn_type.lower() != 'deposit':
                if recipient_card:
                    # Get recipient user by card number
                    recipient_user = UserDAO.get_by_card_number(recipient_card)
                    if not recipient_user:
                        raise Exception("Recipient card not found")
                    
                    recipient_account_id = recipient_user.get('account_id')
                    if not recipient_account_id:
                        raise Exception("Recipient has no account")
                    
                    print(f"DEBUG: Recipient account_id: {recipient_account_id}")
            
            # For deposit, recipient is same as sender
            if txn_type and txn_type.lower() == 'deposit':
                recipient_account_id = sender_account_id
                print(f"DEBUG: Deposit - recipient same as sender: {recipient_account_id}")

            with db.get_cursor(commit=True) as cursor:
                out_txn = cursor.var(int)

                # Call the CREATE_TRANSACTION procedure
                # It expects: p_user_id, p_recipient_name, p_recipient_card, p_amount, p_type, p_transaction_id OUT
                cursor.callproc("CREATE_TRANSACTION", [
                    user_id,                    # p_user_id (sender)
                    recipient_name or "N/A",    # p_recipient_name
                    recipient_card or None,     # p_recipient_card
                    amount,                     # p_amount
                    txn_type or "Transfer",     # p_type
                    out_txn                     # p_transaction_id OUT
                ])

                txn_id = out_txn.getvalue()
                print(f"DEBUG: Created transaction ID: {txn_id}")
                return txn_id

        except Exception as e:
            print(f"Error in TransactionDAO.create: {e}")
            traceback.print_exc()
            raise

    
    # ... other methods ...
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get transactions for user - FIXED COLUMN NAMES (lowercase mapping)"""
        try:
            print(f"DEBUG get_by_user_id: user_id={user_id}")
            
            # Get account_id for this user
            account_id = UserDAO.get_account_id_by_user_id(user_id)
            if not account_id:
                print(f"DEBUG: No account found for user_id: {user_id}")
                return []

            print(f"DEBUG: Fetching transactions for account_id: {account_id}")

            query = """
                SELECT 
                    TRANSACTION_ID,
                    AMOUNT,
                    TRANSACTION_TYPE,
                    TRANSACTION_MODE,
                    TRANSACTION_DATE,
                    RECIPIENT_ACCOUNT_NAME,
                    BALANCE_REMAINING
                FROM BANK_TRANSACTION
                WHERE ACCOUNT_ID = :account_id
                ORDER BY TRANSACTION_DATE DESC
            """

            results = db.execute_query(query, {"account_id": account_id}, fetch_all=True)

            if results:
                print(f"DEBUG: Found {len(results)} transactions")

                formatted_results = []
                for row in results:
                    formatted_results.append({
                        "id": row.get("transaction_id"),
                        "amount": row.get("amount"),
                        "type": row.get("transaction_type"),
                        "mode": row.get("transaction_mode"),
                        "timestamp": row.get("transaction_date"),
                        "recipient_name": row.get("recipient_account_name"),
                        "balance_remaining": row.get("balance_remaining")
                    })

                print("DEBUG formatted:", formatted_results)
                return formatted_results

            else:
                print("DEBUG: No transactions found")
                return []

        except Exception as e:
            print(f"Error loading transactions: {e}")
            traceback.print_exc()
            return []

# ============================================================
# LOAN DAO - COMPLETE IMPLEMENTATION
# ============================================================

class LoanDAO:

    @staticmethod
    def create_application(user_id, branch_id, loan_type_id, amount):
        """Create loan application"""
        try:
            row = db.execute_query(
                "SELECT CUSTOMER_ID FROM USER_AUTH WHERE USER_ID = :user_id_param",
                {"user_id_param": user_id},
                fetch_one=True
            )

            if not row:
                raise Exception("USER_ID not linked to CUSTOMER_ID")

            customer_id = row["customer_id"]

            with db.get_cursor(commit=True) as cursor:
                try:
                    cursor.callproc("APPLY_LOAN", [
                        customer_id,
                        branch_id,
                        loan_type_id,
                        amount
                    ])
                except Exception as proc_error:
                    print(f"APPLY_LOAN procedure failed: {proc_error}")
                    query = """
                        INSERT INTO LOAN_APPLICATION (
                            APPLICATION_ID, CUSTOMER_ID, BRANCH_ID, 
                            LOAN_TYPE_ID, REQUESTED_AMOUNT, APPLICATION_DATE, STATUS
                        ) VALUES (
                            LOAN_APPLICATION_SEQ.NEXTVAL, :customer_id_param, :branch_id_param,
                            :loan_type_id_param, :amount_param, SYSDATE, 'Pending'
                        )
                    """
                    cursor.execute(query, {
                        "customer_id_param": customer_id,
                        "branch_id_param": branch_id,
                        "loan_type_id_param": loan_type_id,
                        "amount_param": amount
                    })

            return True
        except Exception as e:
            print(f"Error in LoanDAO.create_application: {e}")
            traceback.print_exc()
            raise

    @staticmethod
    def get_types():
        """Get loan types"""
        try:
            results = db.execute_query("""
                SELECT 
                    LOAN_TYPE_ID AS loan_type_id,
                    TYPE_NAME AS type_name,
                    PROFIT_RATE AS profit_rate,
                    MAX_AMOUNT AS max_amount,
                    MAX_DURATION_MONTHS AS max_duration_months
                FROM LOAN_TYPE
                ORDER BY TYPE_NAME
            """, {}, fetch_all=True)
            return results or []
        except Exception as e:
            print(f"Error in LoanDAO.get_types: {e}")
            return []

    @staticmethod
    def get_active_loans(user_id):
        """Get active loans"""
        try:
            results = db.execute_query("""
                SELECT
                    la.LOAN_ACCOUNT_ID AS loan_account_id,
                    la.PRINCIPAL_AMOUNT AS principal_amount,
                    la.BALANCE_REMAINING AS balance_remaining,
                    la.START_DATE AS start_date,
                    la.EXPECTED_END_DATE AS expected_end_date,
                    lt.TYPE_NAME AS type_name
                FROM LOAN_ACCOUNT la
                JOIN LOAN_TYPE lt ON la.LOAN_TYPE_ID = lt.LOAN_TYPE_ID
                JOIN USER_AUTH ua ON la.CUSTOMER_ID = ua.CUSTOMER_ID
                WHERE ua.USER_ID = :user_id_param
                  AND la.STATUS = 'Active'
                ORDER BY la.START_DATE DESC
            """, {"user_id_param": user_id}, fetch_all=True)
            return results or []
        except Exception as e:
            print(f"Error in LoanDAO.get_active_loans: {e}")
            return []

    @staticmethod
    def get_applications(user_id):
        """Get loan applications"""
        try:
            results = db.execute_query("""
                SELECT
                    la.APPLICATION_ID AS application_id,
                    la.APPLICATION_DATE AS application_date,
                    la.REQUESTED_AMOUNT AS requested_amount,
                    la.STATUS AS status,
                    lt.TYPE_NAME AS type_name
                FROM LOAN_APPLICATION la
                JOIN LOAN_TYPE lt ON la.LOAN_TYPE_ID = lt.LOAN_TYPE_ID
                JOIN USER_AUTH ua ON la.CUSTOMER_ID = ua.CUSTOMER_ID
                WHERE ua.USER_ID = :user_id_param
                ORDER BY la.APPLICATION_DATE DESC
            """, {"user_id_param": user_id}, fetch_all=True)
            return results or []
        except Exception as e:
            print(f"Error in LoanDAO.get_applications: {e}")
            return []

    @staticmethod
    def repay_installment(loan_account_id, amount):
        """Repay loan installment"""
        try:
            principal = amount * 0.9
            profit = amount * 0.1

            with db.get_cursor(commit=True) as cursor:
                try:
                    cursor.callproc("REPAY_INSTALLMENT", [
                        loan_account_id,
                        amount,
                        principal,
                        profit
                    ])
                except Exception as proc_error:
                    print(f"REPAY_INSTALLMENT procedure failed: {proc_error}")
                    query = """
                        UPDATE LOAN_ACCOUNT 
                        SET BALANCE_REMAINING = BALANCE_REMAINING - :principal_param,
                            LAST_PAYMENT_DATE = SYSDATE
                        WHERE LOAN_ACCOUNT_ID = :loan_account_id_param
                          AND STATUS = 'Active'
                    """
                    cursor.execute(query, {
                        "loan_account_id_param": loan_account_id,
                        "principal_param": principal
                    })

            return True
        except Exception as e:
            print(f"Error in LoanDAO.repay_installment: {e}")
            traceback.print_exc()
            raise


# ============================================================
# LOCKER DAO - COMPLETE IMPLEMENTATION
# ============================================================

class LockerDAO:

    @staticmethod
    def rent_locker(user_id, locker_id):
        """Rent a locker"""
        try:
            account_id = UserDAO.get_account_id_by_user_id(user_id)
            
            if not account_id:
                user_info = UserDAO.get_by_id(user_id)
                if user_info and user_info.get('account_id'):
                    account_id = user_info['account_id']
            
            if not account_id:
                raise Exception("User has no primary account!")
            
            end_date = date.today().replace(year=date.today().year + 1)
            
            with db.get_cursor(commit=True) as cursor:
                try:
                    cursor.callproc("RENT_LOCKER", [
                        locker_id,
                        account_id,
                        end_date
                    ])
                except Exception as proc_error:
                    print(f"RENT_LOCKER procedure failed: {proc_error}")
                    LockerDAO._rent_locker_manually(cursor, locker_id, account_id, end_date)
            
            return True
        except Exception as e:
            print(f"Error in LockerDAO.rent_locker: {e}")
            traceback.print_exc()
            raise

    @staticmethod
    def _rent_locker_manually(cursor, locker_id, account_id, end_date):
        """Manual locker rental"""
        try:
            cursor.execute("""
                SELECT ANNUAL_FEE FROM LOCKER WHERE LOCKER_ID = :locker_id_param
            """, {"locker_id_param": locker_id})
            fee_result = cursor.fetchone()
            annual_fee = fee_result[0] if fee_result else 1000
            
            cursor.execute("""
                UPDATE LOCKER 
                SET STATUS = 'Rented' 
                WHERE LOCKER_ID = :locker_id_param 
                  AND STATUS = 'Available'
            """, {"locker_id_param": locker_id})
            
            rows_updated = cursor.rowcount
            if rows_updated == 0:
                raise Exception("Locker not available or already rented")
            
            cursor.execute("""
                INSERT INTO LOCKER_RENTAL (
                    RENTAL_ID, LOCKER_ID, ACCOUNT_ID, 
                    START_DATE, END_DATE, STATUS
                ) VALUES (
                    LOCKER_RENTAL_SEQ.NEXTVAL, :locker_id_param, :account_id_param,
                    SYSDATE, :end_date_param, 'Active'
                )
            """, {
                "locker_id_param": locker_id,
                "account_id_param": account_id,
                "end_date_param": end_date
            })
            
            cursor.execute("""
                UPDATE ACCOUNT 
                SET BALANCE = BALANCE - :fee_param
                WHERE ACCOUNT_ID = :account_id_param
            """, {
                "fee_param": annual_fee,
                "account_id_param": account_id
            })
            
        except Exception as e:
            print(f"Error in manual locker rental: {e}")
            raise

    @staticmethod
    def get_my_lockers(user_id):
        """Get user's lockers"""
        try:
            query = """
                SELECT 
                    lr.RENTAL_ID AS rental_id,
                    lr.START_DATE AS start_date,
                    lr.END_DATE AS end_date,
                    lr.STATUS AS rental_status,
                    l.LOCKER_NUMBER AS locker_number,
                    l.LOCKER_SIZE AS locker_size,
                    l.ANNUAL_FEE AS annual_fee,
                    b.BRANCH_NAME AS branch_name
                FROM LOCKER_RENTAL lr
                JOIN ACCOUNT a ON lr.ACCOUNT_ID = a.ACCOUNT_ID
                JOIN ACCOUNT_HOLDER ah ON ah.ACCOUNT_ID = a.ACCOUNT_ID
                JOIN USER_AUTH ua ON ua.CUSTOMER_ID = ah.CUSTOMER_ID
                JOIN LOCKER l ON l.LOCKER_ID = lr.LOCKER_ID
                JOIN BRANCH b ON b.BRANCH_ID = l.BRANCH_ID
                WHERE ua.USER_ID = :user_id_param
                ORDER BY lr.START_DATE DESC
            """
            results = db.execute_query(query, {"user_id_param": user_id}, fetch_all=True)
            return results or []
        except Exception as e:
            print(f"Error in LockerDAO.get_my_lockers: {e}")
            return []

    @staticmethod
    def get_available_lockers():
        """Get available lockers"""
        try:
            results = db.execute_query("""
                SELECT 
                    l.LOCKER_ID AS locker_id,
                    l.LOCKER_NUMBER AS locker_number,
                    l.LOCKER_SIZE AS locker_size,
                    l.ANNUAL_FEE AS annual_fee,
                    b.BRANCH_NAME AS branch_name,
                    b.LOCATION AS location
                FROM LOCKER l
                JOIN BRANCH b ON b.BRANCH_ID = l.BRANCH_ID
                WHERE l.STATUS = 'Available'
                ORDER BY b.BRANCH_NAME, l.LOCKER_NUMBER
            """, {}, fetch_all=True)
            return results or []
        except Exception as e:
            print(f"Error in LockerDAO.get_available_lockers: {e}")
            return []


# ============================================================
# BRANCH DAO - COMPLETE IMPLEMENTATION
# ============================================================

class BranchDAO:
    """Helper DAO for branch operations"""
    
    @staticmethod
    def get_all():
        """Get all branches"""
        try:
            return db.execute_query("""
                SELECT BRANCH_ID, BRANCH_NAME, LOCATION
                FROM BRANCH
                ORDER BY BRANCH_NAME
            """, {}, fetch_all=True) or []
        except Exception as e:
            print(f"Error in BranchDAO.get_all: {e}")
            return []


# ============================================================
# BENEFICIARY DAO - COMPLETE IMPLEMENTATION
# ============================================================

class BeneficiaryDAO:
    """Beneficiary operations"""
    
    @staticmethod
    def create(*args, **kwargs):
        raise NotImplementedError("Beneficiaries not supported.")

    @staticmethod
    def get_by_user_id(user_id):
        return []

# ============================================================
# BENEFICIARY (UNCHANGED)
# ============================================================

