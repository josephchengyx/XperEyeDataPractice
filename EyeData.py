class EyeData:

    def __init__(self):
        self.task_id = None
        self.eye = None
        self.coordinates = None
        self.unit = None

    def get_eye(self):
        return self.eye

    def get_task_id(self, task_id):
        return self.task_id

    def get_coordinates(self):
        return self.coordinates

    def get_unit(self):
        return self.unit

    def set_eye(self, eye):
        self.eye = eye

    def set_task_id(self, task_id):
        self.task_id = task_id

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_unit(self, unit):
        self.unit = unit

