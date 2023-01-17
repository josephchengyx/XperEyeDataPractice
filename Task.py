from DBUtil import create_server_connection


class Task:

    def __init__(self, id, start, stop, image_path):
        self.id = id
        self.start = start
        self.stop = stop
        self.image_path = image_path

