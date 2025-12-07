from maya import cmds
from constants import CTRL_NAMESPACE, ORANGE, HANDS, ELBOWS, ANKLES, KNEES
from utils import drawCtrlCircle


def createWorldCtrl():
    # create control circle
    worldCtrl = drawCtrlCircle(name=f"{CTRL_NAMESPACE}:ctrlWorld",
                             radius=70,
                             color=ORANGE)[0]

    # delete history
    cmds.delete(worldCtrl, constructionHistory=True)

    # create zero group
    cmds.group(worldCtrl, name=f"{CTRL_NAMESPACE}:zeroWorld")

    setWorldHierarchy(worldCtrl)


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