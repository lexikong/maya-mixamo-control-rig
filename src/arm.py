from limb import MixamoLimb
from limbParams import mixamoArmParams


class MixamoArm(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 armConfig: mixamoArmParams):
        super().__init__(jntNameSpace, armConfig)
