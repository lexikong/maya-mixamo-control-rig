from maya import cmds
from constants import ARMS, YELLOW, CTRL_NAMESPACE
from utils import createCircleCtrl


def armsCtrl(jntNameSpace: str):
    # duplicate arm joints for FK and IK
    duplicateArmJoints(jntNameSpace, "Fk")
    # duplicateArmJoints(jntNameSpace, "Ik")

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
