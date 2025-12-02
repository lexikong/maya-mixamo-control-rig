from maya import cmds
from utils import multiJntFkCtrl, createCircleCtrl
from constants import YELLOW
from shapes import drawCtrlBox, drawCtrlCube, drawCtrlCircle
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

    def createFootIk(self):
        self.createHelperJnts()
        self.createBallToeRoll()
        self.deleteHelperJnts()
        self.createToeHeelPivots()

        self.createFootIkCtrl()

        self.setHeelToeHierarchy()
        self.hideAndLockAttributes()

        self.renameAnkleIkCtrl()
        self.renameFootIkCtrl()

    def renameAnkleIkCtrl(self):
        ankleIkOld = f"{self.ctrlNameSpace}:ctrl{self.ankleJnt}Ik"
        ankleIkZeroOld = f"{self.ctrlNameSpace}:zero{self.ankleJnt}Ik"
        cmds.rename(ankleIkOld, f"{self.ctrlNameSpace}:ctrl{self.side}AnkleIk")
        ankleIkZeroGrp = f"{self.ctrlNameSpace}:zero{self.side}AnkleIk"
        cmds.rename(ankleIkZeroOld, ankleIkZeroGrp)

    def renameFootIkCtrl(self):
        footIkOld = f"{self.ctrlNameSpace}:ctrl{self.side}AllFootIk"
        footIkZeroOld = f"{self.ctrlNameSpace}:zero{self.side}AllFootIk"
        cmds.rename(footIkOld, f"{self.ctrlNameSpace}:ctrl{self.ankleJnt}Ik")
        footZeroGrp = f"{self.ctrlNameSpace}:zero{self.ankleJnt}Ik"
        cmds.rename(footIkZeroOld, footZeroGrp)

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
        #ankleIkZeroGrp = f"{self.ctrlNameSpace}:zero{self.side}AnkleIk"
        #cmds.parent(self.ankleIkZeroGrp, ballIkCtrl)
        ankleZeroGrp = f"{self.ctrlNameSpace}:zero{self.ankleJnt}Ik"
        cmds.parent(ankleZeroGrp, ballIkCtrl)

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

    def setHeelToeHierarchy(self):
        cmds.parent(self.ballIkZeroGrp, self.heelPivot)
        cmds.parent(self.toeIkZeroGrp, self.heelPivot)
        cmds.parent(self.heelZeroGrp, self.toePivot)
        cmds.parent(self.toeZeroGrp, self.footCtrl)

    def createFootIkCtrl(self):
        # create and scale the control shape
        self.footCtrl = drawCtrlCircle(name=f"{self.ctrlNameSpace}:ctrl{self.side}AllFootIk",
                                       radius=1.0,
                                       color=YELLOW)[0]
        cmds.setAttr(f"{self.footCtrl}.scaleX", 12.5)
        cmds.setAttr(f"{self.footCtrl}.scaleZ", 18)
        cmds.makeIdentity(self.footCtrl, apply=True)
        # create the zero group
        footZeroGrp = cmds.group(self.footCtrl, name=f"{self.ctrlNameSpace}:zero{self.side}AllFootIk")
        ballJntTranslate = cmds.xform(f"{self.jntNameSpace}:{self.ballJnt}", q=True, t=True, ws=True)
        ballJntTranslateX = ballJntTranslate[0]
        cmds.setAttr(f"{footZeroGrp}.translateX", ballJntTranslateX)

    def hideAndLockAttributes(self):
        # lock and hide attributes
        attributesExceptRotate = ['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'visibility']
        attributesExceptTranslate = ['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'visibility']
        # hide all attributes except rotation for ankle ctrl
        ankleCtrl = f"{self.ctrlNameSpace}:ctrl{self.side}FootIk"
        #ankleCtrl = f"{self.ctrlNameSpace}:ctrl{self.side}AnkleIk"
        for attr in attributesExceptRotate:
            fullAttrName = f'{ankleCtrl}.{attr}'
            cmds.setAttr(fullAttrName, lock=True)
            cmds.setAttr(fullAttrName, keyable=False)

        # hide all attributes except translate for foot ctrl
        for attr in attributesExceptTranslate:
            fullAttrName = f'{self.footCtrl}.{attr}'
            cmds.setAttr(fullAttrName, lock=True)
            cmds.setAttr(fullAttrName, keyable=False)
