from DBUtil import create_server_connection


class SlideData:
    def __init__(self):
        self.task_id = None
        self.time = None
        self.image_path = None

    def set_task_id(self, task_id):
        self.task_id = task_id

    def set_time(self, time):
        self.time = time

    def set_image_path(self, image_path):
        self.image_path = image_path

    def get_task_id(self):
        return self.task_id

    def get_time(self):
        return self.time

    def get_image_path(self):
        return self.image_path

