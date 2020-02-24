import os

import maya.cmds as mc
import maya.mel as mel


def onMayaDroppedPythonFile(*args):

    filePath = os.path.dirname(os.path.abspath(__file__))

    mel.eval('global string $gShelfTopLevel;')
    gShelfTopLevel = mel.eval('$tmp=$gShelfTopLevel;')
    # get top shelf names
    getShelf = mc.tabLayout(gShelfTopLevel, query=True, selectTab=True)

    mc.setParent(getShelf)
    mc.shelfButton(command="from nc_soundness_checker import soundness_checker as sc; sc.openui()",
                   annotation="Soundness Checker",
                   label="SC",
                   image=filePath + "/icons/icon.png",
                   image1=filePath + "/icons/icon.png",
                   sourceType="python")
