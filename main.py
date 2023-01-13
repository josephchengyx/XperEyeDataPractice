import xmltodict
from matplotlib import pyplot as plt
import pandas as pd

from DBUtil import create_server_connection, get_column_from_table
from UnitConverter import deg2mm_coord_xy


def get_rows_from_table(cnx, colnames, table):
    sql = f'SELECT {colnames} FROM {table}'

    cur = cnx.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [x.strip() for x in colnames.split(',')]
    return df


if __name__ == "__main__":
    host = "localhost"
    user = "xper_rw"
    pw = "up2nite"
    connection = create_server_connection(host, user, pw)

    events = get_rows_from_table(connection, 'tstamp, type', 'jkDev.BehMsg')
    tasks = get_rows_from_table(connection, 'tstamp, task_id', 'jkDev.TaskDone')

    slide_time = pd.DataFrame()
    for i in range(events.shape[0]):
        #print(i)
        if events.loc[i]['type'] == 'SlideOn' and events.loc[i+1]['type'] == 'SlideOff': # successful slide
            temp = pd.DataFrame(
                {
                'SlideOnTime': [events.loc[i]['tstamp']],
                'SlideOffTime': [events.loc[i+1]['tstamp']]
                }
            )
            slide_time = pd.concat([slide_time, temp])
    print(slide_time)




    eye_dev_msgs = get_column_from_table(connection, 'msg','jkDev.BehMsgEye','type','EyeDeviceMessage', fetch_one = False)

    screen_distance_mm = get_column_from_table(connection, 'val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_distance')
    screen_height_mm = get_column_from_table(connection, 'val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_height')
    screen_width_mm = get_column_from_table(connection, 'val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_width')

    device_msg_list = []
    for x in eye_dev_msgs:
        eye_dev = xmltodict.parse(x[0])
        #print(eye_dev)
        device_msg_list.append(eye_dev['EyeDeviceMessage'])

    # TODO: get the corresponding taskid
    # TODO: get the corresponding image

    left_eye_deg = []
    right_eye_deg = []
    for l in device_msg_list:
        if l['id'] == 'leftIscan':
            left_eye_deg.append(l['degree'])
        elif l['id'] == 'rightIscan':
            right_eye_deg.append(l['degree'])


    left_eye_mm = deg2mm_coord_xy(left_eye_deg, screen_distance_mm)
    right_eye_mm = deg2mm_coord_xy(right_eye_deg, screen_distance_mm)

    im = plt.imread("2.JPG")
    pixel_width = im.shape[0]
    pixel_height = im.shape[1]

    plt.imshow(im, extent=[-im.shape[1] / 2., im.shape[1] / 2., -im.shape[0] / 2., im.shape[0] / 2.])
    plt.scatter(left_eye_mm['x'],left_eye_mm['y'], linestyle='-', marker='.', c = 'red')
    plt.scatter(right_eye_mm['x'],right_eye_mm['y'], linestyle='-', marker='.', c = 'blue')
    plt.show()

    connection.close()