from maya import cmds
from utils import multiJntFkCtrl, setFkCtrlHierarchy
from constants import CTRL_NAMESPACE, HEAD, HEAD_END, NECK, VIOLET, SPINES
from shapes import drawCtrlBox
import math


def createHeadCtrls(jntNameSpace: str):
    createNeckCtrl(jntNameSpace)
    createHeadBox(jntNameSpace)
    setNeckHeadHierarchy(jntNameSpace)


def createNeckCtrl(jntNameSpace: str):
    # create neck ctrl
    neckJnt = NECK
    multiJntFkCtrl(neckJnt, jntNameSpace, CTRL_NAMESPACE, radius=15, color=VIOLET)


def createHeadBox(jntNameSpace: str):
    # get the distance between head and head_end joints
    headTopJnt = HEAD_END
    headTopJntFull = f"{jntNameSpace}:{headTopJnt}"
    translateY = cmds.getAttr(f"{headTopJntFull}.translateY")
    translateZ = cmds.getAttr(f"{headTopJntFull}.translateZ")
    dist = math.hypot(translateY, translateZ)

    # create the control box and zero group
    headJnt = HEAD
    ctrlBox = drawCtrlBox(name=f"{CTRL_NAMESPACE}:ctrl{headJnt}",
                          size=[dist, dist, dist],
                          color=VIOLET,
                          pivot="bottom")
    zeroGrp = cmds.group(empty=True, name=f"{CTRL_NAMESPACE}:zero{headJnt}")
    cmds.matchTransform(zeroGrp, ctrlBox)
    cmds.parent(ctrlBox, zeroGrp)

    # match transformation
    headJntFull = f"{jntNameSpace}:{headJnt}"
    cmds.matchTransform(zeroGrp, headJntFull)

    # add orient constraint
    cmds.orientConstraint(ctrlBox, headJntFull)


def setNeckHeadHierarchy(jntNameSpace):
    jnts = []
    jnts.append(HEAD)
    jnts.append(NECK[0])
    setFkCtrlHierarchy(jnts, jntNameSpace, CTRL_NAMESPACE)

    # put neck ctrl under spine ctrl
    neckZeroGrp = f"{CTRL_NAMESPACE}:zero{NECK[0]}"
    spineCtrl = f"{CTRL_NAMESPACE}:ctrl{SPINES[0]}"
    cmds.parent(neckZeroGrp, spineCtrl)
