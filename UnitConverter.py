import math
import pandas as pd

def mm2pixel(width, height, pixel_width, pixel_height, df):
    hunit = width / pixel_width
    vunit = height / pixel_height
    df['x']= df['x']/hunit
    df['y']= df['y']/vunit
    return df

def deg2mm(deg, distance):
    mm = math.tan((deg / 2) * (math.pi / 180.0)) * 2.0 * distance
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