import json

class ClientRequest:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_json(self):
        return json.dumps({
            "x": self.x,
            "y": self.y
        })