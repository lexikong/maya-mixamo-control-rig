from maya import cmds


def cleanup():
    # remove all arm FK and IK joints
    fkJoints = cmds.ls("*Fk", recursive=True)
    if fkJoints:
        cmds.delete(fkJoints)
    ikJoints = cmds.ls("*Ik", recursive=True)
    if ikJoints:
        cmds.delete(ikJoints)
    reverseNodes = cmds.ls(type="reverse", recursive=True)
    for node in reverseNodes:
        cmds.delete(node)
    return
