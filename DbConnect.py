import mysql.connector
import pandas as pd
import math
import xmltodict
import matplotlib.pyplot as plt

def mm2pixel(width, height, pixel_width, pixel_height, df):
    hunit = width / pixel_width;
    vunit = height / pixel_height;
    df['x']= df['x']/hunit;
    df['y']= df['y']/vunit;
    return df

def deg2mm(deg, distance):
    mm = math.tan((deg / 2) * (math.pi / 180.0)) * 2.0 * distance;
    return mm

def deg2mm_coord_xy(coord_list, distance):

    x_pos = []
    y_pos = []
    for line in coord_list:
        x_mm = deg2mm(float(line['x']), distance)
        y_mm = deg2mm(float(line['y']), distance)
        x_pos.append(x_mm)
        y_pos.append(y_mm)

    eye_pos_df = pd.DataFrame({
        'x': x_pos,
        'y': y_pos
    })

    return eye_pos_df

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

def get_column_from_table(column, table, matchcol, matchval, fetch_one = True):
    sql = f'SELECT {column} FROM {table} WHERE {matchcol} = %({matchcol})s'
    cur = connection.cursor()
    cur.execute(sql, {matchcol: matchval})
    if fetch_one:
        row = cur.fetchone()
        return int(row[0])
    else:
        return cur.fetchall()



if __name__ == "__main__":
    host = "localhost"
    user = "xper_rw"
    pw = "up2nite"
    connection = create_server_connection(host, user, pw)
    eye_dev_msgs = get_column_from_table('msg','jkDev.BehMsgEye','type','EyeDeviceMessage', fetch_one = False)

    screen_distance_mm = get_column_from_table('val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_distance')
    screen_height_mm = get_column_from_table('val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_height')
    screen_width_mm = get_column_from_table('val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_width')

    device_msg_list = []
    for x in eye_dev_msgs:
        eye_dev = xmltodict.parse(x[0])
        #print(eye_dev)
        device_msg_list.append(eye_dev['EyeDeviceMessage'])

    left_eye_deg = []
    right_eye_deg = []
    for l in device_msg_list:
        print(l)
        if l['id'] == 'leftIscan':
            left_eye_deg.append(l['degree'])
        elif l['id'] == 'rightIscan':
            right_eye_deg.append(l['degree'])

    print(left_eye_deg)
    print(right_eye_deg)

    left_eye_mm = deg2mm_coord_xy(left_eye_deg, screen_distance_mm)
    right_eye_mm = deg2mm_coord_xy(right_eye_deg, screen_distance_mm)

    im = plt.imread("2.JPG")
    pixel_width = im.shape[0]
    pixel_height = im.shape[1]

    #new_df = mm2pixel(screen_width_mm, screen_height_mm, pixel_width, pixel_height, lefteye_df)
    #print(new_df)

    plt.imshow(im, extent=[-im.shape[1] / 2., im.shape[1] / 2., -im.shape[0] / 2., im.shape[0] / 2.])
    plt.scatter(left_eye_mm['x'],left_eye_mm['y'], linestyle='-', marker='.', c = 'red')
    plt.scatter(right_eye_mm['x'],right_eye_mm['y'], linestyle='-', marker='.', c = 'blue')
    plt.show()

    connection.close()
