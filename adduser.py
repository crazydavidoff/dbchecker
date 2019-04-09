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

mysqlmanagerdbcursor.execute("SELECT ip FROM hosts")
hosts = mysqlmanagerdbcursor.fetchall()


for host in hosts:

    try:
        exportdb = mysql.connector.connect(
            host = host[0],
            user = login,
            passwd = passwd,
            db = "mysql"
        )
    except:
        print("Server " + host[0] + " is not available. (Mysql is not running or authentication failed)")
        continue

    exportdbcursor = exportdb.cursor()

    exportdbcursor.execute("show variables like 'innodb_version'")
    mysql_version = exportdbcursor.fetchone()

    if version.parse(mysql_version[1]) > version.parse("5.7"):

        exportdbcursor.execute("INSERT INTO mysql.user (Host, User, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv, Reload_priv, Shutdown_priv, Process_priv, File_priv, Grant_priv, References_priv, Index_priv, Alter_priv, Show_db_priv, Super_priv, Create_tmp_table_priv, Lock_tables_priv, Execute_priv, Repl_slave_priv, Repl_client_priv, Create_view_priv, Show_view_priv, Create_routine_priv, Alter_routine_priv, Create_user_priv, Event_priv, Trigger_priv, Create_tablespace_priv, ssl_type, ssl_cipher, x509_issuer, x509_subject, max_questions, max_updates, max_connections, max_user_connections, plugin, authentication_string, password_expired, password_last_changed, account_locked) VALUES ('172.16.%', 'ghost', 'N', 'N', 'N', 'N', 'N', 'N', 'Y', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '', '', '', '', '0', '0', '0', '0', 'mysql_native_password', '*D2E0A01D371C3D97746F55189E7DA147F0FB2AA8', 'N', '2019-04-01 00:00:00', 'N')")
        exportdbcursor.execute("flush privileges")
        exportdb.commit()
        exportdbcursor.close()
        exportdb.close()

    else:

        exportdbcursor.execute("INSERT INTO mysql.user (Host, User, Password, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv, Reload_priv, Shutdown_priv, Process_priv, File_priv, Grant_priv, References_priv, Index_priv, Alter_priv, Show_db_priv, Super_priv, Create_tmp_table_priv, Lock_tables_priv, Execute_priv, Repl_slave_priv, Repl_client_priv, Create_view_priv, Show_view_priv, Create_routine_priv, Alter_routine_priv, Create_user_priv, Event_priv, Trigger_priv, Create_tablespace_priv, ssl_type, ssl_cipher, x509_issuer, x509_subject, max_questions, max_updates, max_connections, max_user_connections, plugin) VALUES ('172.16.%', 'change-pass-user', '*D2E0A01D371C3D97746F55189E7DA147F0FB2AA8', 'N', 'N', 'N', 'N', 'N', 'N', 'Y', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '', '', '', '', '0', '0', '0', '0', '')")
        exportdbcursor.execute("flush privileges")
        exportdb.commit()
        exportdbcursor.close()
        exportdb.close()

mysqlmanagerdbcursor.close()
mysqlmanagerdb.close()




