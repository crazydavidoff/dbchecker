#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector
from packaging import version

login = "change-pass-user"
passwd = "testuser"
try:
    mysqlmanagerdb = mysql.connector.connect(
        host="localhost",
        user=login,
        passwd=passwd,
        db="test_manager"
    )
except:
    print("Server is not available. (Mysql is not running or authentication failed)")
mysqlmanagerdbcursor = mysqlmanagerdb.cursor()
mysqlmanagerdbcursor.execute("SELECT users.login, users.mysql_hash, mysql_servers.ip, mysql_servers.version, "
                             "mysql_link.id FROM users, mysql_link, mysql_servers "
                             "WHERE mysql_link.id_srv=mysql_servers.id_srv AND mysql_link.id_user=users.id_user "
                             "AND mysql_link.changed='1'")
result = mysqlmanagerdbcursor.fetchall()

if result:
    for row in result:
        hashpassword = row[1]
        versiondb = row[3]
        #подключение к управляемым базам
        forupdatedb = mysql.connector.connect(
            host=row[2],
            user=login,
            passwd=passwd,
            db="mysql"
        )

        forupdatedbcursor = forupdatedb.cursor()
        fulluser = row[0]
        if (len(fulluser) > 15):
            cutuser = fulluser[:15] + "%"
        else:
            cutuser = fulluser + "%"
        if version.parse(versiondb) > version.parse("5.7"):
            update_query2 = ("UPDATE mysql.user SET authentication_string=%s WHERE Host='172.16.%' and User like %s")
        else:
            update_query2 = ("UPDATE mysql.user SET Password=%s WHERE Host='172.16.%' and User like %s")

        param = (hashpassword,) + (cutuser,)
        try:
            forupdatedbcursor.execute(update_query2, param)
            forupdatedb.commit()
            forupdatedbcursor.execute("flush privileges")
            forupdatedb.commit()
        except:
           print("Unexpectedly error with host: " + row[2])
        forupdatedbcursor.close()
        forupdatedb.close()
        mysqlmanagerdbcursor.execute("""UPDATE mysql_link SET changed = '0' WHERE id = \'%s\'""" % row[4])
        mysqlmanagerdb.commit()
mysqlmanagerdbcursor.close()
mysqlmanagerdb.close()
