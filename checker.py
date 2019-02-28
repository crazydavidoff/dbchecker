import mysql.connector


login = input("Login:")
passwd = input("Password:")

userdb = mysql.connector.connect(
    host = "172.16.20.38",
    user = login,
    passwd = passwd,
    db = "userdb"
)

userdbcursor = userdb.cursor()

userdbcursor.execute("SELECT login,password FROM export")

result = userdbcursor.fetchall()

if not result:
    print("Table is empty")
    exit(0)

else:
    for row in result:
        #userdbcursor = userdb.cursor()
        hash_query = "SELECT password(%s)"
        userdbcursor.execute(hash_query, (row[1],))
        new_hash = userdbcursor.fetchone()
        row = (row[0],) + new_hash

        #change_query = "update users set password = %s where login like %s;"

        print(row)

