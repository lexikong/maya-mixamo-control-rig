from maya import cmds
from constants import ARMS, ELBOWS, WRISTS, LEGS, KNEES, ANKLES


def orientJoints(jntNameSpace: str):
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
        #cmds.setAttr(f"{knee}.jointOrientX", 0.0)
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

