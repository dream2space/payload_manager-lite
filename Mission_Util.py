from datetime import datetime


def execute_mission(cam, mission_folder_path, timestamp, count):
    '''Function to execute imaging mission at given timestamp at datetime'''
    name_image = mission_folder_path + '/' + \
        str(timestamp).replace(" ", "_") + "_" + str(count) + '.jpg'
    cam.capture(name_image, resize=(640, 480))
    print(f'Image at {name_image} taken at {datetime.utcnow()}')
    print()
