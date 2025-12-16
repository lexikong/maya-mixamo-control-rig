from maya import cmds
from .constants import ARMS, ELBOWS, WRISTS, LEGS, KNEES, ANKLES, BALL, HIP


def orientJoints(jntNameSpace: str):
    # make sure the hip is at world center
    cmds.setAttr(f"{jntNameSpace}:{HIP}.translateX", 0.0)
    cmds.setAttr(f"{jntNameSpace}:{HIP}.translateZ", 0.0)

    for arm in ARMS:
        elbowJnt = f"{jntNameSpace}:{ELBOWS[ARMS.index(arm)]}"
        wristJnt = f"{jntNameSpace}:{WRISTS[ARMS.index(arm)]}"
        cmds.setAttr(f"{elbowJnt}.jointOrientX", 0.0)
        cmds.setAttr(f"{wristJnt}.jointOrientX", 0.0)
        cmds.setAttr(f"{elbowJnt}.jointOrientY", 0.0)
        cmds.setAttr(f"{wristJnt}.jointOrientY", 0.0)
        cmds.setAttr(f"{elbowJnt}.translateX", 0.0)
        cmds.setAttr(f"{wristJnt}.translateX", 0.0)
        cmds.setAttr(f"{elbowJnt}.translateZ", 0.0)
        cmds.setAttr(f"{wristJnt}.translateZ", 0.0)
    for leg in LEGS:
        knee = f"{jntNameSpace}:{KNEES[LEGS.index(leg)]}"
        ankle = f"{jntNameSpace}:{ANKLES[LEGS.index(leg)]}"
        # make sure knee joint orient X is negative
        # so that it won't flip on IK
        # TODO: should I do the same for elbow?
        kneeJointOrientX = cmds.getAttr(f"{knee}.jointOrientX")
        if (kneeJointOrientX > 0):
            cmds.setAttr(f"{knee}.jointOrientX", kneeJointOrientX * -1)
        elif (kneeJointOrientX == 0):
            cmds.setAttr(f"{knee}.jointOrientX", -0.05)
        cmds.setAttr(f"{knee}.jointOrientY", 0.0)
        cmds.setAttr(f"{knee}.jointOrientZ", 0.0)
        cmds.setAttr(f"{ankle}.jointOrientY", 0.0)
        cmds.setAttr(f"{ankle}.jointOrientZ", 0.0)
        cmds.setAttr(f"{knee}.translateX", 0.0)
        cmds.setAttr(f"{ankle}.translateX", 0.0)
        cmds.setAttr(f"{knee}.translateZ", 0.0)
        cmds.setAttr(f"{ankle}.translateZ", 0.0)
        cmds.setAttr(f"{knee}.rotateX", 0.0)
        cmds.setAttr(f"{knee}.rotateY", 0.0)
        cmds.setAttr(f"{knee}.rotateZ", 0.0)
        cmds.setAttr(f"{ankle}.rotateX", 0.0)
        cmds.setAttr(f"{ankle}.rotateY", 0.0)
        cmds.setAttr(f"{ankle}.rotateZ", 0.0)
    # ball joints
    leftBallJnt = f"{jntNameSpace}:Left{BALL}"
    cmds.setAttr(f"{leftBallJnt}.jointOrientY", 0.0)
    cmds.setAttr(f"{leftBallJnt}.jointOrientZ", 0.0)
    rightBallJnt = f"{jntNameSpace}:Right{BALL}"
    cmds.setAttr(f"{rightBallJnt}.jointOrientY", 0.0)
    cmds.setAttr(f"{rightBallJnt}.jointOrientZ", 0.0)

