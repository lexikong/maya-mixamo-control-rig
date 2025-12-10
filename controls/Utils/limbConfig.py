from .limbParams import mixamoArmParams, mixamoLegParams
from . import constants


leftArmParams = mixamoArmParams(
    # TODO: move joint names into constants too
    firstJnt="LeftArm",
    secondJnt="LeftForeArm",
    thirdJnt="LeftHand",
    pvRotateY=constants.LEFT_ARM_PV_ROTATE_Y,
    pvOffset=constants.LEFT_ARM_PV_OFFSET,
    ikFkCtrlOffset=constants.LEFT_ARM_IKFK_OFFSET
)

rightArmParams = mixamoArmParams(
    firstJnt="RightArm",
    secondJnt="RightForeArm",
    thirdJnt="RightHand",
    pvRotateY=constants.RIGHT_ARM_PV_ROTATE_Y,
    pvOffset=constants.RIGHT_ARM_PV_OFFSET,
    ikFkCtrlOffset=constants.RIGHT_ARM_IKFK_OFFSET
)

leftLegParams = mixamoLegParams(
    firstJnt="LeftUpLeg",
    secondJnt="LeftLeg",
    thirdJnt="LeftFoot",
    ballJnt="LeftToeBase",
    toeJnt="LeftToe_End",
    pvRotateY=constants.LEFT_LEG_PV_ROTATE_Y,
    pvOffset=constants.LEFT_LEG_PV_OFFSET,
    ikFkCtrlOffset=constants.LEFT_LEG_IKFK_OFFSET,
    side="Left"
)

rightLegParams = mixamoLegParams(
    firstJnt="RightUpLeg",
    secondJnt="RightLeg",
    thirdJnt="RightFoot",
    ballJnt="RightToeBase",
    toeJnt="RightToe_End",
    pvRotateY=constants.RIGHT_LEG_PV_ROTATE_Y,
    pvOffset=constants.RIGHT_LEG_PV_OFFSET,
    ikFkCtrlOffset=constants.RIGHT_LEG_IKFK_OFFSET,
    side="Right"
)
