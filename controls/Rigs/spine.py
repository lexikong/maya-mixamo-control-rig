from maya import cmds
from ..Utils.helpers import multiJntFkCtrl
from ..Utils.constants import SPINES, PINK, SHOULDERS, NECK, ARMS, LEGS


def createSpineCtrls(jntNameSpace: str, ctrlNameSpace: str):
    spineJnts = SPINES
    multiJntFkCtrl(spineJnts, jntNameSpace, ctrlNameSpace, radius=25, color=PINK, constraint="parent")
    setSpineHierarchy(ctrlNameSpace)


def setSpineHierarchy(ctrlNameSpace):
    # put shoulders, neck, and armIkFkBlend under spine2 ctrl
    spineCtrl = f"{ctrlNameSpace}:ctrl{SPINES[0]}"
    for shoulder in SHOULDERS:
        shoulderGrp = f"{ctrlNameSpace}:zero{shoulder}"
        cmds.parent(shoulderGrp, spineCtrl)
    neckGrp = f"{ctrlNameSpace}:zero{NECK[0]}"
    cmds.parent(neckGrp, spineCtrl)
    for arm in ARMS:
        armIkFkBlend = f"{ctrlNameSpace}:zero{arm}IkFkBlend"
        cmds.parent(armIkFkBlend, spineCtrl)

    # put fk legs under hip ctrl
    hipCtrl = f"{ctrlNameSpace}:ctrl{SPINES[3]}"
    for leg in LEGS:
        legFk = f"{ctrlNameSpace}:zero{leg}Fk"
        cmds.parent(legFk, hipCtrl)
