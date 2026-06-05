import json

class JSONWriter:
    def __init__(self, fileName):
        self.fileName = fileName
    def write(self, data):
        with open(self.fileName, 'w') as f:
            json.dump(data, f, indent=4)
    def close(self):
        pass