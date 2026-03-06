from .Instance import Instance

class Game(Instance):
    ClassName = "Game"
    def __init__(self, version):
        super().__init__()
        self.Version = version
    def findService(self, service):
        return self.findFirstChildOfClass(service)
    def write(self, writer):
        writer.writeData('<?xml version="1.0" encoding="UTF-8"?>')
        writer.writeData(f'<game version="{self.Version}">')
        for obj in self.children:
            obj.write(writer)
        writer.writeDataClosing("</game>")