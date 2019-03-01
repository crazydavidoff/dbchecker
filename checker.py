import mysql.connector
from packaging import version

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
    exit(0)

else:
    for row in result:
        login9 = row[0][:9]+"%"
        update_query = "update users set password = password(%s) where login like %s"
        row = (row[1],) + (login9,)
        userdbcursor.execute(update_query, row)
        #delete_query = "delete from export where login like %s"
        #userdbcursor.execute(delete_query, (row[1],))
        userdb.commit()

        userdbcursor.execute("SELECT ip,login,host,password,version FROM users where login like %s", (login9,))
        result2 = userdbcursor.fetchall()
        for row2 in result2:
            forupdatedb = mysql.connector.connect(
                host = row2[0],
                user = login,
                passwd = passwd,
                db = "mysql"
            )

            forupdatedbcursor = forupdatedb.cursor()

            if version.parse(row2[4]) > version.parse("5.7"):
                update_query2 = ("UPDATE mysql.user SET authentication_string=%s WHERE Host=%s and User=%s")
            else:
                update_query2 = ("UPDATE mysql.user SET Password=%s WHERE Host=%s and User=%s")

            row2 = (row2[3],) + (row2[2],) + (row2[1],)
            forupdatedbcursor.execute(update_query2, row2)
            forupdatedbcursor.execute("flush privileges")
            forupdatedb.commit()
            forupdatedbcursor.close()
            forupdatedb.close()

        userdbcursor.close()
        userdb.close()