from limbParams import mixamoArmParams, mixamoLegParams
import constants


leftArmParams = mixamoArmParams(
    ctrlNameSpace=constants.CTRL_NAMESPACE,
    # TODO: move joint names into constants too
    firstJnt="LeftArm",
    secondJnt="LeftForeArm",
    thirdJnt="LeftHand",
    pvRotateY=constants.LEFT_ARM_PV_ROTATE_Y,
    pvOffset=constants.LEFT_ARM_PV_OFFSET,
    ikFkCtrlOffset=constants.LEFT_ARM_IKFK_OFFSET
)

rightArmParams = mixamoArmParams(
    ctrlNameSpace=constants.CTRL_NAMESPACE,
    firstJnt="RightArm",
    secondJnt="RightForeArm",
    thirdJnt="RightHand",
    pvRotateY=constants.RIGHT_ARM_PV_ROTATE_Y,
    pvOffset=constants.RIGHT_ARM_PV_OFFSET,
    ikFkCtrlOffset=constants.RIGHT_ARM_IKFK_OFFSET
)

leftLegParams = mixamoLegParams(
    ctrlNameSpace=constants.CTRL_NAMESPACE,
    firstJnt="LeftUpLeg",
    secondJnt="LeftLeg",
    thirdJnt="LeftFoot",
    toeJnt="LeftToe_End",
    pvRotateY=constants.LEFT_LEG_PV_ROTATE_Y,
    pvOffset=constants.LEFT_LEG_PV_OFFSET,
    ikFkCtrlOffset=constants.LEFT_LEG_IKFK_OFFSET
)

rightLegParams = mixamoLegParams(
    ctrlNameSpace=constants.CTRL_NAMESPACE,
    firstJnt="RightUpLeg",
    secondJnt="RightLeg",
    thirdJnt="RightFoot",
    toeJnt="RightToe_End",
    pvRotateY=constants.RIGHT_LEG_PV_ROTATE_Y,
    pvOffset=constants.RIGHT_LEG_PV_OFFSET,
    ikFkCtrlOffset=constants.RIGHT_LEG_IKFK_OFFSET
)
