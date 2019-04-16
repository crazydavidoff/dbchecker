import mysql.connector
from packaging import version

login = input("Login:")
passwd = input("Password:")

mysqlmanagerdb = mysql.connector.connect(
    host = "172.16.20.115",
    user = login,
    passwd = passwd,
    db = "mysql_manager"
)

accountsdb = mysql.connector.connect(
    host = "172.16.20.115",
    user = login,
    passwd = passwd,
    db = "accounts"
)

accountsdbcursor = accountsdb.cursor()
mysqlmanagerdbcursor = mysqlmanagerdb.cursor()

accountsdbcursor.execute("SELECT login_change,password_change FROM Password where mysql_flag is NULL")
result = accountsdbcursor.fetchall()

if result:
    for row in result:
        login16 = row[0][:16]+"%"
        update_query = "update users set password = password(%s) where login like %s"
        row = (row[1],) + (login16,)
        mysqlmanagerdbcursor.execute(update_query, row)
        set_flag_query = "UPDATE Password SET mysql_flag = '1' WHERE login_change like %s"
        accountsdbcursor.execute(set_flag_query, (login16,))
        accountsdb.commit()
        mysqlmanagerdb.commit()

        mysqlmanagerdbcursor.execute("SELECT ip,login,host,password,version FROM users where login like %s", (login16,))
        result2 = mysqlmanagerdbcursor.fetchall()
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

accountsdbcursor.execute("delete from Password where mysql_flag = '1' and ad_flag = '1'")
accountsdb.commit()
mysqlmanagerdbcursor.close()
mysqlmanagerdb.close()
accountsdbcursor.close()
accountsdb.close()