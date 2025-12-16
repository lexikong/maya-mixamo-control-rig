from maya import cmds
from ..Utils.constants import ORANGE, HANDS, ELBOWS, ANKLES, KNEES, HIP
from ..Utils.helpers import drawCtrlCircle, lockAndHideAttributes


def createWorldCtrl(jntNameSpace: str, ctrlNameSpace: str):
    # create control circle
    worldCtrl = drawCtrlCircle(name=f"{ctrlNameSpace}:ctrlWorld",
                               radius=70,
                               color=ORANGE)[0]

    # delete history
    cmds.delete(worldCtrl, constructionHistory=True)

    # create zero group
    cmds.group(worldCtrl, name=f"{ctrlNameSpace}:zeroWorld")

    setWorldHierarchy(worldCtrl, ctrlNameSpace)
    setScaleCtrl(jntNameSpace, worldCtrl)


def setWorldHierarchy(worldCtrl: str, ctrlNameSpace: str):
    # put cog, HandIk, FootIk, and their pole vectors under world
    cogZeroGrp = f"{ctrlNameSpace}:zeroCog"
    cmds.parent(cogZeroGrp, worldCtrl)
    for hand in HANDS:
        handIkZeroGrp = f"{ctrlNameSpace}:zero{hand}Ik"
        cmds.parent(handIkZeroGrp, worldCtrl)
    for elbow in ELBOWS:
        elbowPvZeroGrp = f"{ctrlNameSpace}:zero{elbow}PoleVec"
        cmds.parent(elbowPvZeroGrp, worldCtrl)
    for foot in ANKLES:
        footIkZeroGrp = f"{ctrlNameSpace}:zero{foot}Ik"
        cmds.parent(footIkZeroGrp, worldCtrl)
    for knee in KNEES:
        kneePvZeroGrp = f"{ctrlNameSpace}:zero{knee}PoleVec"
        cmds.parent(kneePvZeroGrp, worldCtrl)


def setScaleCtrl(jntNameSpace: str, worldCtrl: str):
    hipJnt = f"{jntNameSpace}:{HIP}"
    # set scale constraint between world ctrl and hip joint
    cmds.scaleConstraint(worldCtrl, hipJnt)
    # add rigScale attribute
    rigScaleAttr = "rigScale"
    cmds.addAttr(worldCtrl, longName=rigScaleAttr, minValue=0.0, keyable=True, attributeType='float')
    cmds.setAttr(f"{worldCtrl}.{rigScaleAttr}", 1)

    # connect rigScale to scaleX, Y and Z
    cmds.connectAttr(f"{worldCtrl}.{rigScaleAttr}", f"{worldCtrl}.scaleX")
    cmds.connectAttr(f"{worldCtrl}.{rigScaleAttr}", f"{worldCtrl}.scaleY")
    cmds.connectAttr(f"{worldCtrl}.{rigScaleAttr}", f"{worldCtrl}.scaleZ")

    # hide other attributes
    lockAndHideAttributes(worldCtrl, translate=False, scale=True)
