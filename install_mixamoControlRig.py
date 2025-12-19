"""
This file was created with the assistance of ChatGPT and Gemini

Mixamo Control Rig Installer
Version: 1.0
Last Update: Dec 17, 2025

HOW TO USE:
    1. Open Autodesk Maya
    2. Drag and drop this file into the Maya 3D Viewport

FOLDER STRUCTURE:
    The installer expects the following layout:
    /mixamoControlRig_v1/
        ├── install_mixamoControlRig.py (this file)
        ├── mixamoRigIcon.png
        └── mixamoControlRig/
            ├── Controls/
            └── UI/

WHAT IT DOES:
    - Detect its current location
    - Copy the tool folder to your Maya modules directory
    - Create a .mod file
    - Create a shelf button in the 'Custom' tab
    - Launch the UI immediately
"""

import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import shutil
import traceback
import stat


TOOL_FOLDER_NAME = "mixamoControlRig"
TOOL_VERSION = "1.0"
SHELF_TAB = "Custom"
BUTTON_LABEL = "Rig"
ICON_FILENAME = "mixamoRigIcon.png"


# Helper Functions
def getMayaModulesPath():
    """Return Maya user modules directory."""
    userDir = cmds.internalVar(userAppDir=True)
    modulesDir = os.path.join(userDir, "modules")
    if not os.path.exists(modulesDir):
        os.makedirs(modulesDir)
    return modulesDir


def createModFile(moduleDir):
    """Create .mod file pointing to the tool folder with forward slashes."""
    modPath = os.path.join(getMayaModulesPath(), f"{TOOL_FOLDER_NAME}.mod")
    # Ensure forward slashes
    moduleDirFixed = moduleDir.replace("\\", "/")
    content = f"+ {TOOL_FOLDER_NAME} {TOOL_VERSION} {moduleDirFixed}"
    with open(modPath, "w") as f:
        f.write(content)
    print(f".mod file created at {modPath} with path: {moduleDirFixed}")


def getShelfLayout():
    return mel.eval('$tmpVar = $gShelfTopLevel')


def ensureShelf(shelfName):
    shelfTab = getShelfLayout()
    shelves = cmds.shelfTabLayout(shelfTab, q=True, childArray=True) or []
    if shelfName not in shelves:
        cmds.shelfLayout(shelfName, parent=shelfTab)
    return shelfName


def removeExistingButton(shelf, label):
    children = cmds.shelfLayout(shelf, q=True, childArray=True) or []
    for child in children:
        if cmds.shelfButton(child, q=True, label=True) == label:
            cmds.deleteUI(child)


def createShelfButton(modulesDir, installerDir):
    """Creates the shelf button using the parent directory path."""
    shelf = ensureShelf(SHELF_TAB)
    removeExistingButton(shelf, BUTTON_LABEL)

    # modulesDir is the path containing the 'mixamoControlRig' folder.
    modulesDirFixed = modulesDir.replace("\\", "/")

    command = f"""
import sys
toolParentDir = r'{modulesDirFixed}'
if toolParentDir not in sys.path:
    sys.path.append(toolParentDir)
from {TOOL_FOLDER_NAME}.UI import ui
ui.createUI()
""".strip()

    iconPath = os.path.join(installerDir, ICON_FILENAME)
    if not os.path.exists(iconPath):
        iconPath = "commandButton.png"

    cmds.shelfButton(
        label=BUTTON_LABEL,
        parent=shelf,
        command=command,
        annotation=f"Launch {TOOL_FOLDER_NAME} Tool",
        image=iconPath,
        style="iconOnly"
    )


def removeReadonly(func, path, excinfo):
    """Handle read-only files for shutil.rmtree on Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def ensureInitFiles(toolDst):
    """Ensure __init__.py exists in main folder and UI subfolder."""
    mainInit = os.path.join(toolDst, "__init__.py")
    uiInit = os.path.join(toolDst, "UI", "__init__.py")
    os.makedirs(os.path.dirname(uiInit), exist_ok=True)
    for f in [mainInit, uiInit]:
        if not os.path.exists(f):
            open(f, "w").close()


# Main Installer
def onMayaDroppedPythonFile(*args):
    # Determine the path of the dropped file
    filePath = None
    if args and isinstance(args[0], str) and os.path.exists(args[0]):
        filePath = args[0]
    elif '__file__' in globals() and os.path.exists(__file__):
        filePath = __file__
    else:
        cmds.warning("❌ Installation failed: Could not determine script path.")
        return

    filePath = os.path.normpath(filePath)

    try:
        installerDir = os.path.dirname(filePath)
        toolSrc = os.path.join(installerDir, TOOL_FOLDER_NAME)

        if not os.path.exists(toolSrc):
            cmds.warning(f"Could not find {TOOL_FOLDER_NAME} folder next to installer. Looked here: {toolSrc}")
            return

        # Destination: Maya modules directory
        modulesDir = getMayaModulesPath()
        toolDst = os.path.join(modulesDir, TOOL_FOLDER_NAME)

        # Remove existing tool folder if present
        if os.path.exists(toolDst):
            shutil.rmtree(toolDst, onerror=removeReadonly)

        # Copy tool folder
        shutil.copytree(toolSrc, toolDst)
        print(f"{TOOL_FOLDER_NAME} copied to {toolDst}")

        # Ensure __init__.py files exist
        ensureInitFiles(toolDst)

        # Create .mod file with forward slashes
        createModFile(toolDst)

        # Add the PARENT directory to sys.path for current session
        modulesDirFixed = modulesDir.replace("\\", "/")
        if modulesDirFixed not in sys.path:
            sys.path.append(modulesDirFixed)
            print(f"Added to sys.path for current session: {modulesDirFixed}")

        # Launch UI
        from mixamoControlRig.UI import ui
        ui.createUI()

        # Add shelf button
        createShelfButton(modulesDir, installerDir)

        cmds.inViewMessage(
            amg=f"<hl>{TOOL_FOLDER_NAME} Installed!</hl> Shelf button added ✔",
            pos="midCenter",
            fade=True
        )
        print("🎉 Installation complete.")

    except Exception:
        traceback.print_exc()
        cmds.warning("❌ Installation failed — see Script Editor for details.")


# Ensure script runs when dropped
if __name__ == "__main__":
    onMayaDroppedPythonFile(__file__)
