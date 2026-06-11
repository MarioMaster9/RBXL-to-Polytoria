from .Instance import Instance


class Game(Instance):
    ClassName = "Game"
    def __init__(self, version):
        super().__init__()
        self.Version = version
        self.nonInstanceObjects = []
    def json(self):
        json_self = {
            "Version": self.Version,
            "FileType": 0,
            "Objects": [],
            "NonInstanceObjects": []
        }
        for obj in self.children:
            json_self["Objects"].append(obj.json(self))
        for obj in self.nonInstanceObjects:
            json_self["NonInstanceObjects"].append(obj.json(self))
        return json_self
