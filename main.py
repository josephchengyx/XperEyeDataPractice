from DbConnect import create_server_connection


if __name__ == '__main__':
    host = "localhost"
    user = "xper_rw"
    pw = "up2nite"
    connection = create_server_connection(host, user, pw)
    cur = connection.cursor()
    cur.execute("SELECT msg FROM jkDev.BehMsgEye WHERE type = %(type)s", {'type': "EyeDeviceMessage"})
    eye_dev_msgs = cur.fetchall()
    cur.execute("SELECT msg FROM jkDev.BehMsgEye WHERE type = %(type)s", {'type': "EyeZeroMessage"})
    eye_zero_msgs = cur.fetchall()

