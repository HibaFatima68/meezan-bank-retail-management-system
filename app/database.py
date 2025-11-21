"""
Manual Database Connection Layer for Oracle SQL
"""
import oracledb
import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'C##dbproject')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_DSN = os.getenv('DB_DSN', 'DESKTOP-3PG8SO1:1521/orcl')

class Database:
    
    def __init__(self):
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.dsn = DB_DSN
        self._connection = None
    
    def get_connection(self):
        try:
            connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
            return connection
        except Exception as e:
            raise Exception(f"Database connection failed: {str(e)}")
    
    @contextmanager
    def get_cursor(self, commit=False):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Database operation failed: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_query(self, query: str, params: Optional[Dict] = None, fetch_one: bool = False, fetch_all: bool = False):
        with self.get_cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                row = cursor.fetchone()
                if row and cursor.description:
                    columns = [desc[0].lower() for desc in cursor.description]
                    return dict(zip(columns, row))
                return None
            elif fetch_all:
                rows = cursor.fetchall()
                if rows and cursor.description:
                    columns = [desc[0].lower() for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in rows]
                return []
            return None
    
    def execute_update(self, query: str, params: Optional[Dict] = None):
        """Execute an INSERT, UPDATE, or DELETE query"""
        with self.get_cursor(commit=True) as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.rowcount
    
    def execute_many(self, query: str, params_list: List[Dict]):
        """Execute a query multiple times with different parameters"""
        with self.get_cursor(commit=True) as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    def verify_connection(self) -> bool:
        """Verify database connection"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1 FROM dual")
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            print(f"Connection verification failed: {str(e)}")
            return False

db = Database()

