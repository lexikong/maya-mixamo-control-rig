from dataclasses import dataclass


@dataclass
class mixamoLimbParams:
    firstJnt: str
    secondJnt: str
    thirdJnt: str
    pvRotateY: float
    pvOffset: tuple
    ikFkCtrlOffset: tuple


@dataclass
class mixamoArmParams(mixamoLimbParams):
    pass


@dataclass
class mixamoLegParams(mixamoLimbParams):
    ballJnt: str
    toeJnt: str
    side: str
