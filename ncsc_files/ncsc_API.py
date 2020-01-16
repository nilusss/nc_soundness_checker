#
#
import maya.cmds as mc


def ncsc_select_all_objs():
    return mc.menuItem("ncsc_select_all_geo", q=True, checkbox=True)


def ncsc_get_mesh(obj):

    obj_type = mc.objectType(obj)

    if obj_type == "mesh":
        return obj
    elif obj_type == "transform":
        shapes = mc.listRelatives(obj, type="mesh")[0]
        return shapes


def ncsc_get_meshes_from_sel():
    sel = mc.ls(sl=True)
    meshes = [ncsc_get_mesh(obj) for obj in sel]
    return meshes


def ncsc_get_obj_from_pref():
    sel = []

    if ncsc_select_all_objs():
        sel = mc.ls(exactType="mesh")
    else:
        sel = ncsc_get_meshes_from_sel()

    return sel
