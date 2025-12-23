# Assuming all mixamo characters share the same joints naming convention
# Also assuming they all have the same joints
from maya import cmds
from ..Utils.constants import HANDS, NUM_FINGER_JOINTS, RED, FNGR_CURL_VAL, THUMB_CURL_VAL, CURL_CTRL_OFFSET
from ..Utils.helpers import multiJntFkCtrl, createCrossCtrl, lockAndHideAttributes
from ..Utils.userInput import UserInput


def createFingerCtrls(jntNameSpace: str, ctrlNameSpace: str):
    fngrNames = UserInput.getFingers()
    # create finger ctrls if fngrNames is not empty
    # i.e. there are finger joints
    if (fngrNames):
        for hand in HANDS:
            # create a group to hold all ctrls
            ctrlGrp = cmds.group(world=True,
                                 empty=True,
                                 name=f"{ctrlNameSpace}:{hand}CtrlGrp")
            wristJnt = f"{jntNameSpace}:{hand}"
            cmds.matchTransform(ctrlGrp, wristJnt)

            for fngr in fngrNames:
                fngrJnt = f"{jntNameSpace}:{hand}{fngr}1"
                # cartoon characters only have 4 fingers
                if (not cmds.objExists(fngrJnt)):
                    break
                jnts = []
                for i in range(NUM_FINGER_JOINTS-1, 0, -1):
                    jnts.append(f"{hand}{fngr}{str(i)}")
                topLvlGrp = multiJntFkCtrl(jnts,
                                           jntNameSpace,
                                           ctrlNameSpace,
                                           radius=2.2,
                                           color=RED)
                cmds.parent(topLvlGrp, ctrlGrp)

            # Parent constrain the control group to the wrist joint
            cmds.parentConstraint(wristJnt, ctrlGrp)
        # Add finger curl ctrl
        addFingerCurlCtrl(jntNameSpace, ctrlNameSpace, fngrNames)


def addFingerCurlCtrl(jntNameSpace, ctrlNameSpace, fngrNames):
    if (fngrNames):
        for hand in HANDS:
            # Create the curl ctrl obj
            curlCtrl, curlZeroGrp = createCrossCtrl(ctrlNameSpace,
                                                    f"{hand}FingerCurlCtrl",
                                                    size=7.0)
            # put the curl control shape around the wrist plus offset
            wristJnt = f"{jntNameSpace}:{hand}"
            cmds.matchTransform(curlZeroGrp, wristJnt, pos=True, rot=False, scl=False)
            currentTranslate = cmds.getAttr(f"{curlZeroGrp}.translate")[0]
            newTranslate = [a + b for a, b in zip(currentTranslate, CURL_CTRL_OFFSET)]
            cmds.setAttr(f"{curlZeroGrp}.translate", newTranslate[0], newTranslate[1],newTranslate[2])
            # lock and hide attributes
            lockAndHideAttributes(curlCtrl, rotation=True)
            for fngr in fngrNames:
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
                    ctrl = f"{ctrlNameSpace}:ctrl{hand}{fngr}{str(i)}"
                    zeroGrp = f"{ctrlNameSpace}:zero{hand}{fngr}{str(i)}"
                    sdkGrpName = f"{ctrlNameSpace}:sdk{hand}{fngr}{str(i)}"
                    sdkGrp = cmds.group(empty=True, name=sdkGrpName)
                    cmds.matchTransform(sdkGrp, ctrl)
                    # Insert the SDK group to the existing hierarchy
                    cmds.parent(sdkGrp, zeroGrp)
                    cmds.parent(ctrl, sdkGrp)

                    # Set Driven Keys
                    if (fngr == "Thumb"):
                        # thumb rotates along z
                        cmds.setDrivenKeyframe(f"{sdkGrp}.rz", cd=f"{curlCtrl}.{driverAttr}", dv=0, v=0)
                        cmds.setDrivenKeyframe(f"{sdkGrp}.rz", cd=f"{curlCtrl}.{driverAttr}", dv=1, v=THUMB_CURL_VAL)
                    else:
                        cmds.setDrivenKeyframe(f"{sdkGrp}.rx", cd=f"{curlCtrl}.{driverAttr}", dv=0, v=0)
                        cmds.setDrivenKeyframe(f"{sdkGrp}.rx", cd=f"{curlCtrl}.{driverAttr}", dv=1, v=FNGR_CURL_VAL)
