import mysql.connector
from mysql.connector import Error


class DataBase:
    def __init__(self, kind, line, host, database, user, password, table, time_field):

        self.kind = kind
        self.line = line
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.table = table
        self.time_field = time_field

        self.name = kind + ' - ' + line

        try:
            self.connection = mysql.connector.connect(host=host,
                                                      database=database,
                                                      user=user,
                                                      password=password)

            if self.connection.is_connected():
                self.status = 'Ok'
                # self.cursor = self.connection.cursor() # Not used as it is declared in the execution methods
            else:
                self.status = 'ERROR'
                print(f'DataBase: {self.name}\t Status: {self.status}')

        except Error as e:
            print(f"Error while connecting to {self.name}\t", e)

    def execute_query_get_one(self, query):
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()[0]
        cursor.close()
        return data

    def execute_query_get_all(self, query):
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_type(self):
        return self.kind

    def get_line(self):
        return self.line
