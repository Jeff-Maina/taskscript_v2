import time

class Task():
    def __init__(self, description, tags):
        self.description = description
        self.tags = tags
        self.isComplete = False
        self._timestamp = int(time.time())
        self._id = self._timestamp

    