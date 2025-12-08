from maya import cmds
from utils import createCircleCtrl, lockAndHideAttributes
from constants import CTRL_NAMESPACE, SHOULDERS, ARMS, YELLOW


def createShoulderCtrls(jntNameSpace: str):
    shoulderJnts = SHOULDERS

    for i, jnt in enumerate(shoulderJnts):
        # create control circle and zero group
        shoulderCtrl, zeroGrp = createCircleCtrl(rigNameSpace=CTRL_NAMESPACE,
                                                 jntNameSpace=jntNameSpace,
                                                 jntName=jnt,
                                                 radius=10.0,
                                                 color=YELLOW,
                                                 constraint="orient")
        lockAndHideAttributes(shoulderCtrl)
        # set hierarchy
        arm = ARMS[i]
        armZeroGrp = f"{CTRL_NAMESPACE}:zero{arm}Fk"
        cmds.parent(armZeroGrp, shoulderCtrl)
