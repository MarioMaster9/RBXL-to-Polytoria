from .Physical import Physical
from data_types import Vector3
class RigidBody(Physical):
    ClassName = "RigidBody"
    Properties = {
        "Velocity": "vector3",
        "AngularVelocity": "vector3",
        "UseGravity": "boolean",
        "Mass": "float",
        "Friction": "float",
        "Drag": "float",
        "AngularDrag": "float",
        "Bounciness": "float",
        "LockRotation": "boolean",
        "CollisionLayers": "uint",
        "CollisionMask": "uint",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(RigidBody.Properties)
        self.Velocity = Vector3.ZERO
        self.AngularVelocity = Vector3.ZERO
        self.UseGravity = True
        self.Mass = 1
        self.Friction = 0.6
        self.Drag = 0
        self.AngularDrag = 0
        self.Bounciness = 0
        self.LockRotation = False