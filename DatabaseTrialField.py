import xmltodict
from DBUtil import create_server_connection
import pandas as pd

class DatabaseTrialField:

    def __init__(self):
        self.table = None
        self.connection = create_server_connection("localhost", "xper_rw", "up2nite")
        self.cur = self.connection.cursor()

    def get_rows(self, colnames, table):
        sql = f'SELECT {colnames} FROM {table}'
        self.cur.execute(sql)
        df = pd.DataFrame(self.cur.fetchall())
        df.columns = [x.strip() for x in colnames.split(',')]
        return df

    def get_columns(self):
        pass



