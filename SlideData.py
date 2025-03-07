from DBUtil import create_server_connection


class SlideData:
    def __init__(self):
        self.task_id = None
        self.time = None
        self.image_path = None
        self.width = None
        self.height = None
        self.head_height = None

    def set_task_id(self, task_id):
        self.task_id = task_id

    def set_time(self, time):
        self.time = time

    def set_image_path(self, image_path):
        self.image_path = image_path

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_head_height(self, head_height):
        self.head_height = head_height

    def get_task_id(self):
        return self.task_id

    def get_time(self):
        return self.time

    def get_image_path(self):
        return self.image_path

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_head_height(self):
        return self.head_height
