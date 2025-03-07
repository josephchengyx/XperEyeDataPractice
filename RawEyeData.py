from typing import Union

import xmltodict
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

from DatabaseTrialField import DatabaseTrialField
from EyeData import EyeData


class RawEyeData(DatabaseTrialField):

    def __init__(self):
        super().__init__()

    def get(self, db_name):
        beh_msg_eye = super().get_rows('type, msg', f'{db_name}.BehMsgEye')
        eye_device_msgs = beh_msg_eye[beh_msg_eye['type'].str.contains("EyeDeviceMessage")].reset_index(drop=True)
        eye_device_msgs = eye_device_msgs['msg']

        pd.set_option('display.width', 400)
        pd.set_option('display.max_columns', None)
        xml_tag = 'EyeDeviceMessage'
        eye_msg_df = super().parse_msgs_into_df(eye_device_msgs, xml_tag)
        eye_msg_df = eye_msg_df.drop(columns=['volt'])

        '''
        Split data into left vs right
        '''
        eye_msg_df = pd.concat([eye_msg_df, pd.DataFrame((d for idx, d in eye_msg_df['degree'].items()))], axis=1)
        del eye_msg_df['degree']
        leftIscan_data = eye_msg_df[eye_msg_df["id"] == 'leftIscan'].reset_index(drop=True)
        rightIscan_data = eye_msg_df[eye_msg_df["id"] == 'rightIscan'].reset_index(drop=True)

        left_eye = EyeData()
        left_eye.set_eye("Left")
        left_eye.set_unit("degrees")
        left_eye.set_coordinates(np.array(list(zip(map(float, leftIscan_data['x']), map(float, leftIscan_data['y'])))))
        left_eye.set_time(pd.to_numeric(leftIscan_data['timestamp']).to_numpy())

        right_eye = EyeData()
        right_eye.set_eye("Right")
        right_eye.set_unit("degrees")
        right_eye.set_coordinates(np.array(list(zip(map(float, rightIscan_data['x']), map(float, rightIscan_data['y'])))))
        right_eye.set_time(pd.to_numeric(rightIscan_data['timestamp']).to_numpy())

        return left_eye, right_eye
