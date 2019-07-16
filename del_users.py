#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector

login = "change-pass-user"
passwd = "testuser"

mysqlmanagerdb = mysql.connector.connect(
        host="localhost",
        user=login,
        passwd=passwd,
        db="test_manager"
    )

mysqlmanagerdbcursor = mysqlmanagerdb.cursor()
mysqlmanagerdbcursor.execute("SELECT mysql_servers.ip, mysql_servers.version, mysql_remove_user.login, "
                             "mysql_remove_user.id, mysql_remove_user.old_id_user "
                             "FROM mysql_remove_user, mysql_servers "
                             "WHERE mysql_remove_user.id_srv=mysql_servers.id_srv")
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
        fulluser = host[2]
        if (len(fulluser) > 15):
            cutuser = fulluser[:15] + "%"
        else:
            cutuser = fulluser + "%"
        exportdbcursor = exportdb.cursor()
        exportdbcursor.execute("""SELECT User FROM mysql.user WHERE User like %s""", (cutuser,))
        a = exportdbcursor.fetchone()
        flatten = [str(item) for sub in a for item in sub]
        username = "".join(flatten)
        try:
            exportdbcursor.execute("""drop user %s@'172.16.%';""", (username,))
            exportdb.commit()
            exportdbcursor.execute("flush privileges")
            exportdb.commit()
            mysqlmanagerdbcursor.execute("""DELETE FROM mysql_remove_user WHERE id = %s""", (host[3],))
            mysqlmanagerdb.commit()
        except:
            print("Cannot delete user: " + fulluser + " from host: " + host[0])
            continue

        exportdbcursor.close()
        exportdb.close()
    mysqlmanagerdbcursor.execute("""UPDATE deleted_users SET mysql_flag = 1 WHERE old_id_user = %s""", (host[4],))
    mysqlmanagerdb.commit()
    mysqlmanagerdbcursor.close()
    mysqlmanagerdb.close()




