import xmltodict
import pandas as pd
import numpy as np

from DatabaseTrialField import DatabaseTrialField
from SlideData import SlideData


class RawSlideData(DatabaseTrialField):

    def __init__(self):
        super().__init__()

    def get(self, db_name):
        beh_msg = super().get_rows('type, msg', f'{db_name}.BehMsg')
        slide_msgs = beh_msg[(beh_msg['type'].str.contains("Slide")) & (beh_msg['msg'].str.contains("PngSlideEvent"))].reset_index(drop=True)
        slide_msgs, slide_type = slide_msgs['msg'], slide_msgs['type']

        pd.set_option('display.width', 400)
        pd.set_option('display.max_columns', None)
        slide_msg_df = super().parse_msgs_into_df(slide_msgs, 'PngSlideEvent')
        slide_msg_df = pd.concat([slide_msg_df.drop(columns=['spec']), pd.json_normalize(slide_msg_df['spec'])], axis=1)
        slide_msg_df[['taskId', 'timestamp', 'height', 'width', 'headHeight']] \
            = slide_msg_df[['taskId', 'timestamp', 'height', 'width', 'headHeight']].apply(pd.to_numeric)
        # slide_msg_df['timestamp'] = slide_msg_df['timestamp'] - slide_msg_df['timestamp'][0]

        '''
        Remove SlideOn that doesn't have the corresponding SlideOff
        Note: frameCount = -1 is slideOn
        '''
        slide_data = pd.DataFrame()
        for i in range(slide_msg_df.shape[0]-1):
            if (slide_msg_df['taskId'][i] == slide_msg_df['taskId'][i+1]) and (slide_type[i] == 'SlideOn' and slide_type[i+1] == 'SlideOff'):
                slide_msg_df.loc[i,'frameCount'] = '-1'
                slide_data = pd.concat([slide_data, slide_msg_df.iloc[i:i+2]])
        print('done')

        slide_data = pd.pivot_table(slide_data, index=['taskId', 'filePath', 'height', 'width', 'headHeight'], values='timestamp',
                                    columns=['frameCount']).astype(int)
        slide_data = slide_data.reset_index().rename(columns={'-1': 'slideOn', '0': 'slideOff'})
        slide_data = slide_data.sort_values(by='slideOn')
        slide_data.columns.name = 'slideNumber'
        # print(slide_data)

        s = SlideData()
        s.set_time(np.array(list(zip(slide_data['slideOn'], slide_data['slideOff']))))
        s.set_task_id(slide_data['taskId'].to_numpy())
        s.set_image_path(slide_data['filePath'].to_numpy())
        s.set_width(slide_data['width'].to_numpy())
        s.set_height(slide_data['height'].to_numpy())
        s.set_head_height(slide_data['headHeight'].to_numpy())

        return s

if __name__ == "__main__":
    # x = DatabaseTrialField()
    # msg = x.get_rows('type, msg', 'jkDev.BehMsg')
    # print(msg)

    db_name = '20230926_recording'
    y = RawSlideData()
    slide = y.get(db_name)
    print(slide.get_time())
    print(slide.get_task_id())
    print(slide.get_image_path())
    # print(type(slide.get_image_path()))
    # print(type(slide.get_task_id()))
    # print(type(slide.get_time()))
