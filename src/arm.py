from limb import MixamoLimb
from maya import cmds


class MixamoArm(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 ctrlNameSpace: str,
                 firstJnt: str,
                 secondJnt: str,
                 thirdJnt: str,
                 ikFkCtrlOffset: tuple):
        super().__init__(jntNameSpace,
                         ctrlNameSpace,
                         firstJnt,
                         secondJnt,
                         thirdJnt,
                         ikFkCtrlOffset)

    def createCtrls(self):
        super().createCtrls()
        self.endJointOrient()

    def endJointOrient(self):
        cmds.orientConstraint(self.ikCtrl, self._thirdJntIkFull)
