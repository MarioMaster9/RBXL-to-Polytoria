from .NetworkedObject import NetworkedObject
import instances as module_self

class Instance(NetworkedObject):
    ClassName = "Instance"
    Properties = {
        "Tags": "array"
    }
    def __init__(self):
        super().__init__()
        self.Tags = []
        self.addProperties(Instance.Properties)
    @staticmethod
    def New(classType):
        return getattr(module_self, classType)()