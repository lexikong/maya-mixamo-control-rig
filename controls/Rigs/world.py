from maya import cmds
from ..Utils.constants import CTRL_NAMESPACE, ORANGE, HANDS, ELBOWS, ANKLES, KNEES, HIP
from ..Utils.helpers import drawCtrlCircle, lockAndHideAttributes


def createWorldCtrl(nameSpace: str):
    # create control circle
    worldCtrl = drawCtrlCircle(name=f"{CTRL_NAMESPACE}:ctrlWorld",
                               radius=70,
                               color=ORANGE)[0]

    # delete history
    cmds.delete(worldCtrl, constructionHistory=True)

    # create zero group
    cmds.group(worldCtrl, name=f"{CTRL_NAMESPACE}:zeroWorld")

    setWorldHierarchy(worldCtrl)
    setScaleCtrl(nameSpace, worldCtrl)


def setWorldHierarchy(worldCtrl: str):
    # put cog, HandIk, FootIk, and their pole vectors under world
    cogZeroGrp = f"{CTRL_NAMESPACE}:zeroCog"
    cmds.parent(cogZeroGrp, worldCtrl)
    for hand in HANDS:
        handIkZeroGrp = f"{CTRL_NAMESPACE}:zero{hand}Ik"
        cmds.parent(handIkZeroGrp, worldCtrl)
    for elbow in ELBOWS:
        elbowPvZeroGrp = f"{CTRL_NAMESPACE}:zero{elbow}PoleVec"
        cmds.parent(elbowPvZeroGrp, worldCtrl)
    for foot in ANKLES:
        footIkZeroGrp = f"{CTRL_NAMESPACE}:zero{foot}Ik"
        cmds.parent(footIkZeroGrp, worldCtrl)
    for knee in KNEES:
        kneePvZeroGrp = f"{CTRL_NAMESPACE}:zero{knee}PoleVec"
        cmds.parent(kneePvZeroGrp, worldCtrl)


def setScaleCtrl(nameSpace: str, worldCtrl: str):
    hipJnt = f"{nameSpace}:{HIP}"
    # set parent and scale constraint between world ctrl and hip joint
    cmds.parentConstraint(worldCtrl, hipJnt, mo=True)
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