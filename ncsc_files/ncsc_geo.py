# scripts related to the GEO module
import maya.cmds as mc
import maya.mel as mel
import ncsc_API as api


def ncsc_delete_history():
    sel = api.ncsc_get_meshes_from_sel()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval("DeleteHistory")

            print "Deleted history on object: " + obj

    mc.select(clear=True)


def ncsc_get_borders():
    if api.ncsc_select_all_objs():
        mc.select(mc.ls(exactType="mesh"))
    mc.polySelectConstraint(m=3, t=0x8000, w=1)
    mc.polySelectConstraint(dis=True)


def ncsc_get_borders_fix():
    sel = mc.ls(sl=True)

    for obj in sel:
        mc.polyCloseBorder(obj, ch=1)

    mc.select(clear=True)
