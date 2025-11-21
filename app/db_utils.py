"""
Database utility functions for CRUD operations
"""
from app.database import db
from datetime import datetime, date
from typing import Optional, List, Dict, Any

class UserDAO:
    """Data Access Object for User operations - maps to CUSTOMER + USER_AUTH + ACCOUNT + CARD"""
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        query = """
            SELECT 
                ua.USER_ID as id,
                c.CUSTOMER_ID,
                c.FIRST_NAME || ' ' || c.LAST_NAME as full_name,
                c.FIRST_NAME,
                c.LAST_NAME,
                c.EMAIL,
                c.CNIC,
                c.PHONE_NUMBER,
                c.ADDRESS,
                ua.PASSWORD_HASH as password,
                ua.STATUS as auth_status,
                a.ACCOUNT_ID,
                a.ACCOUNT_NUMBER,
                a.BALANCE as balance,
                a.STATUS as account_status,
                card.CARD_NUMBER as card_number,
                card.CARD_ID,
                card.CARD_TYPE,
                card.STATUS as card_status
            FROM USER_AUTH ua
            JOIN CUSTOMER c ON ua.CUSTOMER_ID = c.CUSTOMER_ID
            LEFT JOIN ACCOUNT_HOLDER ah ON c.CUSTOMER_ID = ah.CUSTOMER_ID AND ah.HOLDER_TYPE = 'Primary'
            LEFT JOIN ACCOUNT a ON ah.ACCOUNT_ID = a.ACCOUNT_ID
            LEFT JOIN CARD card ON a.ACCOUNT_ID = card.ACCOUNT_ID AND card.STATUS = 'Active'
            WHERE ua.USER_ID = :user_id
        """
        return db.execute_query(query, {'user_id': user_id}, fetch_one=True)
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        query = """
            SELECT 
                ua.USER_ID as id,
                c.CUSTOMER_ID,
                c.FIRST_NAME || ' ' || c.LAST_NAME as full_name,
                c.FIRST_NAME,
                c.LAST_NAME,
                c.EMAIL,
                c.CNIC,
                c.PHONE_NUMBER,
                c.ADDRESS,
                ua.PASSWORD_HASH as password,
                ua.STATUS as auth_status,
                a.ACCOUNT_ID,
                a.ACCOUNT_NUMBER,
                a.BALANCE as balance,
                a.STATUS as account_status,
                card.CARD_NUMBER as card_number,
                card.CARD_ID,
                card.CARD_TYPE,
                card.STATUS as card_status
            FROM USER_AUTH ua
            JOIN CUSTOMER c ON ua.CUSTOMER_ID = c.CUSTOMER_ID
            LEFT JOIN ACCOUNT_HOLDER ah ON c.CUSTOMER_ID = ah.CUSTOMER_ID AND ah.HOLDER_TYPE = 'Primary'
            LEFT JOIN ACCOUNT a ON ah.ACCOUNT_ID = a.ACCOUNT_ID
            LEFT JOIN CARD card ON a.ACCOUNT_ID = card.ACCOUNT_ID AND card.STATUS = 'Active'
            WHERE c.EMAIL = :email
        """
        return db.execute_query(query, {'email': email}, fetch_one=True)
    
    @staticmethod
    def get_by_card_number(card_number: str) -> Optional[Dict]:
        query = """
            SELECT 
                ua.USER_ID as id,
                c.CUSTOMER_ID,
                c.FIRST_NAME || ' ' || c.LAST_NAME as full_name,
                c.FIRST_NAME,
                c.LAST_NAME,
                c.EMAIL,
                c.CNIC,
                c.PHONE_NUMBER,
                c.ADDRESS,
                ua.PASSWORD_HASH as password,
                ua.STATUS as auth_status,
                a.ACCOUNT_ID,
                a.ACCOUNT_NUMBER,
                a.BALANCE as balance,
                a.STATUS as account_status,
                card.CARD_NUMBER as card_number,
                card.CARD_ID,
                card.CARD_TYPE,
                card.STATUS as card_status
            FROM USER_AUTH ua
            JOIN CUSTOMER c ON ua.CUSTOMER_ID = c.CUSTOMER_ID
            LEFT JOIN ACCOUNT_HOLDER ah ON c.CUSTOMER_ID = ah.CUSTOMER_ID AND ah.HOLDER_TYPE = 'Primary'
            LEFT JOIN ACCOUNT a ON ah.ACCOUNT_ID = a.ACCOUNT_ID
            LEFT JOIN CARD card ON a.ACCOUNT_ID = card.ACCOUNT_ID
            WHERE card.CARD_NUMBER = :card_number
        """
        return db.execute_query(query, {'card_number': card_number}, fetch_one=True)
    
    @staticmethod
    def create(full_name: str, email: str, password: str, card_number: str, balance: float = 50000.00, 
               cnic: str = None, phone_number: str = None, address: str = None, 
               date_of_birth: date = None) -> int:
        
        connection = db.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""SELECT BRANCH_ID FROM BRANCH WHERE ROWNUM = 1 ORDER BY BRANCH_ID""")
            branch_row = cursor.fetchone()
            if not branch_row:
                raise Exception("No branch found. Please ensure branches are created in the database.")
            branch_id = branch_row[0]
            
            cursor.execute(""" SELECT TYPE_ID FROM ACCOUNT_TYPE WHERE TYPE_NAME = 'Savings Account'""")
            account_type_row = cursor.fetchone()
            if not account_type_row:
                raise Exception("No 'Savings Account' type found. Please ensure account types are created.")
            account_type_id = account_type_row[0]
            
            name_parts = full_name.strip().split(' ', 1)
            first_name = name_parts[0] if name_parts else full_name
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            if not cnic:
                import random
                cnic = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            
            if not date_of_birth:
                from datetime import timedelta
                date_of_birth = date.today() - timedelta(days=365*18)
            if phone_number:
                phone_number = phone_number.replace(' ', '').replace('-', '')
                if len(phone_number) != 11 or not phone_number.isdigit():
                    raise ValueError("Phone number must be exactly 11 digits")
            else:
                phone_number = '03000000000'
            
            # 1. Create CUSTOMER
            customer_id_var = cursor.var(int)
            cursor.execute("""
                INSERT INTO CUSTOMER (CNIC, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, PHONE_NUMBER, ADDRESS, EMAIL)
                VALUES (:cnic, :first_name, :last_name, :date_of_birth, :phone_number, :address, :email)
                RETURNING CUSTOMER_ID INTO :customer_id
            """, {
                'cnic': cnic,
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': date_of_birth,
                'phone_number': phone_number,
                'address': address or 'Not provided',
                'email': email,
                'customer_id': customer_id_var
            })
            customer_id = customer_id_var.getvalue()[0]
            
            # 2. Create USER_AUTH
            user_id_var = cursor.var(int)
            cursor.execute("""
                INSERT INTO USER_AUTH (CUSTOMER_ID, PASSWORD_HASH, STATUS)
                VALUES (:customer_id, :password_hash, 'Active')
                RETURNING USER_ID INTO :user_id
            """, {
                'customer_id': customer_id,
                'password_hash': password,
                'user_id': user_id_var
            })
            user_id = user_id_var.getvalue()[0]
            
            # 3. Create ACCOUNT (trigger will generate ACCOUNT_NUMBER)
            account_id_var = cursor.var(int)
            cursor.execute("""
                INSERT INTO ACCOUNT (BRANCH_ID, TYPE_ID, BALANCE, ACCOUNT_MODE, STATUS)
                VALUES (:branch_id, :type_id, :balance, 'Individual', 'Active')
                RETURNING ACCOUNT_ID INTO :account_id
            """, {
                'branch_id': branch_id,
                'type_id': account_type_id,
                'balance': balance,
                'account_id': account_id_var
            })
            account_id = account_id_var.getvalue()[0]
            
            # Get the generated account number
            cursor.execute("""
                SELECT ACCOUNT_NUMBER FROM ACCOUNT WHERE ACCOUNT_ID = :account_id
            """, {'account_id': account_id})
            account_number = cursor.fetchone()[0]
            
            # 4. Create ACCOUNT_HOLDER (Primary)
            cursor.execute("""
                INSERT INTO ACCOUNT_HOLDER (ACCOUNT_ID, CUSTOMER_ID, HOLDER_TYPE)
                VALUES (:account_id, :customer_id, 'Primary')
            """, {
                'account_id': account_id,
                'customer_id': customer_id
            })
            
            # 5. Create CARD (trigger will generate card number if NULL, but we provide one)
            # Calculate expiry date (5 years from now)
            from datetime import timedelta
            expiry_date = date.today() + timedelta(days=365*5)
            
            card_id_var = cursor.var(int)
            cursor.execute("""
                INSERT INTO CARD (ACCOUNT_ID, CARD_NUMBER, CARD_TYPE, EXPIRY_DATE, STATUS, DAILY_LIMIT)
                VALUES (:account_id, :card_number, 'Debit', :expiry_date, 'Active', 100000)
                RETURNING CARD_ID INTO :card_id
            """, {
                'account_id': account_id,
                'card_number': card_number,
                'expiry_date': expiry_date,
                'card_id': card_id_var
            })
            
            connection.commit()
            return user_id
        except Exception as e:
            connection.rollback()
            raise Exception(f"User creation failed: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def update_balance(user_id: int, new_balance: float):
        """Update account balance for user"""
        query = """
            UPDATE ACCOUNT a
            SET a.BALANCE = :balance
            WHERE a.ACCOUNT_ID = (
                SELECT ah.ACCOUNT_ID 
                FROM ACCOUNT_HOLDER ah
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                WHERE ua.USER_ID = :user_id AND ah.HOLDER_TYPE = 'Primary'
            )
        """
        db.execute_update(query, {'balance': new_balance, 'user_id': user_id})
    
    @staticmethod
    def add_to_balance(user_id: int, amount: float):
        """Add amount to user's account balance"""
        query = """
            UPDATE ACCOUNT a
            SET a.BALANCE = a.BALANCE + :amount
            WHERE a.ACCOUNT_ID = (
                SELECT ah.ACCOUNT_ID 
                FROM ACCOUNT_HOLDER ah
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                WHERE ua.USER_ID = :user_id AND ah.HOLDER_TYPE = 'Primary'
            )
        """
        db.execute_update(query, {'amount': amount, 'user_id': user_id})
    
    @staticmethod
    def subtract_from_balance(user_id: int, amount: float):
        """Subtract amount from user's account balance"""
        query = """
            UPDATE ACCOUNT a
            SET a.BALANCE = a.BALANCE - :amount
            WHERE a.ACCOUNT_ID = (
                SELECT ah.ACCOUNT_ID 
                FROM ACCOUNT_HOLDER ah
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                WHERE ua.USER_ID = :user_id AND ah.HOLDER_TYPE = 'Primary'
            )
        """
        db.execute_update(query, {'amount': amount, 'user_id': user_id})
    
    @staticmethod
    def get_account_id_by_user_id(user_id: int) -> Optional[int]:
        """Get account ID for a user"""
        query = """
            SELECT ah.ACCOUNT_ID
            FROM ACCOUNT_HOLDER ah
            JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
            WHERE ua.USER_ID = :user_id AND ah.HOLDER_TYPE = 'Primary'
        """
        result = db.execute_query(query, {'user_id': user_id}, fetch_one=True)
        return result['account_id'] if result else None
    
    @staticmethod
    def ensure_account_and_card(user_id: int, balance: float = 50000.00):
        """
        Ensure that a user has an account and card. If they don't exist, create them.
        This is useful for existing customers who only have CUSTOMER and USER_AUTH records.
        """
        connection = db.get_connection()
        cursor = connection.cursor()
        try:
            # Check if user already has an account
            account_check = """
                SELECT ah.ACCOUNT_ID, a.ACCOUNT_NUMBER
                FROM ACCOUNT_HOLDER ah
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                JOIN ACCOUNT a ON ah.ACCOUNT_ID = a.ACCOUNT_ID
                WHERE ua.USER_ID = :user_id AND ah.HOLDER_TYPE = 'Primary'
            """
            cursor.execute(account_check, {'user_id': user_id})
            account_row = cursor.fetchone()
            
            if account_row:
                # Account exists, check for card
                account_id = account_row[0]
                card_check = """
                    SELECT CARD_ID, CARD_NUMBER
                    FROM CARD
                    WHERE ACCOUNT_ID = :account_id AND STATUS = 'Active'
                """
                cursor.execute(card_check, {'account_id': account_id})
                card_row = cursor.fetchone()
                
                if not card_row:
                    # Account exists but no card, create one
                    import random
                    from datetime import timedelta
                    card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
                    expiry_date = date.today() + timedelta(days=365*5)
                    
                    card_id_var = cursor.var(int)
                    cursor.execute("""
                        INSERT INTO CARD (ACCOUNT_ID, CARD_NUMBER, CARD_TYPE, EXPIRY_DATE, STATUS, DAILY_LIMIT)
                        VALUES (:account_id, :card_number, 'Debit', :expiry_date, 'Active', 100000)
                        RETURNING CARD_ID INTO :card_id
                    """, {
                        'account_id': account_id,
                        'card_number': card_number,
                        'expiry_date': expiry_date,
                        'card_id': card_id_var
                    })
                connection.commit()
                return
            else:
                # No account exists, create account and card
                # Get customer_id
                cursor.execute("""
                    SELECT CUSTOMER_ID FROM USER_AUTH WHERE USER_ID = :user_id
                """, {'user_id': user_id})
                customer_row = cursor.fetchone()
                if not customer_row:
                    raise Exception("Customer not found for user_id")
                customer_id = customer_row[0]
                
                # Get default branch and account type
                cursor.execute("""
                    SELECT BRANCH_ID FROM BRANCH WHERE ROWNUM = 1 ORDER BY BRANCH_ID
                """)
                branch_row = cursor.fetchone()
                if not branch_row:
                    raise Exception("No branch found. Please ensure branches are created in the database.")
                branch_id = branch_row[0]
                
                cursor.execute("""
                    SELECT TYPE_ID FROM ACCOUNT_TYPE WHERE TYPE_NAME = 'Savings Account'
                """)
                account_type_row = cursor.fetchone()
                if not account_type_row:
                    raise Exception("No 'Savings Account' type found. Please ensure account types are created.")
                account_type_id = account_type_row[0]
                
                # Create ACCOUNT
                account_id_var = cursor.var(int)
                cursor.execute("""
                    INSERT INTO ACCOUNT (BRANCH_ID, TYPE_ID, BALANCE, ACCOUNT_MODE, STATUS)
                    VALUES (:branch_id, :type_id, :balance, 'Individual', 'Active')
                    RETURNING ACCOUNT_ID INTO :account_id
                """, {
                    'branch_id': branch_id,
                    'type_id': account_type_id,
                    'balance': balance,
                    'account_id': account_id_var
                })
                account_id = account_id_var.getvalue()[0]
                
                # Create ACCOUNT_HOLDER
                cursor.execute("""
                    INSERT INTO ACCOUNT_HOLDER (ACCOUNT_ID, CUSTOMER_ID, HOLDER_TYPE)
                    VALUES (:account_id, :customer_id, 'Primary')
                """, {
                    'account_id': account_id,
                    'customer_id': customer_id
                })
                
                # Create CARD
                import random
                from datetime import timedelta
                card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
                expiry_date = date.today() + timedelta(days=365*5)
                
                card_id_var = cursor.var(int)
                cursor.execute("""
                    INSERT INTO CARD (ACCOUNT_ID, CARD_NUMBER, CARD_TYPE, EXPIRY_DATE, STATUS, DAILY_LIMIT)
                    VALUES (:account_id, :card_number, 'Debit', :expiry_date, 'Active', 100000)
                    RETURNING CARD_ID INTO :card_id
                """, {
                    'account_id': account_id,
                    'card_number': card_number,
                    'expiry_date': expiry_date,
                    'card_id': card_id_var
                })
                
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(f"Failed to ensure account and card: {str(e)}")
        finally:
            cursor.close()
            connection.close()


