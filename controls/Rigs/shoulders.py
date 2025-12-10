from maya import cmds
from ..Utils.helpers import createCircleCtrl, lockAndHideAttributes
from ..Utils.constants import SHOULDERS, ARMS, YELLOW


def createShoulderCtrls(jntNameSpace: str, ctrlNameSpace: str):
    shoulderJnts = SHOULDERS

    for i, jnt in enumerate(shoulderJnts):
        # create control circle and zero group
        shoulderCtrl, zeroGrp = createCircleCtrl(rigNameSpace=ctrlNameSpace,
                                                 jntNameSpace=jntNameSpace,
                                                 jntName=jnt,
                                                 radius=10.0,
                                                 color=YELLOW,
                                                 constraint="orient")
        lockAndHideAttributes(shoulderCtrl)
        # set hierarchy
        arm = ARMS[i]
        armZeroGrp = f"{ctrlNameSpace}:zero{arm}Fk"
        cmds.parent(armZeroGrp, shoulderCtrl)
