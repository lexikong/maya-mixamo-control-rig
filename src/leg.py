from limb import MixamoLimb
from maya import cmds
from utils import createCircleCtrl, createCubeCtrl, createCrossCtrl
from constants import YELLOW
from shapes import drawCtrlCube


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
        ctrlJnt = cmds.joint(name=f"{self.ctrlNameSpace}:ctrl{jntName}",p=[0,0,0])
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

    def createIkHandle(self):
        ctrlJnt = cmds.joint(name=f"{self.ctrlNameSpace}:ctrl{self.thirdJnt}Ik", p=[0,0,0])
        cubeCtrl = drawCtrlCube(name=f"{self.ctrlNameSpace}:cube{self.thirdJnt}", size=5.0)
        cmds.makeIdentity(cubeCtrl, apply=True, r=True)
        cubeShape = cmds.listRelatives(cubeCtrl, shapes=True)[0]

        # attach circle shape to joint
        cmds.parent(cubeShape, ctrlJnt, add=True, shape=True)
        # set the joint display to none
        cmds.setAttr(f"{ctrlJnt}.drawStyle", 2)
        cmds.delete(cubeCtrl)

        loc = cmds.spaceLocator(p=[0,0,0])[0]
        grp = cmds.group([ctrlJnt, loc], name=f"{self.ctrlNameSpace}:zero{self.thirdJnt}Ik")
        jntNameFull = f"{self.jntNameSpace}:{self.thirdJnt}"
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

        self.ikCtrl = ctrlJnt

        ikHandle = cmds.ikHandle(name=f"{self.ctrlNameSpace}:ikHandle{self.thirdJnt}",
                                 startJoint=self._firstJntIkFull,
                                 endEffector=self._thirdJntIkFull,
                                 solver="ikRPsolver")[0]
        cmds.parent(ikHandle, ctrlJnt)
        cmds.hide(ikHandle)

        return ikHandle
    
    def endJointOrient(self):
        cmds.orientConstraint(self.ikCtrl, self._thirdJntIkFull, mo=True)

    def createPoleVector(self, ikHandle: str):
        poleVec, poleVecZeroGrp = createCubeCtrl(self.ctrlNameSpace,
                                                 f"{self.secondJnt}PoleVec",
                                                 poleVector=True)
        cmds.matchTransform(poleVecZeroGrp, self._sndJntIkFull)
        cmds.parent(poleVecZeroGrp, self._sndJntIkFull)
        # TODO: put the offset to constants
        # TODO: better way of handling left and right side
        cmds.setAttr(f"{poleVec}.rotateY", 90.0)
        cmds.makeIdentity(poleVec, apply=True, rotate=True)
        cmds.setAttr(f"{poleVecZeroGrp}.translateZ", 60.0)
        cmds.parent(poleVecZeroGrp, world=True)
        cmds.poleVectorConstraint(poleVec, ikHandle)

        return poleVec

    def poleVectorAnnotation(self, poleVec: str):
        annotationShape = cmds.annotate(poleVec, tx="")
        parentXform = cmds.listRelatives(annotationShape, parent=True)
        # rename
        parentXform = cmds.rename(
                    parentXform,
                    f"{self.ctrlNameSpace}:annotation{self.secondJnt}")
        # match transform
        cmds.matchTransform(parentXform, poleVec)
        cmds.parent(parentXform, poleVec, shape=True)
        cmds.pointConstraint(self._sndJntIkFull, parentXform)
        # set drawing mode as reference
        # TODO: put displayType number to constants
        annotationShape = cmds.listRelatives(parentXform, children=True)[0]
        cmds.setAttr(f"{annotationShape}.overrideEnabled", 1)
        cmds.setAttr(f"{annotationShape}.overrideDisplayType", 2)

    def createIkFkBlend(self):
        firstJntFull = f"{self.jntNameSpace}:{self.firstJnt}"
        sndJntFull = f"{self.jntNameSpace}:{self.secondJnt}"
        thirdJntFull = f"{self.jntNameSpace}:{self.thirdJnt}"

        # create orient constraints from IK and FK joints to the original joints
        firstJntConstraint = cmds.orientConstraint(self._firstJntIkFull,
                                                   self._firstJntFkFull,
                                                   firstJntFull)[0]
        cmds.setAttr(f"{firstJntConstraint}.interpType", 2)
        sndJntConstraint = cmds.orientConstraint(
            self._sndJntIkFull, self._sndJntFkFull, sndJntFull)[0]
        cmds.setAttr(f"{sndJntConstraint}.interpType", 2)
        thirdJntConstraint = cmds.orientConstraint(
            self._thirdJntIkFull, self._thirdJntFkFull, thirdJntFull)[0]
        cmds.setAttr(f"{thirdJntConstraint}.interpType", 2)

        # hide IK and FK joints
        cmds.setAttr(f"{self._firstJntIkFull}.visibility", 0)
        cmds.setAttr(f"{self._sndJntIkFull}.visibility", 0)
        cmds.setAttr(f"{self._thirdJntIkFull}.visibility", 0)
        cmds.setAttr(f"{self._firstJntFkFull}.visibility", 0)
        cmds.setAttr(f"{self._sndJntFkFull}.visibility", 0)
        cmds.setAttr(f"{self._thirdJntFkFull}.visibility", 0)

        # create IKFK blend control shape
        blendCtrl, blendZeroGrp = createCrossCtrl(self.ctrlNameSpace,
                                                  f"{self.firstJnt}IkFkBlend",
                                                  size=7.0,
                                                  color=YELLOW)
        # TODO: make it not hard-coded                                          
        # move the blend ctrl somewhere above the arm
        cmds.matchTransform(blendZeroGrp, thirdJntFull, pos=True, rot=False, scl=False)
        currentX = cmds.getAttr(f"{blendZeroGrp}.translateX")
        cmds.setAttr(f"{blendZeroGrp}.translateX", currentX+20.0)
        # lock and hide attributes
        attributesToHide = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'visibility']
        for attr in attributesToHide:
            fullAttrName = f'{blendCtrl}.{attr}'
            cmds.setAttr(fullAttrName, lock=True)
            cmds.setAttr(fullAttrName, keyable=False)

        # create IKFK blend attribute
        blendAttr = "IkFkBlend"
        cmds.addAttr(blendCtrl, longName=blendAttr, minValue=0.0, maxValue=1.0, keyable=True)
        cmds.setAttr(f"{blendCtrl}.{blendAttr}", 0)

        # get the weight attribute names
        firstFkAttr = cmds.listAttr(firstJntConstraint, string="*Fk*")[0]
        firstIkAttr = cmds.listAttr(firstJntConstraint, string="*Ik*")[0]
        sndFkAttr = cmds.listAttr(sndJntConstraint, string="*Fk*")[0]
        sndIkAttr = cmds.listAttr(sndJntConstraint, string="*Ik*")[0]
        thirdFkAttr = cmds.listAttr(thirdJntConstraint, string="*Fk*")[0]
        thirdIkAttr = cmds.listAttr(thirdJntConstraint, string="*Ik*")[0]
        # connect the blend attribute to the constraint weights
        reverseNode = cmds.createNode('reverse', name=f"rvs{self.firstJnt}IkFk")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{reverseNode}.inputX")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{firstJntConstraint}.{firstIkAttr}")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{firstJntConstraint}.{firstFkAttr}")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{sndJntConstraint}.{sndIkAttr}")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{sndJntConstraint}.{sndFkAttr}")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{thirdJntConstraint}.{thirdIkAttr}")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{thirdJntConstraint}.{thirdFkAttr}")

        # connect to visibility of IK and FK ctrls
        # TODO: make zero grp names not hardcoded
        fkZeroGrp = f"{self.ctrlNameSpace}:zero{self.firstJnt}Fk"
        ikZeroGrp = f"{self.ctrlNameSpace}:zero{self.thirdJnt}Ik"
        pvZeroGrp = f"{self.ctrlNameSpace}:zero{self.secondJnt}PoleVec"
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{fkZeroGrp}.visibility")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{ikZeroGrp}.visibility")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{pvZeroGrp}.visibility")
