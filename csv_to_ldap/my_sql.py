import sys
import mysql.connector
from mysql.connector import errorcode


class MySQLConnector:

    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
        self.connection = self._get_connection()
        self.cursor = self.connection.cursor()
        self._db_email()

    def _get_connection(self):
        """
        Returns the connection with MySQL using
        the user parameters.
        """
        try:
            connection = mysql.connector.connect(user=self.user,
                                                 password=self.password,
                                                 host=self.host)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("ERROR - MYSQL - Wrong username or password")
                sys.exit()
            else:
                print('ERROR - MYSQL - ', e)
                sys.exit()
        else:
            return connection

    def _create_database(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS company")
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print("ERROR - MYSQL - Failed creating database:", e)
            self._close_resources(self.connection, self.cursor)
            sys.exit()

    def _create_table(self):
        try:
            self.cursor.execute("USE company")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                      id_users INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      name CHAR(255) NOT NULL,
                      lastname CHAR(255) NOT NULL,
                      email CHAR(255) NOT NULL,
                      password CHAR(255) NOT NULL)""")
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print("ERROR - MYSQL - Failed creating table: ", e)
            self._close_resources(self.connection, self.cursor)
            sys.exit()

    def _close_resources(self, connection, cursor):
        cursor.close()
        connection.close()
        return

    def _db_email(self):
        """
        Checks if both database and tables were
        created successfully and close the
        'connection' and 'cursor'.
        """
        if self._create_database() and self._create_table():
            print("INFO - MYSQL - Database 'company' and table 'users' OK")
        self._close_resources(self.connection, self.cursor)

    def insert_items(self, entries):
        """
        Receives the 'entries' object and makes the
        insertion in the database. All the inserted
        items are printed.
        """
        query = "INSERT INTO users(name, lastname, email, password)" \
                "VALUES (%s, %s, %s, MD5(%s))"
        args = (entries['name'],
                entries['lastname'],
                entries['email'],
                entries['password'])
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute("USE company")
            cursor.execute(query, args)
            connection.commit()
            print("INFO - MYSQL - Inserting '{}' on table 'users'".format(args[:-1]))
            return True
        except mysql.connector.Error as e:
            print('ERROR - MYSQL - ', e)
        finally:
            self._close_resources(connection, cursor)
            return False
