from .Dynamic import Dynamic
from .Animator import Animator
class CharacterModel(Dynamic):
    ClassName = "CharacterModel"
    Properties = [
        ["Animator", "ref"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(CharacterModel.Properties)

        animator = Animator()
        animator.Name = "Animator"
        self.addChild(animator)
        self.Animator = animator