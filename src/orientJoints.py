from maya import cmds
from constants import ARMS, ELBOWS, WRISTS


def orientJoints(jntNameSpace: str):
    for arm in ARMS:
        elbowJnt = f"{jntNameSpace}:{ELBOWS[ARMS.index(arm)]}"
        wristJnt = f"{jntNameSpace}:{WRISTS[ARMS.index(arm)]}"
        cmds.setAttr(f"{elbowJnt}.jointOrientX", 0.0)
        cmds.setAttr(f"{wristJnt}.jointOrientX", 0.0)
        cmds.setAttr(f"{elbowJnt}.jointOrientY", 0.0)
        cmds.setAttr(f"{wristJnt}.jointOrientY", 0.0)
