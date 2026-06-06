import json
import zstd

class JSONWriter:
    def __init__(self, fileName):
        self.fileName = fileName
    def write(self, data):
        jsonStr = json.dumps(data, indent=2)
        zstdData = zstd.compress(jsonStr.encode('utf-8'))
        with open(self.fileName, 'w') as f:
            f.write(jsonStr)
        if self.fileName != "out/project.ptproj":
            fileName2 = self.fileName.replace('.poly','2.poly')
            with open(fileName2, 'wb+') as f:
                f.write(zstdData)
    def close(self):
        pass