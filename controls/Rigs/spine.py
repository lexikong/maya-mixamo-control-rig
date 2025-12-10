from maya import cmds
from ..Utils.helpers import multiJntFkCtrl
from ..Utils.constants import CTRL_NAMESPACE, SPINES, PINK, SHOULDERS, NECK, ARMS, LEGS


def createSpineCtrls(jntNameSpace: str):
    spineJnts = SPINES
    multiJntFkCtrl(spineJnts, jntNameSpace, CTRL_NAMESPACE, radius=25, color=PINK, constraint="parent")
    setSpineHierarchy()


def setSpineHierarchy():
    # put shoulders, neck, and armIkFkBlend under spine2 ctrl
    spineCtrl = f"{CTRL_NAMESPACE}:ctrl{SPINES[0]}"
    for shoulder in SHOULDERS:
        shoulderGrp = f"{CTRL_NAMESPACE}:zero{shoulder}"
        cmds.parent(shoulderGrp, spineCtrl)
    neckGrp = f"{CTRL_NAMESPACE}:zero{NECK[0]}"
    cmds.parent(neckGrp, spineCtrl)
    for arm in ARMS:
        armIkFkBlend = f"{CTRL_NAMESPACE}:zero{arm}IkFkBlend"
        cmds.parent(armIkFkBlend, spineCtrl)

    # put fk legs under hip ctrl
    hipCtrl = f"{CTRL_NAMESPACE}:ctrl{SPINES[3]}"
    for leg in LEGS:
        legFk = f"{CTRL_NAMESPACE}:zero{leg}Fk"
        cmds.parent(legFk, hipCtrl)

