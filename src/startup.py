from maya import cmds
import sys
import importlib


def importMayaScript():
    # add the script directory to the system path
    # TODO: make this work when being distributed as a package
    myScriptDir = cmds.internalVar(userScriptDir=True)
    setScriptDir = myScriptDir + 'mixamoControlRig/src/'
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
    fingers.fingers(parentGrp, nameSpace)
    orientJoints.orientJoints(nameSpace)
    arms.armsCtrl(nameSpace)


def cleanup():
    # remove all controls
    ctrls = cmds.ls(f"{constants.CTRL_NAMESPACE}:*")
    if ctrls:
        cmds.delete(ctrls)
    # remove arm FK and IK joints
    arms.cleanup()


if __name__ == "__main__":
    importMayaScript()
    import fingers
    import arms
    import constants
    import orientJoints
    import utils
    importlib.reload(fingers)
    importlib.reload(arms)
    importlib.reload(constants)
    importlib.reload(orientJoints)
    importlib.reload(utils)

    cleanup()
    preprocess()
