import mysql.connector

login = input("Login:")
passwd = input("Password:")

mysqlmanagerdb = mysql.connector.connect(
        host="172.16.20.115",
        user=login,
        passwd=passwd,
        db="mysql_manager"
    )

mysqlmanagerdbcursor = mysqlmanagerdb.cursor()

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