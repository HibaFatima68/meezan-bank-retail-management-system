
import oracledb



connection = oracledb.connect(
    user="C##dbproject",
    password="123",
    dsn="DESKTOP-3PG8SO1:1521/orcl"   # OR service name
)

cursor = connection.cursor()

cursor.execute("SELECT table_name FROM user_tables")

tables = cursor.fetchall()
for table in tables:
    print(table[0])

cursor.close()
connection.close()
