import pandas as pd
import xmltodict

from DatabaseTrialField import DatabaseTrialField


class RawEyeData(DatabaseTrialField):

    def __init__(self):
        super().__init__()

    def get(self):
        beh_msg_eye = super().get_rows('type, msg', 'jkDev.BehMsgEye')
        eye_device_msgs = beh_msg_eye[beh_msg_eye['type'].str.contains("EyeDeviceMessage")].reset_index(drop=True)
        eye_device_msgs = eye_device_msgs['msg']

        eye_device_msg_list = []
        for msg in eye_device_msgs:
            eye_device_msg = xmltodict.parse(msg)['EyeDeviceMessage']
            eye_device_msg_list.append(eye_device_msg)

        df = pd.DataFrame(eye_device_msg_list)
        pd.set_option('display.max_columns', None)
        df = df.drop(columns=['volt'])

        # left vs right
        df = pd.concat([df, pd.DataFrame((d for idx, d in df['degree'].items()))], axis=1)
        del df['degree']
        left_eye = df[df["id"] == 'leftIscan'].reset_index(drop=True)
        right_eye = df[df["id"] == 'rightIscan'].reset_index(drop=True)

        return left_eye, right_eye

if __name__ == "__main__":

    a = RawEyeData()
    left,right = a.get()


