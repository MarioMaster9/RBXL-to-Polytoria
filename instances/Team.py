from .Instance import Instance
class Team(Instance):
    ClassName = "Team"
    Properties = [
        ["DisplayName", "string"],
        ["Color", "color"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Team.Properties)