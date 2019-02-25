import mysql.connector
import getpass

hosts = open("hosts.txt")

login = input("Login: ")
passwd = getpass.getpass('Password: ')

for hostdb in hosts:

    hostdb = hostdb[:-1]

    exportdb = mysql.connector.connect(
        host = hostdb,
        user = login,
        passwd = passwd
    )
    exportdbcursor = exportdb.cursor()

    exportdbcursor.execute("show variables like 'hostname'")
    hostname = exportdbcursor.fetchone()
    exportdbcursor.execute("show variables like 'innodb_version'")
    version = exportdbcursor.fetchone()

    exportdbcursor.execute("select User,Password from mysql.user where Host like '172.16%'")

    result = exportdbcursor.fetchall()

    for row in result:
        row = (hostname[1], ) + (hostdb, ) + row + (version[1], )

        userdb = mysql.connector.connect(
            host="172.16.20.38",
            user=login,
            passwd=passwd,
            db="userdb"
        )
        userdbcursor = userdb.cursor()

        sql_insert = "INSERT INTO users (hostname,ip,login,password,version) VALUES (%s, %s, %s, %s, %s)"

        userdbcursor.execute(sql_insert, row)
        userdb.commit()
        print(row)

hosts.close()

