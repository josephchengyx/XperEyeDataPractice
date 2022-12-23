import math
import mysql.connector
import numpy as np
import pandas as pd
import xmltodict
import matplotlib.pyplot as plt


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database Connection Successful!")
    except ConnectionError as err:
        print(f"Error:" '{err}'"")
    return connection


def deg2mm(deg, distance):
    mm = math.tan((deg / 2) * (math.pi / 180.0)) * 2.0 * distance;

    return mm


def mm2pixel(width, height, pixel_width, pixel_height, df):
    hunit = width / pixel_width;
    vunit = height / pixel_height;
    df['x']= df['x']/hunit;
    df['y']= df['y']/vunit;

    return df


if __name__ == "__main__":
    host = "localhost"
    user = "xper_rw"
    pw = "up2nite"
    connection = create_server_connection(host, user, pw)
    cur = connection.cursor()
    cur.execute("SELECT msg FROM jkDev.BehMsgEye WHERE type = %(type)s", {'type': "EyeDeviceMessage"})
    eye_dev_msgs = cur.fetchall()
    cur.execute("SELECT msg FROM jkDev.BehMsgEye WHERE type = %(type)s", {'type': "EyeZeroMessage"})
    eye_zero_msgs = cur.fetchall()

    device_msg_list = []
    for x in eye_dev_msgs:
        eye_dev = xmltodict.parse(x[0])
        device_msg_list.append(eye_dev['EyeDeviceMessage'])

    eye_pos_mm_list = []
    x_pos = []
    y_pos = []
    distance = 525
    for i in range(len(device_msg_list)):
        # TODO: read the distance from database
        x_mm = deg2mm(float(device_msg_list[i]['degree']['x']), distance)
        y_mm = deg2mm(float(device_msg_list[i]['degree']['y']), distance)
        x_pos.append(x_mm)
        y_pos.append(y_mm)
        eye_pos_mm = dict({'x': x_mm, 'y': y_mm})
        eye_pos_mm_list.append(eye_pos_mm)

    df = pd.DataFrame({
        'x': x_pos,
        'y': y_pos
    })

    print(df)
    #plt.scatter(x_pos,y_pos)
    im = plt.imread("2.JPG")

    pixel_width = 5472
    pixel_height = 3648

    screen_width_mm = 1440
    screen_height_mm = 816

    new_df = mm2pixel(screen_width_mm, screen_height_mm, pixel_width, pixel_height, df)
    print(new_df)


    plt.imshow(im, extent=[-im.shape[1] / 2., im.shape[1] / 2., -im.shape[0] / 2., im.shape[0] / 2.])
    #plt.scatter('.', '.', data=df, linestyle='-', marker='.')
    plt.scatter(df['x'],df['y'], linestyle='-', marker='.')
    plt.show()

    # print(l[0]['degree']['x'])
    # a = float(eye_dev['EyeDeviceMessage']['degree']['x'])
    # a = deg2mm(a,525)

    # print(eye_dev['EyeDeviceMessage']['degree']['x'])

    # for x in eye_zero_msgs:
    #     eye_zero = parse_XML_rows(x[0])
    #     print(eye_zero['EyeZeroMessage'])

    # cur.execute("DESCRIBE jkDev.BehMsg")
    # for x in cur:
    #     print(x)
    connection.close()
