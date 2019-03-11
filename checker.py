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

userdbcursor.execute("SELECT login,password FROM export where mysql_flag is NULL")
result = userdbcursor.fetchall()

if result:
    for row in result:
        login9 = row[0][:9]+"%"
        update_query = "update users set password = password(%s) where login like %s"
        row = (row[1],) + (login9,)
        userdbcursor.execute(update_query, row)
        set_flag_query = "UPDATE export SET mysql_flag = '1' WHERE login like %s"
        userdbcursor.execute(set_flag_query, (login9,))
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

userdbcursor.execute("delete from export where mysql_flag = '1' and ad_flag = '1'")
userdb.commit()
userdbcursor.close()
userdb.close()