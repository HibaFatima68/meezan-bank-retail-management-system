import oracledb

try:
    con = oracledb.connect(
        user="c##hrtester",
        password="123",
        dsn="localhost:1521/iba"
    )
    print("Connected!")
    con.close()
except Exception as e:
    print("ERROR:", e)
