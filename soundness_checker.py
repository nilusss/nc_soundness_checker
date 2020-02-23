#       nc_soundness_checker
#       Version 0.0.1
#       Copyright (C)2020 Nilas Niebuhr
#       Email: niebuhrgfx@gmail.com
#       Last Modified: 16/01/2020
#
#
# nc_checker is a collection of maya tools, making it easier for the
# modelling lead to check for invalid geometry and more.
#
# For detailed instructions read the "readme.txt" file
#

import os
import pprint
import sys

import maya.cmds as mc
import maya.OpenMayaUI as omui
import shiboken2
import ncsc_files.ncsc_geo as geo
import ncsc_files.ncsc_transform as trans
import ncsc_files.ncsc_naming as naming
import ncsc_files.ncsc_uv as uv
from PySide2 import QtCore, QtGui, QtUiTools, QtWidgets
from pyside2uic import compileUi

reload(geo)

try:
    from ncsc_ui import soundness_checker_ui as scui
    reload(scui)
except ImportError:
    mc.warning("No UI Found. Please compile")


def compile_ui(fdir, file_name):
    py_file_name = file_name.split(".")[0] + ".py"
    pyfile = open("{}/{}".format(fdir, py_file_name), 'w')
    compileUi("{}/{}".format(fdir, file_name), pyfile, False, 4, False)
    pyfile.close()
    from ncsc_ui import soundness_checker_ui as scui
    reload(scui)


def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(main_window), QtWidgets.QWidget)


class SoundnessCheckerWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SoundnessCheckerWindow, self).__init__(parent)
        self.setWindowTitle("Soundness Checker")
        self.setParent(parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = scui.Ui_SoundnessChecker()
        self.ui.setupUi(self)

        mc.optionVar(iv=('ncsc_checbox', 0))

        self.ui.checkBox.clicked.connect(self.checkbox_state)

        # ## Geometry ## #
        # Delete history
        self.ui.dh_fix_btn.clicked.connect(self.dh_fix)

        # Get borders
        self.ui.gb_fix_btn.clicked.connect(self.gb_fix)
        self.ui.gb_show_btn.clicked.connect(self.gb_show)

        # More than four sides
        self.ui.mtf_fix_btn.clicked.connect(self.mtf_fix)
        self.ui.mtf_show_btn.clicked.connect(self.mtf_show)

        # Find poly normal direction
        self.ui.nd_fix_btn.clicked.connect(self.nd_fix)
        self.ui.nd_show_btn.clicked.connect(self.nd_show)

        # Non manifold faces
        self.ui.nm_fix_btn.clicked.connect(self.nm_fix)
        self.ui.nm_show_btn.clicked.connect(self.nm_show)

        # Non manifold faces
        self.ui.lf_fix_btn.clicked.connect(self.lf_fix)
        self.ui.lf_show_btn.clicked.connect(self.lf_show)

        # ## Transform ## #
        # Freeze transform
        self.ui.ft_all_btn.clicked.connect(self.ft_all)
        self.ui.ft_selected_btn.clicked.connect(self.ft_selected)

        # Place top node
        self.ui.ptn_fix_btn.clicked.connect(self.ptn_fix)

        # Zero pivot
        self.ui.zp_all_btn.clicked.connect(self.zp_all)
        self.ui.zp_selected_btn.clicked.connect(self.zp_selected)

        # Center pivot
        self.ui.cp_all_btn.clicked.connect(self.cp_all)
        self.ui.cp_selected_btn.clicked.connect(self.cp_selected)

        # Zero object
        self.ui.zo_all_btn.clicked.connect(self.zo_all)
        self.ui.zo_selected_btn.clicked.connect(self.zo_selected)

        # Move above zero
        self.ui.maz_all_btn.clicked.connect(self.maz_all)
        self.ui.maz_selected_btn.clicked.connect(self.maz_selected)

        # ## Naming ## #
        # Material and Shading Group prefix
        self.ui.cm_fix_btn.clicked.connect(self.cm_fix)

        # Add suffix to groups and geometry
        self.ui.cs_fix_btn.clicked.connect(self.cs_fix)

        # ## UV's ## #
        # Overlapping UV's
        self.ui.ou_show_btn.clicked.connect(self.ou_show)

        # Inverted UV's
        self.ui.iu_show_btn.clicked.connect(self.iu_show)

    def checkbox_state(self):
        if self.ui.checkBox.isChecked():
            print "is checked"
            mc.optionVar(iv=('ncsc_checbox', 1))
        else:
            self.ui.checkBox.setChecked(False)
            print "not checked"
            mc.optionVar(iv=('ncsc_checbox', 0))

    # ## Geometry ## #

    def dh_fix(self):
        geo.ncsc_delete_history()

    def dh_show(self):
        print "show"

    def gb_fix(self):
        geo.ncsc_get_borders_fix()

    def gb_show(self):
        geo.ncsc_get_borders()

    def mtf_fix(self):
        geo.ncsc_more_than_four_fix()

    def mtf_show(self):
        geo.ncsc_more_than_four()

    def nd_fix(self):
        geo.ncsc_normal_dir_fix()

    def nd_show(self):
        geo.ncsc_normal_dir()

    def nm_fix(self):
        geo.ncsc_non_manifold_faces_fix()

    def nm_show(self):
        geo.ncsc_non_manifold_faces()

    def lf_fix(self):
        geo.ncsc_lamina_faces_fix()

    def lf_show(self):
        geo.ncsc_lamina_faces()

    # ## Transform ## #

    def ft_all(self):
        trans.ncsc_freeze_trans(all=True)

    def ft_selected(self):
        trans.ncsc_freeze_trans(all=False)

    def ptn_fix(self):
        trans.ncsc_place_top_node()

    def ptn_show(self):
        trans.ncsc_place_top_node()

    def zp_all(self):
        trans.ncsc_zero_pivot(all=True)

    def zp_selected(self):
        trans.ncsc_zero_pivot(all=False)

    def cp_all(self):
        trans.ncsc_center_pivot(all=True)

    def cp_selected(self):
        trans.ncsc_center_pivot(all=False)

    def zo_all(self):
        trans.ncsc_zero_object(all=True)

    def zo_selected(self):
        trans.ncsc_zero_object(all=False)

    def maz_all(self):
        trans.ncsc_move_above_zero(all=True)

    def maz_selected(self):
        trans.ncsc_move_above_zero(all=False)

    # ## Naming ## #
    def cm_fix(self):
        naming.ncsc_materials()

    def cs_fix(self):
        naming.ncsc_suffix()

    # ## UV's ## #
    def ou_show(self):
        uv.ncsc_overlapping_uvs()

    def iu_show(self):
        uv.ncsc_inverted_uvs()


def openui():
    try:
        ui.deleteLater()
    except NameError as e:
        pass

    ui = SoundnessCheckerWindow(parent=maya_main_window())
    ui.setWindowTitle("Soundness Checker")
    ui.show()


"""# This scripts location
SCRIPT_LOC = os.path.split(__file__)[0]


def loadUiWidget(uifilename, parent=None):
    Properly Loads and returns UI files - by BarryPye on stackOverflow
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui


class SoundnessChecker(QtGui.QMainWindow):

    def __init__(self):
        mainUI = SCRIPT_LOC + "/ncsc_ui/soundness_checker_ui.ui"
        MayaMain = shiboken2.wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget)
        super(SoundnessChecker, self).__init__(MayaMain)

        # main window load / settings
        self.MainWindowUI = loadUiWidget(mainUI, MayaMain)
        self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  
        self.MainWindowUI.destroyed.connect(self.onExitCode)
        self.MainWindowUI.show()

    def openUI(self):
        Command within Maya to run this script
        if not (mc.window("demoUI", exists=True)):
            SoundnessChecker()
        else:
            sys.stdout.write("tool is already open!\n")"""
