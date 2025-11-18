# Assuming all mixamo characters share the same joints naming convention
# Also assuming they all have the same joints
from maya import cmds
from constants import *  # noqa: F403, F405


# TODO: cartoon characters e.g. Doopy only has 4 fingers
def fingers(parentGrp: str, jntNameSpace: str):
    # TODO: try mirroring to the other side instead of running all over again
    for hand in HANDS:
        for fngr in FINGERS:
            for i in range(1, NUM_FINGER_JOINTS):
                fngrJntName = f"{hand}{fngr}{str(i)}"
                createCircleCtrl(CTRL_NAMESPACE, jntNameSpace, fngrJntName)
    # Set hierarchy to ctrls
    for hand in HANDS:
        # Create a group for all finger controls,
        # and match transform to the wrist joint
        ctrlGrp = cmds.group(world=True,
                             empty=True,
                             name=f"{CTRL_NAMESPACE}:{hand}CtrlGrp")
        wristJnt = f"{jntNameSpace}:{hand}"
        cmds.matchTransform(ctrlGrp, wristJnt)

        for fngr in FINGERS:
            for i in range(NUM_FINGER_JOINTS-1, 1, -1):
                setFingerCtrlHierarchy(CTRL_NAMESPACE, hand, fngr, i)
            # Put the finger controls into one group
            topLvlFngr = f"{CTRL_NAMESPACE}:zero{hand}{fngr}1"
            cmds.parent(topLvlFngr, ctrlGrp)

        # Parent constrain the control group to the wrist joint
        cmds.parentConstraint(wristJnt, ctrlGrp)


def createCircleCtrl(rigNameSpace: str, jntNameSpace: str, jntName: str):
    # TODO: use the function from utils.py
    # create nurbs circle and zero group
    # TODO: non-hardcoded radius
    if ("Thumb1" in jntName):
        radius = 2.2
    else:
        radius = 1.8
    nurbsCircle = cmds.circle(name=f"{rigNameSpace}:ctrl{jntName}",
                              normal=UP,
                              radius=radius)
    # set color to be red
    # TODO: allow user to customize color
    shapeNode = cmds.listRelatives(nurbsCircle, shapes=True)[0]
    cmds.setAttr(f"{shapeNode}.overrideEnabled", 1)
    cmds.setAttr(f'{shapeNode}.overrideColor', RED)
    zeroGrp = cmds.group(nurbsCircle, name=f"{rigNameSpace}:zero{jntName}")
    # match transformation
    jntNameFull = f"{jntNameSpace}:{jntName}"
    cmds.matchTransform(zeroGrp, jntNameFull)
    # set parent constraint
    cmds.parentConstraint(nurbsCircle, jntNameFull)


def setFingerCtrlHierarchy(rigNameSpace: str, hand: str, fngr: str, index: int):
    zeroGrp = f"{rigNameSpace}:zero{hand}{fngr}{str(index)}"
    parentCtrl = f"{rigNameSpace}:ctrl{hand}{fngr}{str(index-1)}"
    cmds.parent(zeroGrp, parentCtrl)
