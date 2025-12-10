import maya.cmds as cmds
from ..Controls.startup import RigBuilder


# UI elements id
NS_FIELD_ID = "nameSpaceField"
SKELETON_MENU_ID = 'skeletonLodMenu'
# constants
TEXT_HEIGHT = 30
TEXT_FIELD_WIDTH = (120, 100)


def createUI():
    # building UI
    windowName = 'MixamoControlRigWindow'

    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, window=True)

    cmds.window(windowName, title="MixamoControlRig")
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="Select the hip joint to start", h=TEXT_HEIGHT)

    cmds.textFieldGrp(NS_FIELD_ID,
                      label='Control NameSpace',
                      placeholderText='e.g. ctrl',
                      text='ctrl',
                      columnWidth2=TEXT_FIELD_WIDTH)

    cmds.optionMenuGrp(SKELETON_MENU_ID,
                       label='Skeleton LOD',
                       h=TEXT_HEIGHT)
    cmds.menuItem(label='Standard Skeleton (65)')
    cmds.menuItem(label='3 Chain Finger (49)')
    cmds.menuItem(label='2 Chain Finger (41)')
    cmds.menuItem(label='No Finger (25)')

    cmds.button(label="Create Control Rigs", command=createCtrls)

    cmds.showWindow(windowName)


def createCtrls(*args):
    ctrlNameSpace = cmds.textFieldGrp(NS_FIELD_ID, query=True, text=True)
    skeletonLOD = cmds.optionMenuGrp(SKELETON_MENU_ID, query=True, select=True)

    rigBuilder = RigBuilder()
    rigBuilder.start(ctrlNameSpace, skeletonLOD)
