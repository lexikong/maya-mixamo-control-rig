from limb import MixamoLimb
from maya import cmds
from utils import createCircleCtrl, createCubeCtrl, createCrossCtrl
from constants import YELLOW
from shapes import drawCtrlCube
from limbParams import mixamoLegParams


class MixamoLeg(MixamoLimb):
    def __init__(self,
                 jntNameSpace: str,
                 legConfig: mixamoLegParams):
        super().__init__(jntNameSpace,
                         legConfig)
        self.toeJnt = legConfig.toeJnt

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
        ctrlJnt = cmds.joint(name=f"{self.ctrlNameSpace}:ctrl{jntName}",p=[0,0,0])
        ctrlCircle = cmds.circle(radius=10.0)
        cmds.makeIdentity(ctrlCircle, apply=True, r=True)
        self.setupAnkleCtrl(ctrlJnt, jntName, ctrlCircle)

        jntNameFull = f"{self.jntNameSpace}:{jntName}"
        cmds.orientConstraint(ctrlJnt, jntNameFull, mo=True)

    def createIkHandle(self):
        ctrlJnt = cmds.joint(name=f"{self.ctrlNameSpace}:ctrl{self.thirdJnt}Ik", p=[0,0,0])
        cubeCtrl = drawCtrlCube(name=f"{self.ctrlNameSpace}:cube{self.thirdJnt}", size=5.0)
        cmds.makeIdentity(cubeCtrl, apply=True, r=True)
        self.setupAnkleCtrl(ctrlJnt, f"{self.thirdJnt}Ik", cubeCtrl)

        self.ikCtrl = ctrlJnt

        ikHandle = cmds.ikHandle(name=f"{self.ctrlNameSpace}:ikHandle{self.thirdJnt}",
                                 startJoint=self._firstJntIkFull,
                                 endEffector=self._thirdJntIkFull,
                                 solver="ikRPsolver")[0]
        cmds.parent(ikHandle, ctrlJnt)
        cmds.hide(ikHandle)

        return ikHandle

    def setupAnkleCtrl(self, ctrlJnt: str, jntName: str, ctrlObj: str):
        # attach ctrl shape to joint
        ctrlShape = cmds.listRelatives(ctrlObj, shapes=True)[0]
        cmds.parent(ctrlShape, ctrlJnt, add=True, shape=True)
        # set the joint display to none
        cmds.setAttr(f"{ctrlJnt}.drawStyle", 2)
        cmds.delete(ctrlObj)

        loc = cmds.spaceLocator()[0]
        grp = cmds.group([ctrlJnt, loc], name=f"{self.ctrlNameSpace}:zero{jntName}")
        jntNameFull = f"{self.jntNameSpace}:{jntName}"
        cmds.matchTransform(grp, jntNameFull)
        # move the locator up along world Y
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
