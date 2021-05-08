from datetime import datetime, timedelta
from parameters import MISSION_ROOT_FILEPATH


class Command():
    def __init__(self, mission_type):
        self.mission_type = mission_type

    def __str__(self):
        return f"{self.mission_type}"

    def get_type(self):
        return self.mission_type


class MissionDownlinkCommand(Command):
    def __init__(self, mission_type, num_images, interval, start_timestamp, down_timestamp):
        Command.__init__(mission_type)
        self.num_images = int(num_images)
        self.interval = int(interval)
        self.start_timestamp = self._process_timestamp(start_timestamp)
        self.down_timestamp = self._process_timestamp(down_timestamp)

        # Generate list of images filepath created from this mission
        self.list_mission_datetime = self._generate_mission_images_datetime(
            self.start_timestamp, self.num_images, self.interval)

        # Geneerate mission folder path
        self.mission_folder_path = self._generate_mission_folder_path(
            self.start_timestamp)

    def __str__(self):
        start = self.start_timestamp.strftime("%Y/%m/%d_%H:%M:%S")
        down = self.down_timestamp.strftime("%Y/%m/%d_%H:%M:%S")
        return f"{self.mission_type} | num: {self.num_images} | interval: {self.interval} | start: {start} | down: {down}"

    def _generate_mission_images_datetime(self, start_ts, num, interval):
        """Generate list of filepaths of images to be taken in mission"""
        # Generate list of datetime objects of images to be captured
        # dt = start timestamp + index * interval
        ls = [start_ts]
        curr_dt = start_ts
        for _ in range(num-1):
            ls.append(curr_dt + timedelta(milliseconds=interval))
            curr_dt = curr_dt + timedelta(milliseconds=interval)
        return ls

    def _generate_mission_folder_path(self, start_ts):
        return MISSION_ROOT_FILEPATH + '/' + start_ts.strftime("%Y-%m-%d_%H:%M:%S")

    def _process_timestamp(self, ts):
        """Process timestamp in string to datetime object"""
        chop_timestamp = ts.split('_')
        list_ts = []
        for i in chop_timestamp[0].split('-'):
            list_ts.append(i)
        for i in chop_timestamp[1].split(':'):
            list_ts.append(i)
        list_ts = [int(y) for y in list_ts]

        dt = datetime(list_ts[0], list_ts[1],
                      list_ts[2], list_ts[3], list_ts[4], list_ts[5])
        return dt

    def get_mission_folder_path(self):
        return self.get_mission_folder_path

    def get_mission_datetime(self):
        return self.list_mission_datetime

    def get_down_timestamp(self):
        return self.down_timestamp
