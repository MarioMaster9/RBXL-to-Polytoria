from .DynamicInstance import DynamicInstance

class Particles(DynamicInstance):
    ClassName = "Particles"
    Properties = [
        ["ImageID", "string"],
        ["ImageType", "int"],
        ["Color", "colorrange"],
        ["ColorMode", "int"],
        ["Lifetime", "numberrange"],
        ["SizeOverLifetime", "numberrange"],
        ["Speed", "numberrange"],
        ["EmissionRate", "int"],
        ["MaxParticles", "int"],
        ["Gravity", "float"],
        ["SimulationSpace", "int"],
        ["StartRotation", "numberrange"],
        ["AngularVelocity", "numberrange"],
        ["Autoplay", "boolean"],
        ["Loop", "boolean"],
        ["Duration", "float"],
        ["Shape", "int"],
        ["ShapeRadius", "float"],
        ["ShapeAngle", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Particles.Properties)