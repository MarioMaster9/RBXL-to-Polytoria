colorfmt = '<color name="{0}">\n<R>{1.r:.4f}</R>\n<G>{1.g:.4f}</G>\n<B>{1.b:.4f}</B>\n<A>{1.a:.4f}</A>\n</color>'
vector2fmt = '<vector2 name="{0}">\n<X>{1.x:.4f}</X>\n<Y>{1.y:.4f}</Y>\n</vector2>'
vector3fmt = '<vector3 name="{0}">\n<X>{1.x:.4f}</X>\n<Y>{1.y:.4f}</Y>\n<Z>{1.z:.4f}</Z>\n</vector3>'
floatfmt = '<float name="{0}">{1:.4f}</float>'
intfmt = '<int name="{0}">{1}</int>'
stringfmt = '<string name="{0}">{1}</string>'
booleanfmt = '<boolean name="{0}">{1}</boolean>'
numberrangefmt = '<numberrange name="{0}">\n<Min>\n<float name="Min">{1.min:.4f}</float>\n</Min>\n<Max>\n<float name="Max">{1.max:.4f}</float>\n</Max>\n</numberrange>'
colorrangefmt = '<colorrange name="{0}">\n<Min>\n<color name="Min">\n<R>{1.min.r:.4f}</R>\n<G>{1.min.g:.4f}</G>\n<B>{1.min.b:.4f}</B>\n<A>{1.min.a:.4f}</A>\n</color>\n</Min>\n<Max>\n<color name="Max">\n<R>{1.max.r:.4f}</R>\n<G>{1.max.g:.4f}</G>\n<B>{1.max.b:.4f}</B>\n<A>{1.max.a:.4f}</A>\n</color>\n</Max>\n</colorrange>'

strtransform = str.maketrans({"&": "&amp;", "<": "&lt;", ">": "&gt;"})

bufferSize = 16384

xmlBool = {
    False: "false",
    True: "true"
}

class BufferedXMLWriter:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = ""
        with open(fileName, "w+") as f:
            pass
    def flush(self):
        if len(self.data) > bufferSize:
            with open(self.fileName, "a+") as f:
                f.write(self.data)
            self.data = ""
    def write(self, newData):
        self.data = self.data + newData
        self.flush()
    def writeData(self, xmlData):
        self.write(xmlData + "\n")
    def writeDataOpening(self, xmlData):
        self.write(xmlData + "\n")
    def writeDataClosing(self, xmlData):
        self.write(xmlData + "\n")
    def close(self):
        with open(self.fileName, "a+") as f:
            f.write(self.data)
    def writeBoolean(self, name, value):
        self.writeData(booleanfmt.format(name, xmlBool[value]))
    def writeString(self, name, value):
        self.writeData(stringfmt.format(name, value.translate(strtransform)))
    def writeInt(self, name, value):
        self.writeData(intfmt.format(name, value))
    def writeFloat(self, name, value):
        self.writeData(floatfmt.format(name, value))
    def writeVector3(self, name, value):
        self.writeData(vector3fmt.format(name, value))
    def writeVector2(self, name, value):
        self.writeData(vector2fmt.format(name, value))
    def writeColor(self, name, value):
        self.writeData(colorfmt.format(name, value))
    def writeNumberRange(self, name, value):
        self.writeData(numberrangefmt.format(name, value))
    def writeColorRange(self, name, value):
        self.writeData(colorrangefmt.format(name, value))