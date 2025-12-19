from .limb import MixamoLimb
from maya import cmds
from ..Utils.helpers import createCircleCtrl, lockAndHideAttributes
from ..Utils.constants import YELLOW, FRONT
from ..Utils.shapes import drawCtrlCircle
from ..Utils.limbParams import mixamoLegParams
from .foot import MixamoFoot


class MixamoLeg(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 ctrlNameSpace: str,
                 legConfig: mixamoLegParams):
        super().__init__(jntNameSpace,
                         ctrlNameSpace,
                         legConfig)
        self.toeJnt = legConfig.toeJnt
        self.ballJnt = legConfig.ballJnt
        self.side = legConfig.side
        self.foot = MixamoFoot(self.jntNameSpace,
                               self.ctrlNameSpace,
                               self.thirdJnt,
                               self.ballJnt,
                               self.toeJnt,
                               self.side)

    def createFkCtrls(self):
        jnts = cmds.listRelatives(self._firstJntFkFull, allDescendents=True)
        jnts.append(self._firstJntFkFull)
        for i, Jnt in enumerate(jnts):
            jntName = Jnt.split(":")[-1]
            if (i == 0):
                self.createAnkleFkCtrl(jntName)
            else:
                circleCtrl = createCircleCtrl(self.ctrlNameSpace,
                                              self.jntNameSpace,
                                              jntName,
                                              radius=10.0,
                                              color=YELLOW,
                                              constraint="orient")[0]
                # lockAndHideAttributes(circleCtrl)
        # set hierarchy
        for jnt, parentJnt in zip(jnts, jnts[1:]):
            jntName = jnt.split(":")[-1]
            parentJntName = parentJnt.split(":")[-1]
            zeroGrp = f"{self.ctrlNameSpace}:zero{jntName}"
            parentCtrl = f"{self.ctrlNameSpace}:ctrl{parentJntName}"
            cmds.parent(zeroGrp, parentCtrl)

        # create foot FK
        # TODO: separate it
        self.foot.createFootFk()

    def createAnkleFkCtrl(self, jntName: str):
        # create ankle FK control
        # using a joint as the controller
        # so that the rotation is around world Y and local X,Z
        ctrlJnt = cmds.joint(name=f"{self.ctrlNameSpace}:ctrl{jntName}", p=[0,0,0])
        ctrlCircle = drawCtrlCircle(f"tmpCtrl{jntName}",
                                    radius=10.0,
                                    normal=FRONT,
                                    color=YELLOW)
        cmds.makeIdentity(ctrlCircle, apply=True, r=True)
        self.setupEndJntCtrl(ctrlJnt, jntName, ctrlCircle)

        jntNameFull = f"{self.jntNameSpace}:{jntName}"
        cmds.orientConstraint(ctrlJnt, jntNameFull, mo=True)
        lockAndHideAttributes(ctrlJnt, others=["radius"])

    def createIkCtrls(self):
        super().createIkCtrls()
        self.foot.createFootIk()

    def setupEndJntCtrl(self, ctrlJnt: str, jntName: str, ctrlObj: str):
        # take in a single joint and a ctrl object
        # and set up for ankle control
        # so that it rotates around world Y and local X and Z

        jntNameFull = f"{self.jntNameSpace}:{jntName}"
        cmds.matchTransform(ctrlJnt, jntNameFull)
        loc = cmds.duplicate(ctrlJnt)
        # move the locator up along world Y
        pos = cmds.xform(loc, q=True, ws=True, t=True)
        newPos = (pos[0], pos[1] + 5, pos[2])
        cmds.xform(loc, ws=True, t=newPos)

        # set aim constraint so that the ctrl joint aligns with world Y
        toeJntFull = f"{self.jntNameSpace}:{self.toeJnt}"
        aimConst = cmds.aimConstraint(
            loc,
            ctrlJnt,
            aimVector=[0, 0, 1],
            upVector=[0, 1, 0],
            wut="object",
            wuo=toeJntFull)
        cmds.delete(aimConst)
        cmds.delete(loc)
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
        pass
