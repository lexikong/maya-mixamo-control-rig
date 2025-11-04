from maya import cmds
from constants import UP, RED


def createCircleCtrl(rigNameSpace: str,
                     jntNameSpace: str,
                     jntName: str,
                     radius: float = 5.0,
                     color: int = RED,
                     constraint: str = "parent"):
    # create nurbs circle and zero group
    # TODO: non-hardcoded radius

    nurbsCircle = cmds.circle(name=f"{rigNameSpace}:ctrl{jntName}",
                              normal=UP,
                              radius=radius)
    # set color to be red
    # TODO: allow user to customize color
    shapeNode = cmds.listRelatives(nurbsCircle, shapes=True)[0]
    cmds.setAttr(f"{shapeNode}.overrideEnabled", 1)
    cmds.setAttr(f'{shapeNode}.overrideColor', color)
    zeroGrp = cmds.group(nurbsCircle, name=f"{rigNameSpace}:zero{jntName}")
    # match transformation
    jntNameFull = f"{jntNameSpace}:{jntName}"
    cmds.matchTransform(zeroGrp, jntNameFull)

    # set constraint
    if (constraint == "parent"):
        cmds.parentConstraint(nurbsCircle, jntNameFull)
    elif (constraint == "orient"):
        cmds.orientConstraint(nurbsCircle, jntNameFull)

