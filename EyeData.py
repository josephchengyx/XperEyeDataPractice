class EyeData:

    def __init__(self, taskId, eye, x, y):
        self.taskId = taskId
        self.eye = eye
        self.x = x
        self.y = y


    # Getters and Setters
    def get_eye(self):
        return self.eye

    def set_eye(self, eye):
        self.eye = eye

    def set_taskId(self, taskId):
        self.taskId = taskId

    def get_taskId(self,taskId):
        return taskId

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self,y):
        self.y = y

    def get_y(self):
        return self.y

