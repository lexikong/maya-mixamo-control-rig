# User input from UI

class UserInput:
    ctrlNameSpace: str = ""
    fingers: list[str] = []

    @classmethod
    def setCtrlNS(cls, ctrlNameSpace: str):
        cls.ctrlNameSpace = ctrlNameSpace

    @classmethod
    def setFingers(cls, skeletonIndex: int):
        # Standard Skeleton
        if (skeletonIndex == 1):
            cls.fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        # 3 Chain Finger
        elif (skeletonIndex == 2):
            cls.fingers = ["Thumb", "Index", "Ring"]
        # 2 Chain Finger
        elif (skeletonIndex == 3):
            cls.fingers = ["Thumb", "Index"]
        elif (skeletonIndex == 4):
            cls.fingers = []

    @classmethod
    def getCtrlNS(cls):
        return cls.ctrlNameSpace

    @classmethod
    def getFingers(cls):
        return cls.fingers
