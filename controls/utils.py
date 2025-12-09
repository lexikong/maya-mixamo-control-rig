from maya import cmds
from constants import RED, YELLOW
from shapes import drawCtrlCircle, drawCtrlCube, drawCtrlCross


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
    return nurbsCircle[0], zeroGrp


def createCubeCtrl(ctrlNameSpace: str,
                   jntName: str,
                   size: float = 5.0,
                   color: int = YELLOW,
                   poleVector: bool = False):
    cubeCtrl = drawCtrlCube(name=f"{ctrlNameSpace}:ctrl{jntName}",
                            size=size,
                            color=color,
                            poleVector=poleVector)
    zeroGrp = cmds.group(cubeCtrl, name=f"{ctrlNameSpace}:zero{jntName}")
    return cubeCtrl, zeroGrp


def createCrossCtrl(ctrlNameSpace: str,
                    name: str,
                    size: float = 5.0,
                    color: int = RED,
                    lineWidth: float = 2.0):
    crossCtrl = drawCtrlCross(name=f"{ctrlNameSpace}:ctrl{name}",
                              size=size,
                              color=color,
                              lineWidth=lineWidth)
    shapeNode = cmds.listRelatives(crossCtrl, shapes=True)[0]
    cmds.setAttr(f"{shapeNode}.overrideEnabled", 1)
    cmds.setAttr(f"{shapeNode}.overrideColor", color)
    cmds.setAttr(f"{shapeNode}.lineWidth", float(lineWidth))
    zeroGrp = cmds.group(crossCtrl, name=f"{ctrlNameSpace}:zero{name}")
    return crossCtrl, zeroGrp


def multiJntFkCtrl(jnts, jntNameSpace, ctrlNameSpace, radius=25, color=YELLOW, constraint: str = "orient"):
    # jnts: a list of joint names without namespace prefix
    # the order is bottom up
    # e.g. ["Spine2", "Spine1", "Spine"]
    createFkCtrls(jnts, jntNameSpace, ctrlNameSpace, radius, color, constraint)
    setFkCtrlHierarchy(jnts, jntNameSpace, ctrlNameSpace)
    topLvlGrp = f"{ctrlNameSpace}:zero{jnts[-1]}"
    return topLvlGrp


def createFkCtrls(jnts, jntNameSpace, ctrlNameSpace, radius, color, constraint: str = "orient"):
    for jnt in jnts:
        circleCtrl = createCircleCtrl(ctrlNameSpace,
                                      jntNameSpace,
                                      jnt,
                                      radius=radius,
                                      color=color,
                                      constraint=constraint)[0]
        if (constraint == "orient"):
            lockAndHideAttributes(circleCtrl)
        elif (constraint == "parent"):
            lockAndHideAttributes(circleCtrl, translate=False)


def setFkCtrlHierarchy(jnts, jntNameSpace, ctrlNameSpace):
    for jnt, parentJnt in zip(jnts, jnts[1:]):
        zeroGrp = f"{ctrlNameSpace}:zero{jnt}"
        parentCtrl = f"{ctrlNameSpace}:ctrl{parentJnt}"
        cmds.parent(zeroGrp, parentCtrl)


def lockAndHideAttributes(ctrl: str,
                          translate: bool = True,
                          rotation: bool = False,
                          scale: bool = True,
                          visibility: bool = True,
                          others: list = []):
    '''
    ctrl: the full name with namespace, e.g.ctrl:worldCtrl
    '''
    attributesToHide = []
    if (translate):
        attributesToHide.extend(["tx", "ty", "tz"])
    if (rotation):
        attributesToHide.extend(["rx", "ry", "rz"])
    if (scale):
        attributesToHide.extend(["sx", "sy", "sz"])
    if (visibility):
        attributesToHide.append("visibility")
    attributesToHide.extend(others)

    for attr in attributesToHide:
        fullAttrName = f"{ctrl}.{attr}"
        cmds.setAttr(fullAttrName, lock=True)
        cmds.setAttr(fullAttrName, keyable=False)
        cmds.setAttr(fullAttrName, channelBox=False)
