# Assuming all mixamo characters share the same joints naming convention
# Also assuming they all have the same joints
from maya import cmds
from ..Utils.constants import NUM_FINGER_JOINTS, RED, FNGR_CURL_VAL, THUMB_CURL_VAL, CURL_CTRL_OFFSET
from ..Utils.helpers import multiJntFkCtrl, createCrossCtrl, lockAndHideAttributes
from ..Utils.userInput import UserInput


class MixamoFingers:
    def __init__(self, jntNameSpace: str, ctrlNameSpace: str, hand: str):
        self.jntNameSpace = jntNameSpace
        self.ctrlNameSpace = ctrlNameSpace
        self.hand = hand
        self.fngrNames = UserInput.getFingers()

    def createCtrls(self):
        self.createFkCtrls()
        self.addCurlCtrl()

    def createFkCtrls(self):
        # create finger ctrls if fngrNames is not empty
        # i.e. there are finger joints
        if (self.fngrNames):
            # create a group to hold all ctrls
            ctrlGrp = cmds.group(world=True,
                                 empty=True,
                                 name=f"{self.ctrlNameSpace}:{self.hand}CtrlGrp")
            wristJnt = f"{self.jntNameSpace}:{self.hand}"
            cmds.matchTransform(ctrlGrp, wristJnt)

            for fngr in self.fngrNames:
                fngrJnt = f"{self.jntNameSpace}:{self.hand}{fngr}1"
                # cartoon characters only have 4 fingers
                if (not cmds.objExists(fngrJnt)):
                    break
                jnts = []
                for i in range(NUM_FINGER_JOINTS-1, 0, -1):
                    jnts.append(f"{self.hand}{fngr}{str(i)}")
                topLvlGrp = multiJntFkCtrl(jnts,
                                           self.jntNameSpace,
                                           self.ctrlNameSpace,
                                           radius=2.2,
                                           color=RED)
                cmds.parent(topLvlGrp, ctrlGrp)

            # Parent constrain the control group to the wrist joint
            cmds.parentConstraint(wristJnt, ctrlGrp)

    def addCurlCtrl(self):
        if (self.fngrNames):
            # Create the curl ctrl obj
            curlCtrl, curlZeroGrp = createCrossCtrl(self.ctrlNameSpace,
                                                    f"{self.hand}FingerCurlCtrl",
                                                    size=4.5)
            # put the curl control shape around the wrist plus offset
            wristJnt = f"{self.jntNameSpace}:{self.hand}"
            cmds.matchTransform(curlZeroGrp, wristJnt, pos=True, rot=False, scl=False)
            currentTranslate = cmds.getAttr(f"{curlZeroGrp}.translate")[0]
            newTranslate = [a + b for a, b in zip(currentTranslate, CURL_CTRL_OFFSET)]
            cmds.setAttr(f"{curlZeroGrp}.translate", newTranslate[0], newTranslate[1], newTranslate[2])
            # lock and hide attributes
            lockAndHideAttributes(curlCtrl, rotation=True)
            # set the hierarchy
            self.setCurlCtrlHierarchy(curlZeroGrp)

            # set up the driven keys
            for fngr in self.fngrNames:
                driverAttr = f"{fngr}Curl"
                # Add attribute
                cmds.addAttr(curlCtrl,
                            longName=driverAttr,
                            attributeType="double",
                            defaultValue=0,
                            min=0,
                            max=1,
                            keyable=True)

                for i in range(NUM_FINGER_JOINTS-1, 0, -1):
                    # Create a SDK(Set Driven Key) group
                    ctrl = f"{self.ctrlNameSpace}:ctrl{self.hand}{fngr}{str(i)}"
                    zeroGrp = f"{self.ctrlNameSpace}:zero{self.hand}{fngr}{str(i)}"
                    sdkGrpName = f"{self.ctrlNameSpace}:sdk{self.hand}{fngr}{str(i)}"
                    sdkGrp = cmds.group(empty=True, name=sdkGrpName)
                    cmds.matchTransform(sdkGrp, ctrl)
                    # Insert the SDK group to the existing hierarchy
                    cmds.parent(sdkGrp, zeroGrp)
                    cmds.parent(ctrl, sdkGrp)

                    # Set Driven Keys
                    if (fngr == "Thumb"):
                        # thumb rotates along z
                        cmds.setDrivenKeyframe(f"{sdkGrp}.rz", cd=f"{curlCtrl}.{driverAttr}", dv=0, v=0)
                        # left and right hand rotate along different directions
                        if (self.hand == "LeftHand"):
                            cmds.setDrivenKeyframe(f"{sdkGrp}.rz", cd=f"{curlCtrl}.{driverAttr}", dv=1, v=THUMB_CURL_VAL)
                        else:
                            cmds.setDrivenKeyframe(f"{sdkGrp}.rz", cd=f"{curlCtrl}.{driverAttr}", dv=1, v=-THUMB_CURL_VAL)
                    else:
                        cmds.setDrivenKeyframe(f"{sdkGrp}.rx", cd=f"{curlCtrl}.{driverAttr}", dv=0, v=0)
                        cmds.setDrivenKeyframe(f"{sdkGrp}.rx", cd=f"{curlCtrl}.{driverAttr}", dv=1, v=FNGR_CURL_VAL)

    def setCurlCtrlHierarchy(self, curlZeroGrp: str):
        wristJnt = f"{self.jntNameSpace}:{self.hand}"
        cmds.parentConstraint(wristJnt, curlZeroGrp, mo=True)
