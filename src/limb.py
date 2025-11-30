from maya import cmds
from abc import ABC, abstractmethod
from utils import createCircleCtrl, createCubeCtrl, createCrossCtrl
from constants import YELLOW
from limbParams import mixamoLimbParams


class MixamoLimb(ABC):

    def __init__(self,
                 jntNameSpace: str,
                 limbConfig: mixamoLimbParams):
        self.jntNameSpace = jntNameSpace
        self.ctrlNameSpace = limbConfig.ctrlNameSpace
        self.firstJnt = limbConfig.firstJnt
        self.secondJnt = limbConfig.secondJnt
        self.thirdJnt = limbConfig.thirdJnt
        self.pvRotateY = limbConfig.pvRotateY
        self.pvOffset = limbConfig.pvOffset
        # the location of IKFK control shape offset from the first joint
        self.ikFkCtrlOffset = limbConfig.ikFkCtrlOffset

    def createCtrls(self):
        # duplicate joints for FK and IK controls
        (self._firstJntFkFull,
         self._sndJntFkFull,
         self._thirdJntFkFull) = self.duplicateThreeJointChain("Fk")
        (self._firstJntIkFull,
         self._sndJntIkFull,
         self._thirdJntIkFull) = self.duplicateThreeJointChain("Ik")
        # create FK controls
        self.createFkCtrls()
        self.createIkCtrls()
        # create IKFK blend ctrl
        self.createIkFkBlend()

        self.endJointOrient()

    def duplicateThreeJointChain(self, postFix: str):
        # duplicate a three-joint chain and rename with postFix
        # delete all children joints from the 4-th joint
        # used for preparing FK and IK arm and leg joints
        firstJntFull = f"{self.jntNameSpace}:{self.firstJnt}"
        dupFirstJnt = cmds.duplicate(firstJntFull,
                                     name=f"{self.jntNameSpace}:{self.firstJnt}{postFix}")[0]
        # rename the second and third joints
        childJnt = cmds.listRelatives(dupFirstJnt)[0]
        secondJnt = cmds.rename(childJnt,
                                f"{self.jntNameSpace}:{childJnt}{postFix}")
        childJnt = cmds.listRelatives(secondJnt)[0]
        thirdJnt = cmds.rename(childJnt, f"{self.jntNameSpace}:{childJnt}{postFix}")
        allOtherJnts = cmds.listRelatives(thirdJnt,
                                          allDescendents=True,
                                          fullPath=True)
        cmds.delete(allOtherJnts)
        return dupFirstJnt, secondJnt, thirdJnt

    def createFkCtrls(self):
        # TODO: use the new util function
        jnts = cmds.listRelatives(self._firstJntFkFull, allDescendents=True)
        jnts.append(self._firstJntFkFull)
        for jnt in jnts:
            jntName = jnt.split(":")[-1]
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

    def createIkCtrls(self):
        # Create IK handle
        ikHandle = self.createIkHandle()
        # Create pole vector
        poleVec = self.createPoleVector(ikHandle)
        # Add annotation to pole vector
        self.poleVectorAnnotation(poleVec)

    def createIkHandle(self):
        self.createIkCtrlObj()
        ikHandle = self.setupIkHandle()
        return ikHandle

    @abstractmethod
    def createIkCtrlObj(self):
        pass

    def setupIkHandle(self):
        ikHandle = cmds.ikHandle(name=f"{self.ctrlNameSpace}:ikHandle{self.thirdJnt}",
                                 startJoint=self._firstJntIkFull,
                                 endEffector=self._thirdJntIkFull,
                                 solver="ikRPsolver")[0]
        cmds.parent(ikHandle, self.ikCtrl)
        cmds.hide(ikHandle)
        return ikHandle

    def createPoleVector(self, ikHandle: str):
        poleVec, poleVecZeroGrp = createCubeCtrl(self.ctrlNameSpace,
                                                 f"{self.secondJnt}PoleVec",
                                                 poleVector=True)
        cmds.matchTransform(poleVecZeroGrp, self._sndJntIkFull)
        cmds.parent(poleVecZeroGrp, self._sndJntIkFull)

        # set the pole vector location
        cmds.setAttr(f"{poleVec}.rotateY", self.pvRotateY)
        cmds.makeIdentity(poleVec, apply=True, rotate=True)
        cmds.setAttr(f"{poleVecZeroGrp}.translate",
                     self.pvOffset[0],
                     self.pvOffset[1],
                     self.pvOffset[2])
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
        
        # put the blend control around the first joint plus offset
        cmds.matchTransform(blendZeroGrp, firstJntFull, pos=True, rot=False, scl=False)

        currentTranslate = cmds.getAttr(f"{blendZeroGrp}.translate")[0]
        newTranslate = [a + b for a, b in zip(currentTranslate, self.ikFkCtrlOffset)]
        cmds.setAttr(f"{blendZeroGrp}.translate", newTranslate[0], newTranslate[1],newTranslate[2])
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

    def endJointOrient(self):
        cmds.orientConstraint(self.ikCtrl, self._thirdJntIkFull, mo=True)
