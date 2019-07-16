#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector
from packaging import version

login = "change-pass-user"
passwd = "testuser"

mysqlmanagerdb = mysql.connector.connect(
        host="localhost",
        user=login,
        passwd=passwd,
        db="test_manager"
    )

mysqlmanagerdbcursor = mysqlmanagerdb.cursor()
mysqlmanagerdbcursor.execute("SELECT mysql_servers.ip, mysql_servers.version, users.login, users.mysql_hash, "
                             "mysql_link.id FROM users, mysql_link, mysql_servers "
                             "WHERE mysql_link.id_srv=mysql_servers.id_srv AND mysql_link.id_user=users.id_user "
                             "AND mysql_link.new='1'")
result = mysqlmanagerdbcursor.fetchall()
if result:
    for host in result:
        try:
            exportdb = mysql.connector.connect(
                host=host[0],
                user=login,
                passwd=passwd,
                db="mysql"
            )
        except:
            print("Server " + host[0] + " is not available. (Mysql is not running or authentication failed)")
            continue
        print("HOST: "+host[0])
        print("Login: " + host[2])
        exportdbcursor = exportdb.cursor()
        exportdbcursor.execute("show variables like 'innodb_version'")
        mysql_version = exportdbcursor.fetchone()
        fulluser = host[2]
        if (len(fulluser) > 15):
            cutuser = fulluser[:15] + "%"
        else:
            cutuser = fulluser + "%"
        if version.parse(mysql_version[1]) > version.parse("5.7"):
            try:
                exportdbcursor.execute("""create user %s@'172.16.%' identified WITH mysql_native_password;""", (fulluser,))
                exportdb.commit()
                exportdbcursor.execute("""UPDATE mysql.user SET authentication_string = %s WHERE User like %s AND Host='172.16.%';""",
                                       (host[3], cutuser,))
                exportdb.commit()
                exportdbcursor.execute("flush privileges")
                exportdb.commit()
                mysqlmanagerdbcursor.execute("""UPDATE mysql_link SET new = '0' WHERE id = %s""", (host[4],))
                mysqlmanagerdb.commit()
            except:
                print("Duplicate entry or you do not have privileges on server: " + host[0])
                continue
        else:
            try:
                exportdbcursor.execute("""create user %s@'172.16.%' identified WITH mysql_native_password;""", (cutuser,))
                exportdb.commit()
                exportdbcursor.execute("""UPDATE mysql.user SET Password = '%s' WHERE User like %s AND Host='172.16.%';""",
                                       (host[3], cutuser,))
                exportdb.commit()
                exportdbcursor.execute("flush privileges")
                exportdb.commit()
                mysqlmanagerdbcursor.execute("""UPDATE mysql_link SET new = '0' WHERE id = \'%s\'""", (host[4],))
                mysqlmanagerdb.commit()
            except:
                print("Duplicate entry or you do not have privileges on server: " + host[0])
                continue
            exportdbcursor.close()
            exportdb.close()

mysqlmanagerdbcursor.close()
mysqlmanagerdb.close()




