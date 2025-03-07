class EyeData:

    def __init__(self):
        self.eye = None
        self.coordinates = None
        self.time = None
        self.unit = None

    def get_eye(self):
        return self.eye

    def get_coordinates(self):
        return self.coordinates

    def get_time(self):
        return self.time

    def get_unit(self):
        return self.unit

    def set_eye(self, eye):
        self.eye = eye

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_time(self, time):
        self.time = time

    def set_unit(self, unit):
        self.unit = unit
