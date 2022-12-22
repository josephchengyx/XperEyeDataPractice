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
            host = host_name,
            user = user_name,
            passwd = user_password
        )
        print("MySQL Database Connection Successful!")
    except ConnectionError as err:
        print(f"Error:" '{err}'"")
    return connection

def deg2mm(deg, distance):

    mm = math.tan((deg / 2) * (math.pi / 180.0)) * 2.0 * distance;

    return mm


if __name__ == "__main__":
    host = "localhost"
    user = "xper_rw"
    pw = "up2nite"
    connection = create_server_connection(host,user,pw)
    cur = connection.cursor()
    cur.execute("SELECT msg FROM jkDev.BehMsgEye WHERE type = %(type)s", {'type' : "EyeDeviceMessage"})
    eye_dev_msgs = cur.fetchall()
    cur.execute("SELECT msg FROM jkDev.BehMsgEye WHERE type = %(type)s", {'type' : "EyeZeroMessage"})
    eye_zero_msgs = cur.fetchall()

    device_msg_list = []
    for x in eye_dev_msgs:
        eye_dev = xmltodict.parse(x[0])
        device_msg_list.append(eye_dev['EyeDeviceMessage'])



    eye_pos_mm_list = []
    x_pos = []
    y_pos = []
    for i in range(len(device_msg_list)):
        x_mm = deg2mm(float(device_msg_list[i]['degree']['x']), 525)
        y_mm = deg2mm(float(device_msg_list[i]['degree']['y']), 525)
        x_pos.append(x_mm)
        y_pos.append(y_mm)
        eye_pos_mm = dict({'x': x_mm, 'y': y_mm})
        eye_pos_mm_list.append(eye_pos_mm)

    df = pd.DataFrame({
        'x_axis': x_pos,
        'y_axis': y_pos
    })

    plt.plot('x_axis','y_axis', data=df, linestyle='-', marker ='.')
    plt.show()



    #print(l[0]['degree']['x'])
        # a = float(eye_dev['EyeDeviceMessage']['degree']['x'])
        # a = deg2mm(a,525)

        #print(eye_dev['EyeDeviceMessage']['degree']['x'])


    # for x in eye_zero_msgs:
    #     eye_zero = parse_XML_rows(x[0])
    #     print(eye_zero['EyeZeroMessage'])


    # cur.execute("DESCRIBE jkDev.BehMsg")
    # for x in cur:
    #     print(x)
    connection.close()
