from .InstanceTree import TreeItem

class BinaryTreeItem(TreeItem):
    def __init__(self, className):
        self.custom = {}
        self.children = []
        self.className = className
        if self.className == "Model":
            self.setcustom('hasHumanoid', False)
        self.properties = {}
        self.parent = None
        self.gameObject = None