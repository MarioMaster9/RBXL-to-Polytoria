from .Instance import Instance
class NetworkEvent(Instance):
    ClassName = "NetworkEvent"
    Properties = [
        ["Reliable", "boolean"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(NetworkEvent.Properties)
        self.Reliable = True