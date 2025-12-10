from maya import cmds
import sys

from .Utils import constants
from .Utils import orientJoints
from .Utils import helpers
from .Utils import shapes
from .Utils import limbParams
from .Utils import limbConfig
from .Utils.userInput import UserInput

from .Rigs import fingers
from .Rigs import arm
from .Rigs import foot
from .Rigs import leg
from .Rigs import limb
from .Rigs import spine
from .Rigs import head
from .Rigs import shoulders
from .Rigs import cog
from .Rigs import world


class RigBuilder:
    def __init__(self):
        self.ctrlNameSpace = ""

    def importMayaScript(self):
        # add the script directory to the system path
        # TODO: make this work when being distributed as a package
        myScriptDir = cmds.internalVar(userScriptDir=True)
        setScriptDir = myScriptDir + 'mixamoControlRig/controls/'
        sys.path.append(setScriptDir)

    def checkSelection(self):
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
            self.process(selected[0])

    def process(self, selected: str):
        # extract the jnt namespace from the selected object
        if (":" not in selected):
            jntNameSpace = ""
        else:
            jntNameSpace = selected.split(":")[0]

        orientJoints.orientJoints(jntNameSpace)
        #fingers.createFingerCtrls(jntNameSpace, self.ctrlNameSpace)

        leftArm = arm.MixamoArm(jntNameSpace, self.ctrlNameSpace, limbConfig.leftArmParams)
        leftLeg = leg.MixamoLeg(jntNameSpace, self.ctrlNameSpace, limbConfig.leftLegParams)
        rightArm = arm.MixamoArm(jntNameSpace, self.ctrlNameSpace, limbConfig.rightArmParams)
        rightLeg = leg.MixamoLeg(jntNameSpace, self.ctrlNameSpace, limbConfig.rightLegParams)

        leftArm.createCtrls()
        leftLeg.createCtrls()
        rightArm.createCtrls()
        rightLeg.createCtrls()

        shoulders.createShoulderCtrls(jntNameSpace, self.ctrlNameSpace)
        head.createHeadCtrls(jntNameSpace, self.ctrlNameSpace)
        spine.createSpineCtrls(jntNameSpace, self.ctrlNameSpace)

        cog.createCogCtrl(jntNameSpace, self.ctrlNameSpace)

        world.createWorldCtrl(jntNameSpace, self.ctrlNameSpace)

        cmds.select(clear=True)

    def cleanup(self):
        # remove all controls
        ctrls = cmds.ls(f"{self.ctrlNameSpace}:*")
        if ctrls:
            cmds.delete(ctrls)
        # remove FK and IK joints
        fkJoints = cmds.ls("*Fk", recursive=True)
        if fkJoints:
            cmds.delete(fkJoints)
        ikJoints = cmds.ls("*Ik", recursive=True)
        if ikJoints:
            cmds.delete(ikJoints)
        reverseNodes = cmds.ls(type="reverse", recursive=True)
        for node in reverseNodes:
            cmds.delete(node)

    def start(self, ctrlNameSpace: str, skeletonIndex: int):
        #self.importMayaScript()

        # TODO: check-up instead of cleanup
        UserInput.setCtrlNS(ctrlNameSpace)
        UserInput.setFingers(skeletonIndex)
        self.ctrlNameSpace = UserInput.getCtrlNS()
        self.cleanup()

        self.checkSelection()
