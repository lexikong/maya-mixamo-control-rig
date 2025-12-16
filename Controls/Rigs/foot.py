from maya import cmds
from ..Utils.helpers import multiJntFkCtrl, createCircleCtrl, lockAndHideAttributes
from ..Utils.constants import YELLOW
from ..Utils.shapes import drawCtrlBox, drawCtrlCube, drawCtrlCircle


class MixamoFoot:
    def __init__(self,
                 jntNameSpace: str,
                 ctrlNameSpace: str,
                 ankleJnt: str,
                 ballJnt: str,
                 toeJnt: str,
                 side: str):
        self.jntNameSpace = jntNameSpace
        self.ctrlNameSpace = ctrlNameSpace
        self.ankleJnt = ankleJnt
        self.ballJnt = ballJnt
        self.toeJnt = toeJnt
        self.side = side

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
        # lock and hide other attribtues
        lockAndHideAttributes(ballCtrlFk)

    def createFootIk(self):
        self.createHelperJnts()
        self.createBallToeRoll()
        self.deleteHelperJnts()
        self.createToeHeelPivots()
        self.setHeelToeHierarchy()

    def createHelperJnts(self):
        # create helper joints that will help with ctrl orientation
        cmds.select(clear=True)
        self.RvsToeIkJnt = cmds.joint(name=f"{self.ctrlNameSpace}:RvsToeIk")
        cmds.select(clear=True)
        RvsToeIkJnt2 = cmds.joint(name=f"{self.ctrlNameSpace}:RvsToeIk2")
        cmds.select(clear=True)
        self.RvsBallIkJnt = cmds.joint(name=f"{self.ctrlNameSpace}:RvsBallIk")
        cmds.select(clear=True)
        RvsBallIkJnt2 = cmds.joint(name=f"{self.ctrlNameSpace}:RvsBallIk2")

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

    def deleteHelperJnts(self):
        cmds.delete(self.RvsToeIkJnt)
        cmds.delete(self.RvsBallIkJnt)

    def createBallToeRoll(self):
        # create the control shapes and zero groups
        toeIkCtrl = drawCtrlBox(name=f"{self.ctrlNameSpace}:ctrl{self.toeJnt}Ik",
                                size=[12, 6, 4],
                                pivot="bottom")
        self.toeIkZeroGrp = cmds.group(empty=True, name=f"{self.ctrlNameSpace}:zero{self.toeJnt}Ik")
        cmds.matchTransform(self.toeIkZeroGrp, toeIkCtrl, pivots=True)
        cmds.parent(toeIkCtrl, self.toeIkZeroGrp)

        ballIkCtrl = drawCtrlBox(name=f"{self.ctrlNameSpace}:ctrl{self.ballJnt}Ik",
                                 size=[12, 8, 6],
                                 pivot="bottom")
        self.ballIkZeroGrp = cmds.group(empty=True, name=f"{self.ctrlNameSpace}:zero{self.ballJnt}Ik")
        cmds.matchTransform(self.ballIkZeroGrp, ballIkCtrl, pivots=True)
        cmds.parent(ballIkCtrl, self.ballIkZeroGrp)

        # match transformation
        cmds.matchTransform(self.toeIkZeroGrp, self.RvsToeIkJnt)
        cmds.matchTransform(self.ballIkZeroGrp, self.RvsBallIkJnt)

        # move the controls so that they don't conflict with each other
        cmds.move(0, 0, 2, self.toeIkZeroGrp, relative=True)

        # set orient constraints
        cmds.orientConstraint(toeIkCtrl, f"{self.jntNameSpace}:{self.ballJnt}")
        cmds.orientConstraint(ballIkCtrl, f"{self.jntNameSpace}:{self.ankleJnt}Ik", mo=True)

        # hide and lock attributes
        lockAndHideAttributes(toeIkCtrl)
        lockAndHideAttributes(ballIkCtrl)

        # put leg ik under ball roll ctrl
        legIk = f"{self.ctrlNameSpace}:ikHandle{self.ankleJnt}"
        cmds.parent(legIk, ballIkCtrl)

    def createToeHeelPivots(self):
        # heel and toe position
        self.heelPivot = drawCtrlCube(name=f"{self.ctrlNameSpace}:{self.side}HeelPivot",
                                      size=3.0,
                                      poleVector=True)
        cmds.setAttr(f"{self.heelPivot}.rotateZ", 90)
        cmds.makeIdentity(self.heelPivot, apply=True)
        self.heelZeroGrp = cmds.group(self.heelPivot, name=f"{self.ctrlNameSpace}:{self.side}HeelZeroGrp")
        
        self.toePivot = drawCtrlCube(name=f"{self.ctrlNameSpace}:{self.side}ToePivot",
                                     size=3.0,
                                     poleVector=True)
        cmds.setAttr(f"{self.toePivot}.rotateZ", 90)
        cmds.makeIdentity(self.toePivot, apply=True)
        self.toeZeroGrp = cmds.group(self.toePivot, name=f"{self.ctrlNameSpace}:{self.side}ToeZeroGrp")

        # set heel pivot position
        cmds.matchTransform(self.heelZeroGrp, f"{self.jntNameSpace}:{self.ankleJnt}", position=True, rotation=False)
        cmds.setAttr(f"{self.heelZeroGrp}.translateY", 0.0)
        heel_z = cmds.getAttr(f"{self.heelZeroGrp}.translateZ")
        cmds.setAttr(f"{self.heelZeroGrp}.translateZ", heel_z-7.0)
        # set toe pivot position
        cmds.matchTransform(self.toeZeroGrp, f"{self.jntNameSpace}:{self.toeJnt}", position=True, rotation=False)
        cmds.setAttr(f"{self.toeZeroGrp}.translateY", 0.0)
        toe_z = cmds.getAttr(f"{self.toeZeroGrp}.translateZ")
        cmds.setAttr(f"{self.toeZeroGrp}.translateZ", toe_z+2.0)

        # hide and lock attributes
        lockAndHideAttributes(self.heelPivot)
        lockAndHideAttributes(self.toePivot)

    def setHeelToeHierarchy(self):
        cmds.parent(self.ballIkZeroGrp, self.heelPivot)
        cmds.parent(self.toeIkZeroGrp, self.heelPivot)
        cmds.parent(self.heelZeroGrp, self.toePivot)
        cmds.parent(self.toeZeroGrp, f"{self.ctrlNameSpace}:ctrl{self.ankleJnt}Ik")
