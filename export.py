import mysql.connector
from packaging import version

login = input("Login:")
passwd = input("Password:")

mysqlmanagerdb = mysql.connector.connect(
        host="172.16.20.115",
        user=login,
        passwd=passwd,
        db="mysql_manager"
    )

mysqlmanagerdbcursor = mysqlmanagerdb.cursor()

mysqlmanagerdbcursor.execute("truncate table users")
mysqlmanagerdb.commit()

mysqlmanagerdbcursor.execute("SELECT ip FROM hosts")
hosts = mysqlmanagerdbcursor.fetchall()


for host in hosts:

    try:
        exportdb = mysql.connector.connect(
            host = host[0],
            user = login,
            passwd = passwd
        )
    except:
        print("Server " + host[0] + " is not available. (Mysql is not running or authentication failed)")
        continue

    exportdbcursor = exportdb.cursor()

    exportdbcursor.execute("show variables like 'hostname'")
    hostname = exportdbcursor.fetchone()
    exportdbcursor.execute("show variables like 'innodb_version'")
    mysql_version = exportdbcursor.fetchone()

    if version.parse(mysql_version[1]) > version.parse("5.7"):
        exportdbcursor.execute("select User,Host,authentication_string from mysql.user where (Host like '172.16%') OR (Host like '\%')")
        result = exportdbcursor.fetchall()
    else:
        exportdbcursor.execute("select User,Host,Password from mysql.user where (Host like '172.16%') OR (Host like '\%')")
        result = exportdbcursor.fetchall()

    for row in result:
        row = (hostname[1], ) + (host[0], ) + row + (mysql_version[1], )

        sql_insert = "INSERT INTO users (hostname,ip,login,host,password,version) VALUES (%s, %s, %s, %s, %s, %s)"

        mysqlmanagerdbcursor.execute(sql_insert, row)
        mysqlmanagerdb.commit()
    exportdbcursor.close()
    exportdb.close()

mysqlmanagerdbcursor.close()
mysqlmanagerdb.close()