class TransactionDAO:
    """Data Access Object for Transaction operations - maps to BANK_TRANSACTION"""
    
    @staticmethod
    def create(user_id: int, recipient_name: str, recipient_card_number: str, amount: float, transaction_type: str) -> int:
        """
        Create a new transaction and return the ID
        For deposits: recipient_account_id = account_id (self)
        For transfers: 
          - Debit: from sender's account to recipient's account
          - Credit: from recipient's account perspective (shows incoming transfer)
        """
        connection = db.get_connection()
        cursor = connection.cursor()
        try:
            # Get account_id and balance for the user (could be sender or recipient)
            account_query = """
                SELECT ah.ACCOUNT_ID, a.BALANCE
                FROM ACCOUNT_HOLDER ah
                JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
                JOIN ACCOUNT a ON ah.ACCOUNT_ID = a.ACCOUNT_ID
                WHERE ua.USER_ID = :user_id AND ah.HOLDER_TYPE = 'Primary'
            """
            cursor.execute(account_query, {'user_id': user_id})
            account_row = cursor.fetchone()
            if not account_row:
                raise Exception("Account not found for user")
            account_id = account_row[0]
            account_balance = float(account_row[1])
            
            # Determine recipient_account_id and transaction details
            if transaction_type in ['Credit', 'Credit - Deposit']:
                # Deposit or incoming transfer: recipient is the same account
                recipient_account_id = account_id
                if 'Deposit' in transaction_type:
                    schema_transaction_type = 'Deposit'
                    balance_remaining = account_balance + amount
                else:
                    # Incoming transfer (Credit)
                    schema_transaction_type = 'Transfer'
                    balance_remaining = account_balance + amount
            else:
                # Debit or outgoing transfer: find recipient's account by card number
                recipient_query = """
                    SELECT a.ACCOUNT_ID
                    FROM CARD c
                    JOIN ACCOUNT a ON c.ACCOUNT_ID = a.ACCOUNT_ID
                    WHERE c.CARD_NUMBER = :card_number AND c.STATUS = 'Active'
                """
                cursor.execute(recipient_query, {'card_number': recipient_card_number})
                recipient_account = cursor.fetchone()
                if not recipient_account:
                    raise Exception("Recipient account not found")
                recipient_account_id = recipient_account[0]
                
                if 'Airtime' in transaction_type:
                    schema_transaction_type = 'Transfer'  # Treat as transfer
                else:
                    schema_transaction_type = 'Transfer'
                balance_remaining = account_balance - amount
            
            transaction_mode = 'Online'
            
            # Create transaction
            transaction_id_var = cursor.var(int)
            cursor.execute("""
                INSERT INTO BANK_TRANSACTION (
                    ACCOUNT_ID, RECIPIENT_ACCOUNT_ID, RECIPIENT_ACCOUNT_NAME,
                    AMOUNT, TRANSACTION_TYPE, TRANSACTION_MODE, BALANCE_REMAINING, TRANSACTION_DATE
                )
                VALUES (
                    :account_id, :recipient_account_id, :recipient_name,
                    :amount, :transaction_type, :transaction_mode, :balance_remaining, :transaction_date
                )
                RETURNING TRANSACTION_ID INTO :transaction_id
            """, {
                'account_id': account_id,
                'recipient_account_id': recipient_account_id,
                'recipient_name': recipient_name,
                'amount': amount,
                'transaction_type': schema_transaction_type,
                'transaction_mode': transaction_mode,
                'balance_remaining': balance_remaining,
                'transaction_date': datetime.utcnow(),
                'transaction_id': transaction_id_var
            })
            connection.commit()
            return transaction_id_var.getvalue()[0] if transaction_id_var.getvalue() else None
        except Exception as e:
            connection.rollback()
            raise Exception(f"Transaction creation failed: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_user_id(user_id: int, order_by: str = "TRANSACTION_DATE DESC") -> List[Dict]:
        """Get all transactions for a user"""
        query = f"""
            SELECT 
                t.TRANSACTION_ID as id,
                ua.USER_ID as user_id,
                t.RECIPIENT_ACCOUNT_NAME as recipient_name,
                c.CARD_NUMBER as recipient_card_number,
                t.AMOUNT as amount,
                t.TRANSACTION_TYPE as type,
                t.TRANSACTION_DATE as timestamp,
                t.BALANCE_REMAINING,
                t.TRANSACTION_MODE
            FROM BANK_TRANSACTION t
            JOIN ACCOUNT a ON t.ACCOUNT_ID = a.ACCOUNT_ID
            JOIN ACCOUNT_HOLDER ah ON a.ACCOUNT_ID = ah.ACCOUNT_ID
            JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
            LEFT JOIN CARD c ON t.RECIPIENT_ACCOUNT_ID = c.ACCOUNT_ID AND c.STATUS = 'Active'
            WHERE ua.USER_ID = :user_id
            ORDER BY {order_by}
        """
        return db.execute_query(query, {'user_id': user_id}, fetch_all=True)
    
    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[Dict]:
        """Get transaction by ID"""
        query = """
            SELECT 
                t.TRANSACTION_ID as id,
                ua.USER_ID as user_id,
                t.RECIPIENT_ACCOUNT_NAME as recipient_name,
                c.CARD_NUMBER as recipient_card_number,
                t.AMOUNT as amount,
                t.TRANSACTION_TYPE as type,
                t.TRANSACTION_DATE as timestamp,
                t.BALANCE_REMAINING,
                t.TRANSACTION_MODE
            FROM BANK_TRANSACTION t
            JOIN ACCOUNT a ON t.ACCOUNT_ID = a.ACCOUNT_ID
            JOIN ACCOUNT_HOLDER ah ON a.ACCOUNT_ID = ah.ACCOUNT_ID
            JOIN USER_AUTH ua ON ah.CUSTOMER_ID = ua.CUSTOMER_ID
            LEFT JOIN CARD c ON t.RECIPIENT_ACCOUNT_ID = c.ACCOUNT_ID AND c.STATUS = 'Active'
            WHERE t.TRANSACTION_ID = :transaction_id
        """
        return db.execute_query(query, {'transaction_id': transaction_id}, fetch_one=True)


class BeneficiaryDAO:
    """Data Access Object for Beneficiary operations - kept for backward compatibility but may need schema update"""
    
    @staticmethod
    def create(user_id: int, account_number: str, beneficiary_name: str, nickname: str = None, bank_name: str = None) -> int:
        """Note: Beneficiaries table doesn't exist in new schema - this is a placeholder"""
        raise NotImplementedError("Beneficiaries feature not available in new schema. Use account numbers for transfers.")
    
    @staticmethod
    def get_by_user_id(user_id: int) -> List[Dict]:
        """Note: Beneficiaries table doesn't exist in new schema"""
        return []


