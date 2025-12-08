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
    # fingers.fingers(parentGrp, nameSpace)
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


if __name__ == "__main__":
    importMayaScript()
    import fingers
    import arms_old as arms
    import constants
    import orientJoints
    import utils
    import shapes
    import arm
    import foot
    import leg
    import limb
    import limbParams
    import limbConfig
    import spine
    import head
    import shoulders
    import cog
    import world

    importlib.reload(shapes)
    importlib.reload(utils)
    importlib.reload(constants)
    importlib.reload(orientJoints)
    importlib.reload(fingers)
    importlib.reload(arms)
    importlib.reload(limb)
    importlib.reload(arm)
    importlib.reload(foot)
    importlib.reload(leg)
    importlib.reload(limbParams)
    importlib.reload(limbConfig)
    importlib.reload(spine)
    importlib.reload(head)
    importlib.reload(shoulders)
    importlib.reload(cog)
    importlib.reload(world)

    cleanup()
    preprocess()
