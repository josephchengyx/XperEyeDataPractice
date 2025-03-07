import mysql.connector
import pandas as pd


class DBConnection:
    def __init__(self, host_name, user_name, user_password):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
            self.cursor = self.connection.cursor()
            print("MySQL Database Connection Successful!")
        except ConnectionError as err:
            print(f"Error:" '{err}'"")

    def get_cursor(self):
        return self.connection.cursor

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_column_from_table(self, column, table, matchcol, matchval, fmt=None):
        sql = f'SELECT {column} FROM {table} WHERE {matchcol} = %({matchcol})s'
        self.cursor.execute(sql, {matchcol: matchval})
        fetch_result = list(map(lambda x: x[0], self.cursor.fetchall()))
        if fmt is not None:
            fetch_result = list(map(fmt, fetch_result))
        if len(fetch_result) == 1:
            return fetch_result[0]
        else:
            return fetch_result



def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database Connection Successful!")
    except ConnectionError as err:
        print(f"Error:" '{err}'"")
    return connection



def get_rows_from_table(cnx, colnames, table):
    sql = f'SELECT {colnames} FROM {table}'

    cur = cnx.get_cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [x.strip() for x in colnames.split(',')]
    return df


