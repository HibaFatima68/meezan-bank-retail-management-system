import oracledb
import os

def setup_oracle_database():
    try:
        # Connection
        connection = oracledb.connect(
            user="C##HRTESTER",
            password="123",
            dsn="localhost:1521/orcl"
        )
        
        cursor = connection.cursor()
        
        print("Dropping and recreating tables with Identity columns...")
        
        with open('oracle_setup.sql', 'r') as file:
            sql_script = file.read()
        
        statements = sql_script.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement:  
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except oracledb.DatabaseError as e:
                    error_obj, = e.args
                    if error_obj.code == 942:  
                        print("Table didn't exist (this is fine for first run)")
                    else:
                        print(f"Error: {e}")
        
        connection.commit()
        print("Oracle database setup completed successfully!")
        
    except Exception as e:
        print(f"Error during setup: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    setup_oracle_database()