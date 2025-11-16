from maya import cmds
from constants import ARMS, ELBOWS, WRISTS, YELLOW, CTRL_NAMESPACE
from utils import createCircleCtrl, createCubeCtrl, createCrossCtrl


def armsCtrl(jntNameSpace: str):
    # duplicate arm joints for FK and IK
    duplicateArmJoints(jntNameSpace, "Fk")
    duplicateArmJoints(jntNameSpace, "Ik")

    # create controls for FK arms
    for arm in ARMS:
        armJntFk = f"{jntNameSpace}:{arm}Fk"
        jnts = cmds.listRelatives(armJntFk, allDescendents=True)
        jnts.append(armJntFk)
        for jnt in jnts:
            jntName = jnt.split(":")[-1]
            createCircleCtrl(CTRL_NAMESPACE,
                             jntNameSpace,
                             jntName,
                             radius=10.0,
                             color=YELLOW,
                             constraint="orient")
            # TODO: should it be orient constraint?
        # set hierarchy
        for jnt, parentJnt in zip(jnts, jnts[1:]):
            jntName = jnt.split(":")[-1]
            parentJntName = parentJnt.split(":")[-1]
            zeroGrp = f"{CTRL_NAMESPACE}:zero{jntName}"
            parentCtrl = f"{CTRL_NAMESPACE}:ctrl{parentJntName}"
            cmds.parent(zeroGrp, parentCtrl)

    createArmIK(jntNameSpace)

    createIkFkBlend(jntNameSpace)


def duplicateArmJoints(jntNameSpace: str, ctrlType: str):
    for arm in ARMS:
        armJnt = f"{jntNameSpace}:{arm}"
        dupArmJnt = cmds.duplicate(armJnt,
                                   name=f"{jntNameSpace}:{arm}{ctrlType}")[0]
        childJnt = cmds.listRelatives(dupArmJnt)[0]
        # rename forearm and hand joints
        foreArmJnt = cmds.rename(childJnt,
                                 f"{jntNameSpace}:{childJnt}{ctrlType}")
        childJnt = cmds.listRelatives(foreArmJnt)[0]
        handJnt = cmds.rename(childJnt, f"{jntNameSpace}:{childJnt}{ctrlType}")
        fngrJnts = cmds.listRelatives(handJnt,
                                      allDescendents=True,
                                      fullPath=True)
        cmds.delete(fngrJnts)


def createArmIK(jntNameSpace: str):
    for arm in ARMS:
        armJntIk = f"{jntNameSpace}:{arm}Ik"
        elbowJntIk = f"{jntNameSpace}:{ELBOWS[ARMS.index(arm)]}Ik"
        wristJntIk = f"{jntNameSpace}:{WRISTS[ARMS.index(arm)]}Ik"
        wristName = WRISTS[ARMS.index(arm)]
        elbowName = ELBOWS[ARMS.index(arm)]

        # Create IK handle
        ikHandle = createIkHandle(wristName, wristJntIk, armJntIk)
        # Create pole vector
        poleVec = createPoleVector(elbowName, wristJntIk, elbowJntIk, ikHandle)
        # Add annotation to pole vector
        poleVectorAnnotation(poleVec, elbowJntIk, elbowName)


def createIkHandle(wristName: str, wristJntIk: str, armJntIk: str):
    ikCtrl, zeroGrp = createCubeCtrl(CTRL_NAMESPACE, wristJntIk.split(":")[-1])
    cmds.matchTransform(zeroGrp, wristJntIk)
    ikHandle = cmds.ikHandle(name=f"{CTRL_NAMESPACE}:ikHandle{wristName}",
                             startJoint=armJntIk,
                             endEffector=wristJntIk,
                             solver="ikRPsolver")[0]
    cmds.parent(ikHandle, ikCtrl)
    cmds.hide(ikHandle)

    # set orient constraint from ikCtrl to wrist joint
    cmds.orientConstraint(ikCtrl, wristJntIk)
    return ikHandle


def createPoleVector(elbowName: str,
                     wristJntIk: str,
                     elbowJntIk: str,
                     ikHandle: str):
    poleVec, poleVecZeroGrp = createCubeCtrl(CTRL_NAMESPACE,
                                             f"{elbowName}PoleVec",
                                             poleVector=True)
    cmds.matchTransform(poleVecZeroGrp, elbowJntIk)
    cmds.parent(poleVecZeroGrp, wristJntIk)
    # TODO: put the offset to constants
    # TODO: better way of handling left and right side
    if (elbowName == "LeftForeArm"):
        cmds.setAttr(f"{poleVec}.rotateY", 180.0)
        cmds.makeIdentity(poleVec, apply=True, rotate=True)
        cmds.setAttr(f"{poleVecZeroGrp}.translateX", 60.0)
    else:
        cmds.setAttr(f"{poleVecZeroGrp}.translateX", -60.0)
    cmds.parent(poleVecZeroGrp, world=True)
    cmds.poleVectorConstraint(poleVec, ikHandle)
    return poleVec


