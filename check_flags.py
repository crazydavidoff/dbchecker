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

accountsdb = mysql.connector.connect(
    host = "172.16.20.115",
    user = login,
    passwd = passwd,
    db = "accounts"
)

accountsdbcursor = accountsdb.cursor()
mysqlmanagerdbcursor = mysqlmanagerdb.cursor()
mysqlmanagerdbcursor.execute("DELETE FROM deleted_users WHERE mysql_flag = 1 AND ad_flag = 1")
mysqlmanagerdb.commit()
accountsdbcursor.execute("DELETE FROM Password WHERE mysql_flag = '1' AND ad_flag = '1' AND nginx_flag = '1'")
accountsdb.commit()

accountsdbcursor.execute("SELECT login_change,password_change FROM Password where mysql_flag is NULL")
result = accountsdbcursor.fetchall()

if result:
    for row in result:
        mysqlmanagerdbcursor.execute("SELECT id FROM users WHERE login = %s", (row[1], row[0],))
        a = mysqlmanagerdb.fetchall()
        if a:
            #обновляем пароль в нашей табличке
            mysqlmanagerdbcursor.execute("UPDATE users SET mysql_hash = password(%s) WHERE login = %s", (row[1], row[0],))
            mysqlmanagerdb.commit()
        else:
            #добовляем нового пользователя, если нету существующего
            mysqlmanagerdbcursor.execute("INSERT INTO users(login, mysql_hash) VALUES(%s, password(%s))", (row[0], row[1],))
            mysqlmanagerdb.commit()
        #обновить флаг в базе паспорта
        accountsdbcursor.execute("UPDATE Password SET mysql_flag = '1' WHERE login_change = %s", (row[0],))
        accountsdb.commit()

accountsdbcursor.close()
accountsdb.close()
mysqlmanagerdbcursor.close()
mysqlmanagerdb.close()




