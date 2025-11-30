from maya import cmds
from utils import multiJntFkCtrl, createCircleCtrl
from constants import YELLOW
from shapes import drawCtrlBox
# set up toetip position
# set up heel position
# ball ctrl shape
# toe ctrl shape


class MixamoFoot:
    def __init__(self,
                 jntNameSpace: str,
                 ctrlNameSpace: str,
                 ankleJnt: str,
                 ballJnt: str,
                 toeJnt: str):
        self.jntNameSpace = jntNameSpace
        self.ctrlNameSpace = ctrlNameSpace
        self.ankleJnt = ankleJnt
        self.ballJnt = ballJnt
        self.toeJnt = toeJnt

    def createFootFk(self):
        ballCtrl, zeroGrp = createCircleCtrl(self.ctrlNameSpace,
                            self.jntNameSpace,
                            f"{self.ballJnt}",
                            radius=10.0,
                            color=YELLOW,
                            constraint="orient")
        # append "Fk" postfix to ctrl and zero grp
        ballCtrlFk = f"{ballCtrl}Fk"
        cmds.rename(ballCtrl, ballCtrlFk)
        zeroGrpFk = f"{zeroGrp}Fk"
        cmds.rename(zeroGrp, zeroGrpFk)
        # set hierarchy
        ankleJntFk = f"{self.ankleJnt}Fk"
        ankleJntCtrl = f"{self.ctrlNameSpace}:ctrl{ankleJntFk}"
        cmds.parent(zeroGrpFk, ankleJntCtrl)

    def createHelperJnts(self):
        # create helper joints that will help with ctrl orientation
        cmds.select(clear=True)
        self.RvsToeIkJnt = cmds.joint(name="RvsToeIk")
        cmds.select(clear=True)
        RvsToeIkJnt2 = cmds.joint(name="RvsToeIk2")
        cmds.select(clear=True)
        self.RvsBallIkJnt = cmds.joint(name="RvsBallIk")
        cmds.select(clear=True)
        RvsBallIkJnt2 = cmds.joint(name="RvsBallIk2")

        ballJntFull = f"{self.jntNameSpace}:{self.ballJnt}"
        toeJntFull = f"{self.jntNameSpace}:{self.toeJnt}"
        ankleJntFull = f"{self.jntNameSpace}:{self.ankleJnt}"

        # match transformation of ball roll helper joints
        cmds.matchTransform(self.RvsToeIkJnt, ballJntFull)
        cmds.makeIdentity(self.RvsToeIkJnt, apply=True)
        cmds.matchTransform(RvsToeIkJnt2, toeJntFull)
        cmds.makeIdentity(RvsToeIkJnt2, apply=True)
        cmds.parent(RvsToeIkJnt2, self.RvsToeIkJnt)
        # match transformation of toe roll helper joints
        cmds.matchTransform(self.RvsBallIkJnt, ballJntFull)
        cmds.makeIdentity(self.RvsBallIkJnt, apply=True)
        cmds.matchTransform(RvsBallIkJnt2, ankleJntFull)
        cmds.makeIdentity(RvsBallIkJnt2, apply=True)
        cmds.parent(RvsBallIkJnt2, self.RvsBallIkJnt)
        # orient the ball roll joint
        cmds.joint(self.RvsBallIkJnt, e=True, oj='yzx', sao='yup')

    def createIkCtrls(self):
        # create the control shapes and zero groups
        toeIkCtrl = drawCtrlBox(name=f"{self.ctrlNameSpace}:ctrl{self.toeJnt}Ik",
                                size=[12, 8, 6],
                                pivot="bottom")
        toeIkZeroGrp = cmds.group(empty=True, name=f"{self.ctrlNameSpace}:zero{self.toeJnt}Ik")
        cmds.matchTransform(toeIkZeroGrp, toeIkCtrl, pivots=True)
        cmds.parent(toeIkCtrl, toeIkZeroGrp)

        ballIkCtrl = drawCtrlBox(name=f"{self.ctrlNameSpace}:ctrl{self.ballJnt}Ik",
                                size=[12, 8, 6],
                                pivot="bottom")
        ballIkZeroGrp = cmds.group(empty=True, name=f"{self.ctrlNameSpace}:zero{self.ballJnt}Ik")
        cmds.matchTransform(ballIkZeroGrp, ballIkCtrl, pivots=True)
        cmds.parent(ballIkCtrl, ballIkZeroGrp)

        # match transformation
        cmds.matchTransform(toeIkZeroGrp, self.RvsToeIkJnt)
        cmds.matchTransform(ballIkZeroGrp, self.RvsBallIkJnt)

        # set orient constraints
        cmds.orientConstraint(toeIkCtrl, f"{self.jntNameSpace}:{self.ballJnt}")
        footIkCtrl = f"{self.ctrlNameSpace}:ctrl{self.ankleJnt}Ik"
        cmds.parent(footIkCtrl, ballIkCtrl)

