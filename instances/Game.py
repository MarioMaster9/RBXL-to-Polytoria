class Game:
    def __init__(self, version):
        self.Version = version
        self.nonInstanceObjects = []
        self.children = []
    def addChild(self, obj):
        obj.parent = self
        self.children.append(obj)
    def json(self):
        json_self = {
            "Version": self.Version,
            "FileType": 0,
            "Objects": [],
            "NonInstanceObjects": []
        }
        for obj in self.children:
            obj.resourcePass(self)
        for obj in self.children:
            json_self["Objects"].append(obj.json())
        for obj in self.nonInstanceObjects:
            json_self["NonInstanceObjects"].append(obj.json())
        return json_self
