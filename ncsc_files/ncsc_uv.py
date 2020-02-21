""" scripts related to the Transform module """

import os

import ncsc_API as api

try:
    import maya.cmds as mc
    import maya.mel as mel
except ImportError:
    pass


def ncsc_open_uv_seams():
    