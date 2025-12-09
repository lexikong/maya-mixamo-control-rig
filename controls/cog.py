from maya import cmds
from shapes import drawCtrlCircle
from constants import HIP, CTRL_NAMESPACE, ORANGE, WRISTS, LEGS
from utils import lockAndHideAttributes


def createCogCtrl(jntNameSpace: str):
    # create control circle
    cogCtrlGrp = drawCtrlCircle(name=f"{CTRL_NAMESPACE}:ctrlCog",
                             radius=50,
                             color=ORANGE)
    cogCtrl = cogCtrlGrp[0]
    cogCtrlShape = cogCtrlGrp[1]

    # change the shape to octagon
    cmds.setAttr(f"{cogCtrlShape}.degree", 1)

    # delete history
    cmds.delete(cogCtrl, constructionHistory=True)

    # create zero group
    cogZeroGrp = cmds.group(cogCtrl, name=f"{CTRL_NAMESPACE}:zeroCog")
    # match transformation
    hipJnt = f"{jntNameSpace}:{HIP}"
    cmds.matchTransform(cogZeroGrp, hipJnt)

    setCogHierarchy(cogCtrl)
    lockAndHideAttributes(cogCtrl, translate=False)


def setCogHierarchy(cogCtrl):
    # put hips, handCtrlGrps, LegIkFkBlend under cog
    hipZeroGrp = f"{CTRL_NAMESPACE}:zero{HIP}"
    cmds.parent(hipZeroGrp, cogCtrl)
    for hand in WRISTS:
        handGrp = f"{CTRL_NAMESPACE}:{hand}CtrlGrp"
        cmds.parent(handGrp, cogCtrl)
    for leg in LEGS:
        legIkFkBlendGrp = f"{CTRL_NAMESPACE}:zero{leg}IkFkBlend"
        cmds.parent(legIkFkBlendGrp, cogCtrl)
