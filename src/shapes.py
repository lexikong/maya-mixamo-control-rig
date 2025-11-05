from maya import cmds
from constants import UP, RED


# draw different control shapes

def drawCtrlCircle(name: str,
                   radius: float,
                   color: int = RED,
                   lineWidth: float = 2.0):
    nurbsCircle = cmds.circle(name=name,
                              normal=UP,
                              radius=radius)
    shapeNode = cmds.listRelatives(nurbsCircle, shapes=True)[0]
    cmds.setAttr(f"{shapeNode}.overrideEnabled", 1)
    cmds.setAttr(f'{shapeNode}.overrideColor', color)
    cmds.setAttr(f"{shapeNode}.lineWidth", float(lineWidth))
    return nurbsCircle


def drawCtrlCube(name: str,
                 size: float = 1.0,
                 color: int = RED,
                 lineWidth: float = 2.0):
    halfSize = size / 2.0
    points = [(-halfSize, -halfSize, -halfSize),
              (halfSize, -halfSize, -halfSize),
              (halfSize, halfSize, -halfSize),
              (-halfSize, halfSize, -halfSize),
              (-halfSize, -halfSize, halfSize),
              (halfSize, -halfSize, halfSize),
              (halfSize, halfSize, halfSize),
              (-halfSize, halfSize, halfSize)]

    walkPath = [0, 1, 2, 3, 0, 4, 5, 1, 2, 6, 5, 4, 7, 6, 7, 3]
    walkPathPoints = [points[i] for i in walkPath]
    cubeCurve = cmds.curve(name=name,
                           degree=1,
                           point=walkPathPoints,
                           knot=list(range(len(walkPath))))

    shapeNode = cmds.listRelatives(cubeCurve, shapes=True)[0]
    cmds.setAttr(f"{shapeNode}.overrideEnabled", 1)
    cmds.setAttr(f'{shapeNode}.overrideColor', color)
    cmds.setAttr(f"{shapeNode}.lineWidth", float(lineWidth))
    return cubeCurve
