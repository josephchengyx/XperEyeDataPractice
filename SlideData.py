from DBUtil import create_server_connection


class SlideData:

    def __init__(self, task_id, slide_on_time, slide_off_time, image_path):
        self.task_id = task_id
        self.slide_on_time = slide_on_time
        self.slide_off_time = slide_off_time
        self.image_path = image_path

    def set_task_id(self, task_id):
        self.task_id = task_id

    def set_slide_on_time(self, slide_on_time):
        self.slide_on_time = slide_on_time

    def set_slide_off_time(self, slide_off_time):
        self.slide_off_time = slide_off_time

    def set_image_path(self, image_path):
        self.image_path = image_path

    def get_task_id(self):
        return self.task_id

    def get_slide_on_time(self):
        return self.slide_on_time

    def get_slide_off_time(self):
        return self.slide_off_time

    def get_image_path(self):
        return self.image_path

