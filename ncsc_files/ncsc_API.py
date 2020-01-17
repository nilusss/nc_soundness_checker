#
#
import maya.cmds as mc


def ncsc_select_all_objs():
    """Return all objects in the scene

    Returns:
        list -- Return all objects using a checkbox from the UI
    """

    if mc.window("nc_soundness_checker", exists=True):
        return mc.menuItem("ncsc_select_all_geo", q=True, checkBox=True)


def ncsc_get_mesh(obj):
    """Return the object if it is of type 'mesh'

    Arguments:
        obj {string} -- Object to check if it is of type 'mesh'

    Returns:
        string -- Final object that is of type 'mesh'
    """

    obj_type = mc.objectType(obj)

    if obj_type == "mesh":
        return obj
    elif obj_type == "transform":
        shapes = mc.listRelatives(obj, type="mesh")[0]
        return shapes


def ncsc_get_meshes_from_sel():
    """Get a list of all selected objects in the viewport

    Returns:
        list -- All objects from the viewport that are of type 'mesh'
    """

    sel = mc.ls(sl=True)
    meshes = [ncsc_get_mesh(obj) for obj in sel]
    return meshes


def ncsc_get_obj_from_pref():
    """Select objects based on preference

    Returns:
        list -- Objects based on preference
    """

    sel = []

    if ncsc_select_all_objs():
        sel = mc.ls(exactType="mesh")
    else:
        sel = ncsc_get_meshes_from_sel()

    return sel
