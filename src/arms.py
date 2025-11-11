from maya import cmds
from constants import ARMS, ELBOWS, WRISTS, YELLOW, CTRL_NAMESPACE
from utils import createCircleCtrl, createCubeCtrl


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
        break  # FOR TESTING

    createArmIK(jntNameSpace)


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
    annotationShape = cmds.listRelatives(parentXform, children=True)[0]
    cmds.setAttr(f"{annotationShape}.overrideEnabled", 1)
    cmds.setAttr(f"{annotationShape}.overrideDisplayType", 2)


def cleanup():
    # remove all arm FK and IK joints
    fkJoints = cmds.ls("*Fk", recursive=True)
    if fkJoints:
        cmds.delete(fkJoints)
    ikJoints = cmds.ls("*Ik", recursive=True)
    if ikJoints:
        cmds.delete(ikJoints)
    return
