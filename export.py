import mysql.connector

userdb = mysql.connector.connect(
    host = "172.16.20.38",
    user = "",
    passwd = "",
    db = "userdb"
)

userdbcursor = userdb.cursor()

userdbcursor.execute("select User,Password from mysql.user where Host like '172.16%'")

result = userdbcursor.fetchall()
for row in result:
    print(row)