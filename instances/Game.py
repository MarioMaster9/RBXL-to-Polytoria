from .Instance import Instance
class Game(Instance):
    ClassName = "Game"
    def __init__(self, version):
        super().__init__()
        self.Version = version
    def json(self):
        json_self = {
            "Version": self.Version,
            "FileType": 0,
            "Objects": []
        }
        for obj in self.children:
            json_self["Objects"].append(obj.json())
        return json_self
