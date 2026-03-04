class PhysicalProperties:
    def __init__(self):
        self.Friction = 0.3
        self.Elasticity = 0.5
        self.Density = 1
        self.FrictionWeight = 1
        self.ElasticityWeight = 1
        self.AcousticAbsorption = 1
    def get(self, attr):
        return getattr(self, attr)
    @staticmethod
    def FromXML(elem):
        useCustomPhysics = elem.find("CustomPhysics")
        obj = PhysicalProperties()
        if useCustomPhysics == "true":
            for physElem in elem:
                if physElem.tag == "CustomPhysics":
                    continue
                setattr(obj, physElem.tag, float(physElem.text))
        return obj