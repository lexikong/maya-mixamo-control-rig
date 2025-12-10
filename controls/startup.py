from maya import cmds
import sys

from .Utils import constants
from .Utils import orientJoints
from .Utils import helpers
from .Utils import shapes
from .Utils import limbParams
from .Utils import limbConfig

from .Rigs import fingers
from .Rigs import arms_old as arms
from .Rigs import arm
from .Rigs import foot
from .Rigs import leg
from .Rigs import limb
from .Rigs import spine
from .Rigs import head
from .Rigs import shoulders
from .Rigs import cog
from .Rigs import world


def importMayaScript():
    # add the script directory to the system path
    # TODO: make this work when being distributed as a package
    myScriptDir = cmds.internalVar(userScriptDir=True)
    setScriptDir = myScriptDir + 'mixamoControlRig/controls/'
    sys.path.append(setScriptDir)


def preprocess():
    # select the hip joint
    selected = cmds.ls(selection=True)
    numElements = len(selected)
    if not selected:
        print("Please select a Hips joint to start with")
        return
    elif (numElements > 1):
        print("Please select only one object")
        return
    else:
        process(selected[0])


def process(parentGrp: str):
    # extract the namespace from input
    if (":" not in parentGrp):
        nameSpace = ""
    else:
        nameSpace = parentGrp.split(":", 1)[0]

    fingers.createFingerCtrls(nameSpace)
    orientJoints.orientJoints(nameSpace)

    leftArm = arm.MixamoArm(nameSpace, limbConfig.leftArmParams)
    leftLeg = leg.MixamoLeg(nameSpace, limbConfig.leftLegParams)
    rightArm = arm.MixamoArm(nameSpace, limbConfig.rightArmParams)
    rightLeg = leg.MixamoLeg(nameSpace, limbConfig.rightLegParams)

    leftArm.createCtrls()
    leftLeg.createCtrls()
    rightArm.createCtrls()
    rightLeg.createCtrls()

    shoulders.createShoulderCtrls(nameSpace)
    head.createHeadCtrls(nameSpace)
    spine.createSpineCtrls(nameSpace)

    cog.createCogCtrl(nameSpace)

    world.createWorldCtrl(nameSpace)

    cmds.select(clear=True)


def cleanup():
    # remove all controls
    ctrls = cmds.ls(f"{constants.CTRL_NAMESPACE}:*")
    if ctrls:
        cmds.delete(ctrls)
    # remove arm FK and IK joints
    arms.cleanup()


def start():
    importMayaScript()

    cleanup()
    preprocess()
