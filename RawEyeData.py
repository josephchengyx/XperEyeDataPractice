from typing import Union

import pandas as pd
import xmltodict
from pandas import Series, DataFrame

from DatabaseTrialField import DatabaseTrialField
from EyeData import EyeData


class RawEyeData(DatabaseTrialField):

    def __init__(self):
        super().__init__()

    def get(self):
        beh_msg_eye = super().get_rows('type, msg', 'jkDev.BehMsgEye')
        eye_device_msgs = beh_msg_eye[beh_msg_eye['type'].str.contains("EyeDeviceMessage")].reset_index(drop=True)
        eye_device_msgs = eye_device_msgs['msg']

        pd.set_option('display.width', 400)
        pd.set_option('display.max_columns', None)
        eye_msg_df = super().parse_msgs_into_df(eye_device_msgs, 'EyeDeviceMessage')
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
        left_eye.set_coordinates(list(zip(leftIscan_data.x, leftIscan_data.y)))

        right_eye = EyeData()
        right_eye.set_eye("Right")
        right_eye.set_unit("degrees")
        right_eye.set_coordinates(list(zip(rightIscan_data.x, rightIscan_data.y)))

        return left_eye, right_eye
