from ..NetworkedObject import NetworkedObject

class BaseAsset(NetworkedObject):
    ClassName = "BaseAsset"
    def __init__(self):
        super().__init__()
        self.setRandomName()
        self.parent = None
        self.included = False