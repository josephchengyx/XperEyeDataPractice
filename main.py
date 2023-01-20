import xmltodict
from matplotlib import pyplot as plt
import pandas as pd

from RawEyeData import RawEyeData
from RawSlideData import RawSlideData
from SystemVar import SystemVar
from UnitConverter import deg2mm_coord_xy, mm2pixel



def extract_eye_data(eye_dev_msgs):

    eye_data = pd.DataFrame()
    for x in eye_dev_msgs:
        eye_dev = xmltodict.parse(x[0])
        #print(eye_dev)
        temp = pd.DataFrame.from_dict(eye_dev['EyeDeviceMessage'])
        eye_data = pd.concat([eye_data, temp])

    return eye_data



if __name__ == "__main__":

    sys_var = SystemVar()

    left_eye_data, right_eye_data = RawEyeData().get()
    slide_data = RawSlideData().get()

    screen_distance_mm = sys_var.get("xper_monkey_screen_distance")
    print(screen_distance_mm)

    # screen_distance_mm = connection.get_column_from_table('val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_distance')
    # screen_height_mm = connection.get_column_from_table('val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_height')
    # screen_width_mm = connection.get_column_from_table('val', 'jkDev.SystemVar', 'name', 'xper_monkey_screen_width')

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
    # plt.scatter(right_eye_mm['x'],right_eye_mm['y'], linestyle='-', marker='.', c = 'blue')
    # plt.show()

    # connection.close()