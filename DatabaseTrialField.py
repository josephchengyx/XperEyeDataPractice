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


class TaskInfo(DatabaseTrialField):

    def __init__(self):
        super().__init__()
        self.slide_events = None

    def get(self):
        events = super().get_rows('type, msg', 'jkDev.BehMsg')
        print(events)
        events = events[events['type'].str.contains("Slide")].reset_index(drop=True)
        behMsg = events['msg']

        slide_msg = pd.DataFrame()
        for l in behMsg:
            parsed_line = xmltodict.parse(l)['PngSlideEvent']
            print(parsed_line)

        '''
        # remove SlideOn that doesn't have the corresponding SlideOff
        # frameCount = -1 is slideOn
        '''
        # slide_msg = pd.DataFrame()
        # for i in range(events.shape[0]):
        #     try:
        #         if events.iloc[i]['type'] == 'SlideOn' and events.iloc[i + 1]['type'] == 'SlideOff':  # successful slide
        #             slideOn = xmltodict.parse(events.iloc[i]['msg'])['PngSlideEvent']
        #             slideOff = xmltodict.parse(events.iloc[i+1]['msg'])['PngSlideEvent']
        #             print(slideOn)
        #             hello = pd.DataFrame.from_dict(slideOn)
        #             print(hello)
        #             # temp = pd.DataFrame(
        #             #     {
        #             #         'SlideOnMsg': [events.loc[i]['msg']],
        #             #         'SlideOffMsg': [events.loc[i + 1]['msg']]
        #             #     }
        #             # )
        #             #slide_msg = pd.concat([slide_msg, temp])
        #     except:
        #         print("Note: the experiment ends with 'slideOn' ")
        #print(slide_msg)

        # slide_detail_dict_list = []
        # for i in range(len(slide_msg.columns)):
        #     for line in slide_msg.iloc[:, i]:
        #         slide_details = xmltodict.parse(line)['PngSlideEvent']
        #         slide_detail_dict_list.append(slide_details)
        #
        # # print(slide_detail_dict_list)
        # slide_df = pd.DataFrame.from_dict(slide_detail_dict_list)
        # pd.set_option('display.max_columns', None)
        # slide_df = slide_df.sort_values(by=['timestamp'])
        # # print(slide_df.head())
        # taskId_filePath = slide_df[['taskId', 'slideFileName']].drop_duplicates()

        # return slide_df.pivot(index='taskId', columns='frameCount', values='timestamp')
        return None

if __name__ == "__main__":
    # x = DatabaseTrialField()
    # msg = x.get_rows('type, msg', 'jkDev.BehMsg')
    # print(msg)

    y = TaskInfo()
    events = y.get()
    # print("HELLO")
    # print(events)
