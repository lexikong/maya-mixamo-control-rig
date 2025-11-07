from maya import cmds
from constants import RED, YELLOW
from shapes import drawCtrlCircle, drawCtrlCube


# TODO: move match transformation and constraint out?
def createCircleCtrl(rigNameSpace: str,
                     jntNameSpace: str,
                     jntName: str,
                     radius: float = 5.0,
                     color: int = RED,
                     constraint: str = "parent"):
    # create nurbs circle and zero group
    # TODO: non-hardcoded radius
    nurbsCircle = drawCtrlCircle(name=f"{rigNameSpace}:ctrl{jntName}",
                                 radius=radius,
                                 color=color)
    zeroGrp = cmds.group(nurbsCircle, name=f"{rigNameSpace}:zero{jntName}")
    # match transformation
    jntNameFull = f"{jntNameSpace}:{jntName}"
    cmds.matchTransform(zeroGrp, jntNameFull)

    # set constraint
    if (constraint == "parent"):
        cmds.parentConstraint(nurbsCircle, jntNameFull)
    elif (constraint == "orient"):
        cmds.orientConstraint(nurbsCircle, jntNameFull)


def createCubeCtrl(ctrlNameSpace: str,
                   jntName: str,
                   size: float = 5.0,
                   color: int = YELLOW):
    cubeCtrl = drawCtrlCube(name=f"{ctrlNameSpace}:ctrl{jntName}",
                            size=size,
                            color=color)
    zeroGrp = cmds.group(cubeCtrl, name=f"{ctrlNameSpace}:zero{jntName}")
    return cubeCtrl, zeroGrp
