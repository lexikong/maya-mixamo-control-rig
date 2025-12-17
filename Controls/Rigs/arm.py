from .limb import MixamoLimb
from ..Utils.limbParams import mixamoArmParams
from maya import cmds
from ..Utils.helpers import multiJntFkCtrl


class MixamoArm(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 ctrlNameSpace: str,
                 armConfig: mixamoArmParams):
        super().__init__(jntNameSpace, ctrlNameSpace, armConfig)

    def createFkCtrls(self):
        jntsFull = cmds.listRelatives(self._firstJntFkFull, allDescendents=True)
        jntsFull.append(self._firstJntFkFull)

        # get the jnt names without namespace
        jnts = []
        for jnt in jntsFull:
            jnts.append(jnt.split(":")[-1])
        multiJntFkCtrl(jnts, self.jntNameSpace, self.ctrlNameSpace, radius=10)

    def setupEndJntCtrl(self, ctrlJnt: str, jntName: str, ctrlObj: str):
        # take in a single joint and a ctrl object

        jntNameFull = f"{self.jntNameSpace}:{jntName}"
        cmds.matchTransform(ctrlJnt, jntNameFull)

        # freeze transformation
        cmds.makeIdentity(ctrlJnt, apply=True)

        grp = cmds.group(empty=True, name=f"{self.ctrlNameSpace}:zero{jntName}")
        cmds.matchTransform(grp, ctrlJnt, position=True)
        cmds.parent(ctrlJnt, grp)

        # attach ctrl shape to joint
        ctrlShape = cmds.listRelatives(ctrlObj, shapes=True)[0]
        cmds.parent(ctrlShape, ctrlJnt, add=True, shape=True)
        # set the joint display to none
        cmds.setAttr(f"{ctrlJnt}.drawStyle", 2)
        cmds.delete(ctrlObj)

    def endJointOrient(self):
        cmds.orientConstraint(self.ikCtrl, self._thirdJntIkFull, mo=True)
