import pandas as pd
import xmltodict

from DatabaseTrialField import DatabaseTrialField


class RawEyeDataDegrees(DatabaseTrialField):

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
        left_eye_data = eye_msg_df[eye_msg_df["id"] == 'leftIscan'].reset_index(drop=True)
        right_eye_data = eye_msg_df[eye_msg_df["id"] == 'rightIscan'].reset_index(drop=True)

        return left_eye_data, right_eye_data

if __name__ == "__main__":

    a = RawEyeDataDegrees()
    left, right = a.get()
    print(left)
    print(right)


