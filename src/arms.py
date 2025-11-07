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
        # Create IK handle
        armJntIk = f"{jntNameSpace}:{arm}Ik"
        elbowJntIk = f"{jntNameSpace}:{ELBOWS[ARMS.index(arm)]}Ik"
        elbowJntIkShort = elbowJntIk.split(":")[-1]
        wristJntIk = f"{jntNameSpace}:{WRISTS[ARMS.index(arm)]}Ik"
        wristJntIkShort = wristJntIk.split(":")[-1]
        ikCtrl, zeroGrp = createCubeCtrl(CTRL_NAMESPACE, wristJntIkShort)
        cmds.matchTransform(zeroGrp, wristJntIk)
        ikHandle = cmds.ikHandle(name=f"{CTRL_NAMESPACE}:ikHandle{WRISTS[ARMS.index(arm)]}",
                                 startJoint=armJntIk,
                                 endEffector=wristJntIk,
                                 solver="ikRPsolver")[0]
        cmds.parent(ikHandle, ikCtrl)
        cmds.hide(ikHandle)
        # Create pole vector
        poleVec, poleVecZeroGrp = createCubeCtrl(CTRL_NAMESPACE, f"{elbowJntIkShort}PoleVec")
        cmds.matchTransform(poleVecZeroGrp, elbowJntIk)
        cmds.parent(poleVecZeroGrp, wristJntIk)
        # TODO: put the offset to constants
        cmds.setAttr(f"{poleVecZeroGrp}.translateX", 60.0)
        cmds.parent(poleVecZeroGrp, world=True)
        cmds.poleVectorConstraint(poleVec, ikHandle)
        # TODO: left and right arm orient not symmetric...


def cleanup():
    # remove all arm FK and IK joints
    fkJoints = cmds.ls("*Fk", recursive=True)
    if fkJoints:
        cmds.delete(fkJoints)
    ikJoints = cmds.ls("*Ik", recursive=True)
    if ikJoints:
        cmds.delete(ikJoints)
    return
