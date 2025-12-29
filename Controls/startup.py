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

    def checkNameSpace(self):
        if cmds.namespace(exists=self.ctrlNameSpace):
            cmds.warning(f'NameSpace "{self.ctrlNameSpace}" already exists, '
                          'please delete it or use another namespace.')
            return False
        else:
            return True

    def checkSelection(self):
        # select the hip joint
        selected = cmds.ls(selection=True)
        numElements = len(selected)
        if not selected:
            cmds.warning("Please select a Hips joint to start with")
            return False
        elif (numElements > 1):
            cmds.warning("Please select only one object")
            return False
        else:
            self.userSelected = selected[0]
            return True

    def checkUserInput(self):
        return self.checkNameSpace() and self.checkSelection()

    def process(self):
        # extract the jnt namespace from the selected object
        if (":" not in self.userSelected):
            jntNameSpace = ""
        else:
            jntNameSpace = self.userSelected.split(":")[0]

        orientJoints.orientJoints(jntNameSpace)

        leftArm = arm.MixamoArm(jntNameSpace,
                                self.ctrlNameSpace,
                                limbConfig.leftArmParams)
        leftLeg = leg.MixamoLeg(jntNameSpace,
                                self.ctrlNameSpace,
                                limbConfig.leftLegParams)
        rightArm = arm.MixamoArm(jntNameSpace,
                                 self.ctrlNameSpace,
                                 limbConfig.rightArmParams)
        rightLeg = leg.MixamoLeg(jntNameSpace,
                                 self.ctrlNameSpace,
                                 limbConfig.rightLegParams)

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
        # DEV only
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
        # The entry point of the class
        UserInput.setCtrlNS(ctrlNameSpace)
        UserInput.setFingers(skeletonIndex)
        self.ctrlNameSpace = UserInput.getCtrlNS()

        if (self.checkUserInput()):
            self.process()
