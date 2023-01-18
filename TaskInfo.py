import xmltodict
import pandas as pd
import numpy as np

from DatabaseTrialField import DatabaseTrialField


class TaskInfo(DatabaseTrialField):

    def __init__(self):
        super().__init__()

    def get(self):
        '''------------------COMMON---------------------'''
        beh_msg = super().get_rows('type, msg', 'jkDev.BehMsg')
        slide_msgs = beh_msg[beh_msg['type'].str.contains("Slide")].reset_index(drop=True)
        slide_msgs = slide_msgs['msg']

        slide_msg_list = []
        for msg in slide_msgs:
            slide_msg = xmltodict.parse(msg)['PngSlideEvent']
            slide_msg_list.append(slide_msg)

        df = pd.DataFrame(slide_msg_list)
        '''------------------COMMON---------------------'''
        pd.set_option('display.max_columns', None)

        '''
        # remove SlideOn that doesn't have the corresponding SlideOff
        # frameCount = -1 is slideOn
        '''
        a = pd.DataFrame()
        for i in range(df.shape[0]):
            try:
                if df['frameCount'][i] == "-1" and df['frameCount'][i+1] == "0":
                    a = pd.concat([a, df.iloc[i:i+2]])
            except:
                print('done')

        a = pd.pivot_table(a,index = ['taskId','slideFileName'], values = 'timestamp',columns = ['frameCount']).astype(int)

        return None

if __name__ == "__main__":
    # x = DatabaseTrialField()
    # msg = x.get_rows('type, msg', 'jkDev.BehMsg')
    # print(msg)

    y = TaskInfo()
    events = y.get()