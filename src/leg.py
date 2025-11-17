from limb import MixamoLimb
from maya import cmds
from utils import createCircleCtrl
from constants import YELLOW


class MixamoLeg(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 ctrlNameSpace: str,
                 firstctrlJnt: str,
                 secondctrlJnt: str,
                 thirdctrlJnt: str,
                 toeJnt: str):
        super().__init__(jntNameSpace,
                         ctrlNameSpace,
                         firstctrlJnt,
                         secondctrlJnt,
                         thirdctrlJnt)
        self.toeJnt = toeJnt

    def createCtrls(self):
        super().createCtrls()
        self.endJointOrient()

    def createFkCtrls(self):
        jnts = cmds.listRelatives(self._firstJntFkFull, allDescendents=True)
        jnts.append(self._firstJntFkFull)
        for i, Jnt in enumerate(jnts):
            jntName = Jnt.split(":")[-1]
            if (i == 0):
                self.createAnkleFkCtrl(jntName)
            else:
                createCircleCtrl(self.ctrlNameSpace,
                                 self.jntNameSpace,
                                 jntName,
                                 radius=10.0,
                                 color=YELLOW,
                                 constraint="orient")
        # set hierarchy
        for jnt, parentJnt in zip(jnts, jnts[1:]):
            jntName = jnt.split(":")[-1]
            parentJntName = parentJnt.split(":")[-1]
            zeroGrp = f"{self.ctrlNameSpace}:zero{jntName}"
            parentCtrl = f"{self.ctrlNameSpace}:ctrl{parentJntName}"
            cmds.parent(zeroGrp, parentCtrl)

    def createAnkleFkCtrl(self, jntName: str):
        # create ankle FK control
        # using a joint as the controller
        # so that the rotation is around world Y and local X,Z
        ctrlJnt = cmds.joint(name=f"{self.ctrlNameSpace}:ctrl{jntName}")
        ctrlCircle = cmds.circle(radius=10.0)
        cmds.makeIdentity(ctrlCircle, apply=True, r=True)
        circleShape = cmds.listRelatives(ctrlCircle, shapes=True)[0]

        # set circle shape color and line width
        cmds.setAttr(f"{circleShape}.overrideEnabled", 1)
        cmds.setAttr(f'{circleShape}.overrideColor', YELLOW)
        cmds.setAttr(f"{circleShape}.lineWidth", 2.0)

        # attach circle shape to joint
        cmds.parent(circleShape, ctrlJnt, add=True, shape=True)
        # set the joint display to none
        cmds.setAttr(f"{ctrlJnt}.drawStyle", 2)
        cmds.delete(ctrlCircle)

        loc = cmds.spaceLocator()[0]
        grp = cmds.group([ctrlJnt, loc], name=f"{self.ctrlNameSpace}:zero{jntName}")
        jntNameFull = f"{self.jntNameSpace}:{jntName}"
        cmds.matchTransform(grp, jntNameFull)

        pos = cmds.xform(loc, q=True, ws=True, t=True)
        newPos = (pos[0], pos[1] + 5, pos[2])
        cmds.xform(loc, ws=True, t=newPos)

        # set aim constraint so that the ctrl joint aligns with world Y
        toeJntFull = f"{self.jntNameSpace}:{self.toeJnt}"
        aimConst = cmds.aimConstraint(loc, ctrlJnt, aimVector=[0,0,1], upVector=[0,1,0], wut="object", wuo=toeJntFull)
        cmds.delete(aimConst)
        cmds.delete(loc)
        # freeze transformation
        cmds.makeIdentity(ctrlJnt, apply=True, r=True)

        cmds.orientConstraint(ctrlJnt, jntNameFull, mo=True)

    def endJointOrient(self):
        pass
