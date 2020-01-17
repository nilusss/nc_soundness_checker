# scripts related to the GEO module
import maya.cmds as mc
import maya.mel as mel
import ncsc_API as api


def ncsc_delete_history():
    """Delete the history on all or selected objects
    """

    sel = api.ncsc_get_meshes_from_sel()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval("DeleteHistory")

            print "Deleted history on object: " + obj

    mc.select(clear=True)


def ncsc_get_borders():
    """Select borders on all or selected objects
    """

    if api.ncsc_select_all_objs():
        mc.select(mc.ls(exactType="mesh"))

    mc.polySelectConstraint(m=3, t=0x8000, w=1)
    mc.polySelectConstraint(dis=True)


def ncsc_get_borders_fix():
    """A fix solution for the open borders
    """

    sel = mc.ls(sl=True)

    for obj in sel:
        mc.polyCloseBorder(obj, ch=1)

    mc.select(clear=True)


def ncsc_more_than_four():
    """Checks for polys with more that four sides
    """

    api.ncsc_get_obj_from_pref()

    mel.eval('polyCleanupArgList 4 {"0", "2", "1", "0", "1", "0", "0", "0", "0", "1e-05", "0", "1e-05", "0", "1e-05", "0", "1", "0", "0"}')


def ncsc_more_than_four_fix():
    """Fix polys with more than four sides
    """

    api.ncsc_get_obj_from_pref()

    mel.eval('polyCleanupArgList 4 {"0", "1", "1", "0", "1", "0", "0", "0", "0", "1e-05", "0", "1e-05", "0", "1e-05", "0", "1", "0", "0"}')


def ncsc_normal_dir():
    pass


def ncsc_normal_dir_fix():
    pass


def ncsc_non_manifold_faces():
    """Check for non manifold geometry and select it
    """

    api.ncsc_get_obj_from_pref()

    mel.eval('polyCleanupArgList 3 {"0", "2","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0"}')


def ncsc_non_manifold_faces_fix():
    """Check for non manifold geometry and select it
    """

    api.ncsc_get_obj_from_pref()

    mel.eval('polyCleanupArgList 3 {"0", "1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0"}')

