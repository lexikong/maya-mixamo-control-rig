from .limb import MixamoLimb
from ..Utils.limbParams import mixamoArmParams
from maya import cmds
from ..Utils.helpers import (
    createCubeCtrl,
    multiJntFkCtrl,
    lockAndHideAttributes
)


class MixamoArm(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 armConfig: mixamoArmParams):
        super().__init__(jntNameSpace, armConfig)

    def createFkCtrls(self):
        jntsFull = cmds.listRelatives(self._firstJntFkFull, allDescendents=True)
        jntsFull.append(self._firstJntFkFull)

        # get the jnt names without namespace
        jnts = []
        for jnt in jntsFull:
            jnts.append(jnt.split(":")[-1])
        multiJntFkCtrl(jnts, self.jntNameSpace, self.ctrlNameSpace, radius=10)

    def createIkCtrlObj(self):
        self.ikCtrl, zeroGrp = createCubeCtrl(self.ctrlNameSpace,
                                              self._thirdJntIkFull.split(":")[-1],
                                              size=10.0)
        cmds.matchTransform(zeroGrp, self._thirdJntIkFull)
        lockAndHideAttributes(self.ikCtrl, translate=False)

    def endJointOrient(self):
        cmds.orientConstraint(self.ikCtrl, self._thirdJntIkFull, mo=True)
