# This file was created with the assistance of ChatGPT

import maya.OpenMayaUI as omui

# PySide compatibility
try:
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6 import QtWidgets, QtCore
    from shiboken6 import wrapInstance

from ..Controls.startup import RigBuilder


WINDOW_TITLE = "MixamoControlRig"
WINDOW_NAME = "MixamoControlRigWindow"
TEXT_HEIGHT = 30
MIN_WIDTH = 350
SPACING = 8
TEXT_FIELD_WIDTH = (200, 100)

DEV_MODE = True


def getMayaMainWindow():
    mainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindowPtr), QtWidgets.QWidget)


class MixamoControlRigUI(QtWidgets.QDialog):

    def __init__(self, parent=getMayaMainWindow()):
        super().__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)
        self.setObjectName(WINDOW_NAME)
        self.setMinimumWidth(MIN_WIDTH)

        self._buildUi()
        self._connectSignals()

    def _buildUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setSpacing(SPACING)

        # instruction
        instructionLabel = QtWidgets.QLabel("Select the hip joint to start")
        instructionLabel.setFixedHeight(TEXT_HEIGHT)
        instructionLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        mainLayout.addWidget(instructionLabel)

        # namespace field
        nsLayout = QtWidgets.QHBoxLayout()
        nsLabel = QtWidgets.QLabel("Control NameSpace")
        nsLabel.setFixedWidth(TEXT_FIELD_WIDTH[0])

        self.namespaceField = QtWidgets.QLineEdit()
        self.namespaceField.setPlaceholderText("e.g. ctrl")
        self.namespaceField.setText("ctrl")
        self.namespaceField.setFixedWidth(TEXT_FIELD_WIDTH[1])

        nsLayout.addWidget(nsLabel)
        nsLayout.addWidget(self.namespaceField)
        nsLayout.addStretch()
        mainLayout.addLayout(nsLayout)

        # skeleton LOD menu
        lodLayout = QtWidgets.QHBoxLayout()
        lodLabel = QtWidgets.QLabel("Skeleton LOD")
        lodLabel.setFixedWidth(TEXT_FIELD_WIDTH[0])

        self.skeletonMenu = QtWidgets.QComboBox()
        self.skeletonMenu.addItems([
            "Standard Skeleton (65)",
            "3 Chain Finger (49)",
            "2 Chain Finger (41)",
            "No Finger (25)",
        ])

        lodLayout.addWidget(lodLabel)
        lodLayout.addWidget(self.skeletonMenu)
        lodLayout.addStretch()
        mainLayout.addLayout(lodLayout)

        # create button
        self.createButton = QtWidgets.QPushButton("Create Control Rigs")
        mainLayout.addWidget(self.createButton)

    def _connectSignals(self):
        self.createButton.clicked.connect(self.createCtrls)

    def createCtrls(self):
        ctrlNamespace = self.namespaceField.text()
        skeletonLod = self.skeletonMenu.currentIndex() + 1
        # pass the user inputs to RigBuilder
        rigBuilder = RigBuilder()
        rigBuilder.start(ctrlNamespace, skeletonLod)


def createUI():
    # DEV ONLY: reload modules
    if DEV_MODE:
        import sys
        import importlib

        modulesToReload = [
            "mixamoControlRig.Controls.startup",
            "mixamoControlRig.Controls.Rigs",
            "mixamoControlRig.Controls.Rigs.arm",
            "mixamoControlRig.Controls.Rigs.leg",
            "mixamoControlRig.Controls.Rigs.limb",
            "mixamoControlRig.Controls.Rigs.cog",
            "mixamoControlRig.Controls.Rigs.fingers",
            "mixamoControlRig.Controls.Rigs.foot",
            "mixamoControlRig.Controls.Rigs.head",
            "mixamoControlRig.Controls.Rigs.shoulders",
            "mixamoControlRig.Controls.Rigs.spine",
            "mixamoControlRig.Controls.Rigs.world",
            "mixamoControlRig.Controls.Utils",
            "mixamoControlRig.Controls.Utils.constants",
            "mixamoControlRig.Controls.Utils.helpers",
            "mixamoControlRig.Controls.Utils.limbConfig",
            "mixamoControlRig.Controls.Utils.limbParams",
            "mixamoControlRig.Controls.Utils.orientJoints",
            "mixamoControlRig.Controls.Utils.shapes",
            "mixamoControlRig.Controls.Utils.userInput",
            "mixamoControlRig.UI",
            "mixamoControlRig.UI.ui",
        ]

        for m in modulesToReload:
            if m in sys.modules:
                importlib.reload(sys.modules[m])

    # close existing window
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == WINDOW_NAME:
            widget.close()
            widget.deleteLater()

    ui = MixamoControlRigUI()
    ui.show()
    return ui
