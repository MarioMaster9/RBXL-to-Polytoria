from .FontAsset import FontAsset

class BuiltInFontAsset(FontAsset):
    ClassName = "BuiltInFontAsset"
    Properties = [
        ["FontPreset", "int"],
        ["FontWeight", "int"],
        ["FontStyle", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(BuiltInFontAsset.Properties)