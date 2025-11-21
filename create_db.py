import oracledb

connection = oracledb.connect(
    user="C##dbproject",
    password="123",
    dsn="DESKTOP-3PG8SO1:1521/orcl"   # OR service name
)

cursor = connection.cursor()

cursor.execute("""CREATE USER bank_user IDENTIFIED BY bank_pass""")

cursor.execute("GRANT CONNECT, RESOURCE TO bank_user")

print("Oracle schema (user) 'bank_user' created successfully.")

cursor.close()
connection.close()

    