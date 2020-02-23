#
#
import maya.cmds as mc


def ncsc_select_all_objs():
    """Return all objects in the scene

    Returns:
        list -- Return all objects using a checkbox from the UI
    """

    if mc.optionVar(q='ncsc_checbox') == 1:
        return mc.optionVar(q='ncsc_checbox')


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
    try:
        sel = mc.ls(sl=True)
        meshes = [ncsc_get_mesh(obj) for obj in sel]
        return meshes
    except:
        return False


def ncsc_get_obj_from_pref():
    """Select objects based on preference

    Returns:
        list -- Objects based on preference
    """

    sel = []
    if ncsc_select_all_objs():
        sel = []
        mesh = mc.ls(exactType="mesh")
        for obj in mesh:
            rel = mc.listRelatives(obj, parent=True)
            sel.extend(rel)
    else:
        sel = ncsc_get_meshes_from_sel()

    if sel:
        return sel
    else:
        mc.warning("No nodes have been selected!")
        return False


def face_normal(face):
    polyface = mc.polyListComponentConversion(face, tvf=True)
    xes = mc.polyNormalPerVertex(polyface, q=True, x=True)
    yes = mc.polyNormalPerVertex(polyface, q=True, y=True)
    zes = mc.polyNormalPerVertex(polyface, q=True, z=True)
    divisor = 1.0 / len(xes)
    return sum(xes) * divisor, sum(yes) * divisor, sum(zes) * divisor
