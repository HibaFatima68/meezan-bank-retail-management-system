
import oracledb



connection = oracledb.connect(
    user="C##HRTESTER",
    password="123",
    dsn="localhost:1521/orcl"   # OR service name
)

cursor = connection.cursor()

cursor.execute("SELECT table_name FROM user_tables")

tables = cursor.fetchall()
for table in tables:
    print(table[0])

cursor.close()
connection.close()
