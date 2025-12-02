from limb import MixamoLimb
from limbParams import mixamoArmParams
from maya import cmds
from utils import createCubeCtrl


class MixamoArm(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 armConfig: mixamoArmParams):
        super().__init__(jntNameSpace, armConfig)

    def createIkCtrlObj(self):
        self.ikCtrl, zeroGrp = createCubeCtrl(self.ctrlNameSpace,
                                              self._thirdJntIkFull.split(":")[-1],
                                              size=10.0)
        cmds.matchTransform(zeroGrp, self._thirdJntIkFull)
