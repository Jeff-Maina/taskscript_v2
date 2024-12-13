import time
import datetime


class Task():
    def __init__(self, id, description, priority, tags=[]):
        self.description = description
        self.tags = tags
        self.isComplete = False
        self._timestamp = int(time.time())
        self._id = id
        self.priority = priority

    def __str__(self):
        return f"{self._id}. {self.description} [{','.join(self.tags)}]"

    def to_json(self):
        return {
            "_id": self._id,
            "_date": time.ctime(self._timestamp),
            "_timestamp": self._timestamp,
            "description": self.description,
            "isStarred": False,
            "tags": self.tags,
            "_isTask": True,
            "isComplete": self.isComplete,
            "inProgress": False,
            "priority": self.priority
        }

