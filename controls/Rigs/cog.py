from maya import cmds
from ..Utils.shapes import drawCtrlCircle
from ..Utils.constants import HIP, ORANGE, WRISTS, LEGS
from ..Utils.helpers import lockAndHideAttributes


def createCogCtrl(jntNameSpace: str, ctrlNameSpace: str):
    # create control circle
    cogCtrlGrp = drawCtrlCircle(name=f"{ctrlNameSpace}:ctrlCog",
                                radius=50,
                                color=ORANGE)
    cogCtrl = cogCtrlGrp[0]
    cogCtrlShape = cogCtrlGrp[1]

    # change the shape to octagon
    cmds.setAttr(f"{cogCtrlShape}.degree", 1)

    # delete history
    cmds.delete(cogCtrl, constructionHistory=True)

    # create zero group
    cogZeroGrp = cmds.group(cogCtrl, name=f"{ctrlNameSpace}:zeroCog")
    # match transformation
    hipJnt = f"{jntNameSpace}:{HIP}"
    cmds.matchTransform(cogZeroGrp, hipJnt)

    setCogHierarchy(cogCtrl, ctrlNameSpace)
    lockAndHideAttributes(cogCtrl, translate=False)


def setCogHierarchy(cogCtrl, ctrlNameSpace):
    # put hips, handCtrlGrps, LegIkFkBlend under cog
    hipZeroGrp = f"{ctrlNameSpace}:zero{HIP}"
    cmds.parent(hipZeroGrp, cogCtrl)
    for hand in WRISTS:
        handGrp = f"{ctrlNameSpace}:{hand}CtrlGrp"
        cmds.parent(handGrp, cogCtrl)
    for leg in LEGS:
        legIkFkBlendGrp = f"{ctrlNameSpace}:zero{leg}IkFkBlend"
        cmds.parent(legIkFkBlendGrp, cogCtrl)
