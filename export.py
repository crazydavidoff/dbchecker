import mysql.connector
import getpass

hosts = open("hosts.txt")

login = input("Login: ")
passwd = getpass.getpass('Password: ')

userdb = mysql.connector.connect(
        host="172.16.20.38",
        user=login,
        passwd=passwd,
        db="userdb"
    )

userdbcursor = userdb.cursor()

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

    exportdbcursor.execute("select User,Host,Password from mysql.user where (Host like '172.16%') OR (Host like '\%')")

    result = exportdbcursor.fetchall()

    for row in result:
        row = (hostname[1], ) + (hostdb, ) + row + (version[1], )

        sql_insert = "INSERT INTO users (hostname,ip,login,host,password,version) VALUES (%s, %s, %s, %s, %s, %s)"

        userdbcursor.execute(sql_insert, row)
        print(row)
    userdb.commit()

hosts.close()

