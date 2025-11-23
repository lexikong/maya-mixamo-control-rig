from utils import multiJntFkCtrl
from constants import CTRL_NAMESPACE, HEAD, VIOLET


def createHeadCtrls(jntNameSpace: str):
    headJnts = HEAD
    multiJntFkCtrl(headJnts, jntNameSpace, CTRL_NAMESPACE, radius=15, color=VIOLET)
