import mysql.connector
import xmltodict
import matplotlib.pyplot as plt

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



