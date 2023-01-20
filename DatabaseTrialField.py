import xmltodict
from DBUtil import create_server_connection
import pandas as pd


class DatabaseTrialField:

    def __init__(self):
        self.connection = create_server_connection("localhost", "xper_rw", "up2nite")
        self.cur = self.connection.cursor()

    def get_rows(self, colnames, table):
        sql = f'SELECT {colnames} FROM {table}'
        self.cur.execute(sql)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = [x.strip() for x in colnames.split(',')]
        return df

    @staticmethod
    def parse_msgs_into_df(msgs, xml_tag):
        msg_list = []
        for msg in msgs:
            temp = xmltodict.parse(msg)[xml_tag]
            msg_list.append(temp)

        df = pd.DataFrame(msg_list)

        return df

    def get_value_from_matching_entry(self, column, table, matchcol, matchval):
        sql = f'SELECT {column} FROM {table} WHERE {matchcol} = %({matchcol})s'
        self.cur.execute(sql, {matchcol: matchval})
        row = self.cur.fetchone()

        return int(row[0])

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cur
