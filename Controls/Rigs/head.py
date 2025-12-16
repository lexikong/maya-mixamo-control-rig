from maya import cmds
from ..Utils.helpers import multiJntFkCtrl, setFkCtrlHierarchy, lockAndHideAttributes
from ..Utils.constants import HEAD, HEAD_END, NECK, VIOLET, SPINES
from ..Utils.shapes import drawCtrlBox
import math


def createHeadCtrls(jntNameSpace: str, ctrlNameSpace: str):
    createNeckCtrl(jntNameSpace, ctrlNameSpace)
    createHeadBox(jntNameSpace, ctrlNameSpace)
    setNeckHeadHierarchy(jntNameSpace, ctrlNameSpace)


def createNeckCtrl(jntNameSpace: str, ctrlNameSpace: str):
    # create neck ctrl
    neckJnt = NECK
    multiJntFkCtrl(neckJnt, jntNameSpace, ctrlNameSpace, radius=15, color=VIOLET)


def createHeadBox(jntNameSpace: str, ctrlNameSpace: str):
    # get the distance between head and head_end joints
    headTopJnt = HEAD_END
    headTopJntFull = f"{jntNameSpace}:{headTopJnt}"
    translateY = cmds.getAttr(f"{headTopJntFull}.translateY")
    translateZ = cmds.getAttr(f"{headTopJntFull}.translateZ")
    dist = math.hypot(translateY, translateZ)

    # create the control box and zero group
    headJnt = HEAD
    ctrlBox = drawCtrlBox(name=f"{ctrlNameSpace}:ctrl{headJnt}",
                          size=[dist, dist, dist],
                          color=VIOLET,
                          pivot="bottom")
    zeroGrp = cmds.group(empty=True, name=f"{ctrlNameSpace}:zero{headJnt}")
    cmds.matchTransform(zeroGrp, ctrlBox)
    cmds.parent(ctrlBox, zeroGrp)

    # match transformation
    headJntFull = f"{jntNameSpace}:{headJnt}"
    cmds.matchTransform(zeroGrp, headJntFull)

    # add orient constraint
    cmds.orientConstraint(ctrlBox, headJntFull)

    # lock and hide unused attributes
    lockAndHideAttributes(ctrlBox)


def setNeckHeadHierarchy(jntNameSpace, ctrlNameSpace):
    jnts = []
    jnts.append(HEAD)
    jnts.append(NECK[0])
    setFkCtrlHierarchy(jnts, jntNameSpace, ctrlNameSpace)
