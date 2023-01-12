from DbConnect import create_server_connection


host = "localhost"
user = "xper_rw"
pw = "up2nite"
connection = create_server_connection(host, user, pw)
cur = connection.cursor()
def get_col_from_table(col, table, matchcol, matchval, just_one = True):
    sql = f'SELECT {col} FROM {table} WHERE {matchcol} = %({matchcol})s'
    cur.execute(sql, {matchcol: matchval})
    if just_one == 'one':
        row = cur.fetchone()
        return row and row[0]
    else:
        return cur.fetchall()

screen_height_mm = get_col_from_table('val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_height')
dev_msgs = get_col_from_table('msg', 'jkDev.BehMsgEye', 'type', 'EyeDeviceMessage', just_one = False)
#
#
# query = ("SELECT val FROM jkDev.SystemVar "
#          "WHERE name = %(name)s")
# name = {'name': "xper_monkey_screen_height"}
# cur.execute(query, name)
# screen_height_mm = int(cur.fetchone()[0])
# # cur.execute("SELECT val FROM jkDev.SystemVar WHERE name = %(name)s", {'name': "xper_monkey_screen_height"})
# # screen_height_mm = int(cur.fetchone()[0])
# cur.execute("SELECT val FROM jkDev.SystemVar WHERE name = %(name)s", {'name': "xper_monkey_screen_width"})
# screen_width_mm = int(cur.fetchone()[0])
# cur.execute("SELECT val FROM jkDev.SystemVar WHERE name = %(name)s", {'name': "xper_monkey_screen_distance"})
# screen_distance_mm = int(cur.fetchone()[0])
#
# print(screen_distance_mm)
# print(screen_width_mm)
# print(screen_height_mm)
#
#
