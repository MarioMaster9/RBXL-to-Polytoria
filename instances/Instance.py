from .NetworkedObject import NetworkedObject

class Instance(NetworkedObject):
    ClassName = "Instance"
    Properties = [
        ["Tags", "array"]
    ]
    def __init__(self):
        super().__init__()
        self.Tags = []
        self.addProperties(Instance.Properties)