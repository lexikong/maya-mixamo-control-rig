from utils import multiJntFkCtrl
from constants import CTRL_NAMESPACE, SPINES, PINK


def createSpineCtrls(jntNameSpace: str):
    spineJnts = SPINES
    multiJntFkCtrl(spineJnts, jntNameSpace, CTRL_NAMESPACE, radius=25, color=PINK)
