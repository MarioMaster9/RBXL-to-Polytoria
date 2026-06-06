from .Instance import Instance
class World(Instance):
    ClassName = "World"
    def __init__(self):
        super().__init__()
        self.Name = "World"
    def findService(self, service):
        return self.findFirstChildOfClass(service)
