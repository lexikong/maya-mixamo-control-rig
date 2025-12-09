# Assuming all mixamo characters share the same joints naming convention
# Also assuming they all have the same joints
from maya import cmds
from constants import HANDS, FINGERS, NUM_FINGER_JOINTS, CTRL_NAMESPACE, RED
from utils import multiJntFkCtrl


def createFingerCtrls(jntNameSpace: str):
    for hand in HANDS:
        # create a group to hold all ctrls
        ctrlGrp = cmds.group(world=True,
                             empty=True,
                             name=f"{CTRL_NAMESPACE}:{hand}CtrlGrp")
        wristJnt = f"{jntNameSpace}:{hand}"
        cmds.matchTransform(ctrlGrp, wristJnt)

        for fngr in FINGERS:
            fngrJnt = f"{jntNameSpace}:{hand}{fngr}1"
            # cartoon characters only have 4 fingers
            if (not cmds.objExists(fngrJnt)):
                break
            jnts = []
            for i in range(NUM_FINGER_JOINTS-1, 0, -1):
                jnts.append(f"{hand}{fngr}{str(i)}")
            topLvlGrp = multiJntFkCtrl(jnts,
                                       jntNameSpace,
                                       CTRL_NAMESPACE,
                                       radius=2.2,
                                       color=RED)
            cmds.parent(topLvlGrp, ctrlGrp)

        # Parent constrain the control group to the wrist joint
        cmds.parentConstraint(wristJnt, ctrlGrp)
