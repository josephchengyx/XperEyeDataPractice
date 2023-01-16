import xmltodict
from matplotlib import pyplot as plt
import pandas as pd

from DBUtil import create_server_connection, get_column_from_table
from UnitConverter import deg2mm_coord_xy, mm2pixel


def get_rows_from_table(cnx, colnames, table):
    sql = f'SELECT {colnames} FROM {table}'

    cur = cnx.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [x.strip() for x in colnames.split(',')]
    return df

def extract_slide_events(events):
    slide_msg = pd.DataFrame()
    for i in range(events.shape[0]):
        try:
            if events.iloc[i]['type'] == 'SlideOn' and events.iloc[i + 1]['type'] == 'SlideOff':  # successful slide
                temp = pd.DataFrame(
                    {
                        'SlideOnMsg': [events.loc[i]['msg']],
                        'SlideOffMsg': [events.loc[i + 1]['msg']]
                    }
                )
                slide_msg = pd.concat([slide_msg, temp])
        except:
            print("Note: the experiment ends with 'slideOn' ")
    # print(slide_msg)

    slide_detail_dict_list = []
    for i in range(len(slide_msg.columns)):
        for line in slide_msg.iloc[:, i]:
            slide_details = xmltodict.parse(line)['PngSlideEvent']
            slide_detail_dict_list.append(slide_details)

    # print(slide_detail_dict_list)
    slide_df = pd.DataFrame.from_dict(slide_detail_dict_list)
    pd.set_option('display.max_columns', None)
    slide_df = slide_df.sort_values(by=['timestamp'])
    print(slide_df.head())
    return slide_df

def extract_eye_data(eye_dev_msgs):

    eye_data = pd.DataFrame()
    for x in eye_dev_msgs:
        eye_dev = xmltodict.parse(x[0])
        #print(eye_dev)
        temp = pd.DataFrame.from_dict(eye_dev['EyeDeviceMessage'])
        eye_data = pd.concat([eye_data, temp])

    return eye_data



if __name__ == "__main__":
    host = "localhost"
    user = "xper_rw"
    pw = "up2nite"
    connection = create_server_connection(host, user, pw)

    events = get_rows_from_table(connection, 'type, msg', 'jkDev.BehMsg')
    slide_events = extract_slide_events(events)

    # EYE DEVICE MESSAGE
    eye_dev_msgs = get_column_from_table(connection, 'msg','jkDev.BehMsgEye','type','EyeDeviceMessage', fetch_one = False)

    screen_distance_mm = get_column_from_table(connection, 'val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_distance')
    screen_height_mm = get_column_from_table(connection, 'val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_height')
    screen_width_mm = get_column_from_table(connection, 'val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_width')

    eye_data = extract_eye_data(eye_dev_msgs)



    print(eye_data.loc[eye_data['id'] == 'leftIscan'])


    # left_eye_deg = []
    # right_eye_deg = []
    # for l in device_msg_list:
    #     if int(l['timestamp']) > 1673646612905728 and int(l['timestamp']) < 1673646617905947:
    #         if l['id'] == 'leftIscan':
    #             left_eye_deg.append(l['degree'])
    #         elif l['id'] == 'rightIscan':
    #             right_eye_deg.append(l['degree'])
    #
    #
    # left_eye_mm = deg2mm_coord_xy(left_eye_deg, screen_distance_mm)
    # right_eye_mm = deg2mm_coord_xy(right_eye_deg, screen_distance_mm)

    # TODO: CHANGE MM TO PIXEL
    # im = plt.imread("2.JPG")
    # pixel_width = im.shape[0]
    # pixel_height = im.shape[1]
    #
    # left_eye_mm = mm2pixel(1016, 572, 3840, 2160, left_eye_mm)
    # #right_eye_mm = mm2pixel(76, 114, pixel_width, pixel_height, right_eye_mm)
    #
    # plt.imshow(im, extent=[-im.shape[1] / 2., im.shape[1] / 2., -im.shape[0] / 2., im.shape[0] / 2.])
    # plt.scatter(left_eye_mm['x'],left_eye_mm['y'], linestyle='-', marker='.', c = 'red')
    # #plt.scatter(right_eye_mm['x'],right_eye_mm['y'], linestyle='-', marker='.', c = 'blue')
    # plt.show()

    connection.close()