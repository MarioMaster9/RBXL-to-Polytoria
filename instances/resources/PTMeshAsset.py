from .MeshAsset import MeshAsset

class PTMeshAsset(MeshAsset):
    ClassName = "PTMeshAsset"
    Properties = {
        "AssetID": "int",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(PTMeshAsset.Properties)