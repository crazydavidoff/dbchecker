import mysql.connector

userdb = mysql.connector.connect(
    host = "172.16.20.38",
    user = "",
    passwd = "",
    db = "userdb"
)

userdbcursor = userdb.cursor()

userdbcursor.execute("SELECT login,password FROM users")

result = userdbcursor.fetchall()
print(result)

if not result:
    print("Table is empty")
    exit(0)

else:


    for row in result:
        print(row)
