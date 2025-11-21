"""
Database Connection Verification Script
"""
from app.database import db
from app.db_utils import UserDAO, TransactionDAO

def verify_connection():
    print("=" * 60)
    print("Oracle Database Connection Verification")
    print("New Banking Schema (banking.schema2.sql)")
    print("=" * 60)
    
    print("\n1. Testing basic connection...")
    try:
        if db.verify_connection():
            print("   ✓ Connection successful!")
        else:
            print("   ✗ Connection failed!")
            return False
    except Exception as e:
        print(f"   ✗ Connection error: {str(e)}")
        return False
    
    print("\n2. Checking core tables...")
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM user_tables 
                WHERE table_name IN ('CUSTOMER', 'USER_AUTH', 'ACCOUNT', 'ACCOUNT_HOLDER', 
                                     'BANK_TRANSACTION', 'CARD', 'BRANCH', 'ACCOUNT_TYPE')
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            
            expected_tables = ['CUSTOMER', 'USER_AUTH', 'ACCOUNT', 'ACCOUNT_HOLDER', 
                              'BANK_TRANSACTION', 'CARD', 'BRANCH', 'ACCOUNT_TYPE']
            found_tables = [table[0] for table in tables]
            
            print(f"   Expected core tables: {len(expected_tables)}")
            print(f"   Found tables: {len(found_tables)}")
            
            for table in expected_tables:
                if table in found_tables:
                    print(f"   ✓ {table} exists")
                else:
                    print(f"   ✗ {table} missing")
            
            if len(found_tables) >= len(expected_tables):
                print("   ✓ All required core tables exist!")
            else:
                print("   ✗ Some core tables are missing!")
                print("   → Make sure you ran banking.schema2.sql")
    except Exception as e:
        print(f"   ✗ Error checking tables: {str(e)}")
        return False
    
    print("\n3. Checking EMAIL column in CUSTOMER table...")
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM user_tab_columns 
                WHERE table_name = 'CUSTOMER' AND column_name = 'EMAIL'
            """)
            email_col = cursor.fetchone()
            
            if email_col:
                print("   ✓ EMAIL column exists in CUSTOMER table")
            else:
                print("   ✗ EMAIL column missing!")
                print("   → Run schema_additions.sql to add EMAIL column")
    except Exception as e:
        print(f"   ✗ Error checking EMAIL column: {str(e)}")
    
    print("\n4. Checking sequences...")
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT sequence_name 
                FROM user_sequences 
                WHERE sequence_name IN ('CUSTOMER_SEQ', 'USER_AUTH_SEQ', 'ACCOUNT_SEQ', 
                                        'TRANSACTION_SEQ', 'CARD_SEQ', 'BRANCH_SEQ', 'ACCOUNT_TYPE_SEQ')
                ORDER BY sequence_name
            """)
            sequences = cursor.fetchall()
            
            expected_sequences = ['CUSTOMER_SEQ', 'USER_AUTH_SEQ', 'ACCOUNT_SEQ', 
                                'TRANSACTION_SEQ', 'CARD_SEQ', 'BRANCH_SEQ', 'ACCOUNT_TYPE_SEQ']
            found_sequences = [seq[0] for seq in sequences]
            
            print(f"   Expected sequences: {len(expected_sequences)}")
            print(f"   Found sequences: {len(found_sequences)}")
            
            for seq in expected_sequences:
                if seq in found_sequences:
                    print(f"   ✓ {seq} exists")
                else:
                    print(f"   ✗ {seq} missing")
            
            if len(found_sequences) >= len(expected_sequences):
                print("   ✓ All required sequences exist!")
            else:
                print("   ✗ Some sequences are missing!")
    except Exception as e:
        print(f"   ✗ Error checking sequences: {str(e)}")
        return False
    
    print("\n5. Testing DAO operations...")
    try:
        customer_count = db.execute_query("SELECT COUNT(*) as count FROM CUSTOMER", fetch_one=True)
        count_value = customer_count.get('count', 0) if customer_count else 0
        print(f"   ✓ CUSTOMER table: {count_value} customers")
        
        auth_count = db.execute_query("SELECT COUNT(*) as count FROM USER_AUTH", fetch_one=True)
        count_value = auth_count.get('count', 0) if auth_count else 0
        print(f"   ✓ USER_AUTH table: {count_value} user accounts")
        
        account_count = db.execute_query("SELECT COUNT(*) as count FROM ACCOUNT", fetch_one=True)
        count_value = account_count.get('count', 0) if account_count else 0
        print(f"   ✓ ACCOUNT table: {count_value} accounts")
        
        trans_count = db.execute_query("SELECT COUNT(*) as count FROM BANK_TRANSACTION", fetch_one=True)
        count_value = trans_count.get('count', 0) if trans_count else 0
        print(f"   ✓ BANK_TRANSACTION table: {count_value} transactions")
        
        branch_count = db.execute_query("SELECT COUNT(*) as count FROM BRANCH", fetch_one=True)
        branch_value = branch_count.get('count', 0) if branch_count else 0
        print(f"   ✓ BRANCH table: {branch_value} branches (expected: 3)")
        
        account_type_count = db.execute_query("SELECT COUNT(*) as count FROM ACCOUNT_TYPE", fetch_one=True)
        type_value = account_type_count.get('count', 0) if account_type_count else 0
        print(f"   ✓ ACCOUNT_TYPE table: {type_value} account types (expected: 3)")
        
    except Exception as e:
        print(f"   ✗ Error testing DAO operations: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ Database connection and schema verification completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. If any tables/sequences are missing, run banking.schema2.sql")
    print("  2. If EMAIL column is missing, run schema_additions.sql")
    print("  3. Start the application: python run.py")
    return True

if __name__ == '__main__':
    try:
        verify_connection()
    except Exception as e:
        print(f"\n✗ Verification failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

