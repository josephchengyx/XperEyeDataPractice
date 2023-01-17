import mysql.connector
import xmltodict
import matplotlib.pyplot as plt
import pandas as pd


# class DBConnection:
#     def __init__(self, host_name, user_name, user_password):
#         self.host_name = host_name
#         self.user_name = user_name
#         self.user_password = user_password
#         self.connection = None
#         try:
#             self.connection = mysql.connector.connect(
#                 host=host_name,
#                 user=user_name,
#                 passwd=user_password
#             )
#             print("MySQL Database Connection Successful!")
#         except ConnectionError as err:
#             print(f"Error:" '{err}'"")
#         return self.connection
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

def get_column_from_table(cnx, column, table, matchcol, matchval, fetch_one = True):
    sql = f'SELECT {column} FROM {table} WHERE {matchcol} = %({matchcol})s'

    cur = cnx.cursor()
    cur.execute(sql, {matchcol: matchval})
    if fetch_one:
        row = cur.fetchone()
        return int(row[0])
    else:
        return cur.fetchall()


def get_rows_from_table(cnx, colnames, table):
    sql = f'SELECT {colnames} FROM {table}'

    cur = cnx.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [x.strip() for x in colnames.split(',')]
    return df


