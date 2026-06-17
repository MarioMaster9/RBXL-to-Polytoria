from ..Instance import Instance
class CaptureService(Instance):
    ClassName = "CaptureService"
    Properties = {
        "CanCapture": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(CaptureService.Properties)
        self.Name = "Capture"
        self.CanCapture = True