def poleVectorAnnotation(poleVec: str, elbowJntIk: str, elbowName: str):
    annotationShape = cmds.annotate(poleVec, tx="")
    parentXform = cmds.listRelatives(annotationShape, parent=True)
    # rename
    nameSpace = poleVec.split(":")[0]
    parentXform = cmds.rename(parentXform, f"{nameSpace}:annotation{elbowName}")
    # match transform
    cmds.matchTransform(parentXform, poleVec)
    cmds.parent(parentXform, poleVec, shape=True)
    cmds.pointConstraint(elbowJntIk, parentXform)
    # set drawing mode as reference
    # TODO: put displayType number to constants
    annotationShape = cmds.listRelatives(parentXform, children=True)[0]
    cmds.setAttr(f"{annotationShape}.overrideEnabled", 1)
    cmds.setAttr(f"{annotationShape}.overrideDisplayType", 2)


def createIkFkBlend(jntNameSpace: str):
    for arm in ARMS:
        wrist = WRISTS[ARMS.index(arm)]
        elbow = ELBOWS[ARMS.index(arm)]

        armJnt = f"{jntNameSpace}:{arm}"
        elbowJnt = f"{jntNameSpace}:{elbow}"
        wristJnt = f"{jntNameSpace}:{wrist}"

        armJntIk = f"{jntNameSpace}:{arm}Ik"
        elbowJntIk = f"{jntNameSpace}:{elbow}Ik"
        wristJntIk = f"{jntNameSpace}:{wrist}Ik"

        armJntFk = f"{jntNameSpace}:{arm}Fk"
        elbowJntFk = f"{jntNameSpace}:{elbow}Fk"
        wristJntFk = f"{jntNameSpace}:{wrist}Fk"

        # create orient constraints from IK and FK joints to the original joints
        armConstraint = cmds.orientConstraint(armJntIk, armJntFk, armJnt)[0]
        cmds.setAttr(f"{armConstraint}.interpType", 2)
        elbowConstraint = cmds.orientConstraint(
            elbowJntIk, elbowJntFk, elbowJnt)[0]
        cmds.setAttr(f"{elbowConstraint}.interpType", 2)
        wristConstraint = cmds.orientConstraint(
            wristJntIk, wristJntFk, wristJnt)[0]
        cmds.setAttr(f"{wristConstraint}.interpType", 2)

        # hide IK and FK joints
        cmds.setAttr(f"{armJntIk}.visibility", 0)
        cmds.setAttr(f"{elbowJntIk}.visibility", 0)
        cmds.setAttr(f"{wristJntIk}.visibility", 0)
        cmds.setAttr(f"{armJntFk}.visibility", 0)
        cmds.setAttr(f"{elbowJntFk}.visibility", 0)
        cmds.setAttr(f"{wristJntFk}.visibility", 0)

        # create IKFK blend control shape
        blendCtrl, blendZeroGrp = createCrossCtrl(CTRL_NAMESPACE,
                                                  f"{arm}IkFkBlend",
                                                  size=7.0,
                                                  color=YELLOW)
        # move the blend ctrl somewhere above the arm
        cmds.matchTransform(blendZeroGrp, armJnt, pos=True, rot=False, scl=False)

        currentY = cmds.getAttr(f"{blendZeroGrp}.translateY")
        cmds.setAttr(f"{blendZeroGrp}.translateY", currentY+20.0)
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
        armFkAttr = cmds.listAttr(armConstraint, string="*Fk*")[0]
        armIkAttr = cmds.listAttr(armConstraint, string="*Ik*")[0]
        elbowFkAttr = cmds.listAttr(elbowConstraint, string="*Fk*")[0]
        elbowIkAttr = cmds.listAttr(elbowConstraint, string="*Ik*")[0]
        wristFkAttr = cmds.listAttr(wristConstraint, string="*Fk*")[0]
        wristIkAttr = cmds.listAttr(wristConstraint, string="*Ik*")[0]
        # connect the blend attribute to the constraint weights
        reverseNode = cmds.createNode('reverse', name=f"rvs{arm}IkFk")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{reverseNode}.inputX")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{armConstraint}.{armIkAttr}")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{armConstraint}.{armFkAttr}")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{elbowConstraint}.{elbowIkAttr}")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{elbowConstraint}.{elbowFkAttr}")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{wristConstraint}.{wristIkAttr}")
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{wristConstraint}.{wristFkAttr}")

        # connect to visibility of IK and FK ctrls
        # TODO: make zero grp names not hardcoded
        fkZeroGrp = f"{CTRL_NAMESPACE}:zero{arm}Fk"
        ikZeroGrp = f"{CTRL_NAMESPACE}:zero{wrist}Ik"
        pvZeroGrp = f"{CTRL_NAMESPACE}:zero{elbow}PoleVec"
        cmds.connectAttr(f"{blendCtrl}.{blendAttr}", f"{fkZeroGrp}.visibility")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{ikZeroGrp}.visibility")
        cmds.connectAttr(f"{reverseNode}.outputX", f"{pvZeroGrp}.visibility")


def cleanup():
    # remove all arm FK and IK joints
    fkJoints = cmds.ls("*Fk", recursive=True)
    if fkJoints:
        cmds.delete(fkJoints)
    ikJoints = cmds.ls("*Ik", recursive=True)
    if ikJoints:
        cmds.delete(ikJoints)
    reverseNodes = cmds.ls(type="reverse", recursive=True)
    for node in reverseNodes:
        cmds.delete(node)
    return
