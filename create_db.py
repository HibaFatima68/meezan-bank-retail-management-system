import oracledb

connection = oracledb.connect(
    user="C##HRTESTER",               # use your real admin/developer user
    password="YourPasswordHere",
    dsn="localhost:1521/iba"
)

cursor = connection.cursor()

cursor.execute("""
    CREATE USER C##dbproj IDENTIFIED BY dbproj123
""")

cursor.execute("""
    GRANT CONNECT, RESOURCE TO C##dbproj
""")

cursor.execute("""
    ALTER USER C##dbproj QUOTA UNLIMITED ON USERS
""")

print("Oracle schema 'C##dbproj' created successfully.")

cursor.close()
connection.close()
