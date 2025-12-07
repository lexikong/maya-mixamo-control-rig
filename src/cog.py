from maya import cmds
from shapes import drawCtrlCircle
from constants import HIP, CTRL_NAMESPACE, ORANGE


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


# TODO: set up control and hierarchy
