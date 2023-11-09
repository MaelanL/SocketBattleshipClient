import json

class ClientRequest:
    def __init__(self, x=None, y=None, board=None):
        self.x = x
        self.y = y
        self.board = board

    def to_json(self):
        return json.dumps({
            "x": self.x,
            "y": self.y,
            "board": [{"x": cell["x"], "y": cell["y"]} for cell in self.board] if self.board else None
        })