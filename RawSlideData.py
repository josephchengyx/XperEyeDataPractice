import xmltodict
import pandas as pd
import numpy as np

from DatabaseTrialField import DatabaseTrialField


class RawSlideData(DatabaseTrialField):

    def __init__(self):
        super().__init__()

    def get(self):
        beh_msg = super().get_rows('type, msg', 'jkDev.BehMsg')
        slide_msgs = beh_msg[beh_msg['type'].str.contains("Slide")].reset_index(drop=True)
        slide_msgs = slide_msgs['msg']

        pd.set_option('display.width', 400)
        pd.set_option('display.max_columns', None)
        slide_msg_df = super().parse_msgs_into_df(slide_msgs, 'PngSlideEvent')

        '''
        Remove SlideOn that doesn't have the corresponding SlideOff
        Note: frameCount = -1 is slideOn
        '''
        slide_data = pd.DataFrame()
        for i in range(slide_msg_df.shape[0]):
            try:
                if slide_msg_df['frameCount'][i] == "-1" and slide_msg_df['frameCount'][i+1] == "0":
                    slide_data = pd.concat([slide_data, slide_msg_df.iloc[i:i+2]])
            except:
                print('done')

        slide_data = pd.pivot_table(slide_data,index = ['taskId','slideFileName'], values = 'timestamp',columns = ['frameCount']).astype(int)
        slide_data = slide_data.reset_index().rename(columns={'-1': 'slideOn', '0': 'slideOff'})
        print(slide_data)
        return slide_data

if __name__ == "__main__":
    # x = DatabaseTrialField()
    # msg = x.get_rows('type, msg', 'jkDev.BehMsg')
    # print(msg)

    y = RawSlideData()
    events = y.get()