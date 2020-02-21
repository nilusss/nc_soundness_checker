""" scripts related to the GEO module """

import maya.cmds as mc
import maya.mel as mel
import ncsc_API as api
from collections import namedtuple

selectiontype = namedtuple('selectiontype', 'faces verts edges')


def get_selected_components():
    sel = mc.ls(sl=True, type='float3') # this is obscure maya way to get only components
    faces = mc.polyListComponentConversion(sel, ff=True, tf=True)
    verts = mc.polyListComponentConversion(sel, fv=True, tv=True)
    edges = mc.polyListComponentConversion(sel, fe=True, te=True)
    return selectiontype(faces, verts, edges)


def ncsc_delete_history():
    """Delete the history on all or selected objects
    """

    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval("DeleteHistory")

            print "Deleted history on object: " + obj

    mc.select(clear=True)


def ncsc_get_borders():
    """Select borders on all or selected objects
    """

    a = []
    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mc.polySelectConstraint(m=3, t=0x8000, w=1)
            mc.polySelectConstraint(dis=True)
            a.extend(mc.ls(sl=True))

    mc.select(a, add=True)


def ncsc_get_borders_fix():
    """A fix solution for the open borders
    """

    sel = mc.ls(sl=True)

    for obj in sel:
        mc.polyCloseBorder(obj, ch=1)

    mc.select(clear=True)


def ncsc_more_than_four():
    """Checks for polys with more than four sides
    """

    a = []
    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('polyCleanupArgList 4 {"0", "2", "1", "0", "1", "0", "0", "0", "0", "1e-05", "0", "1e-05", "0", "1e-05", "0", "1", "0", "0"}')
            a.extend(mc.ls(sl=True))

    mc.select(a, add=True)


def ncsc_more_than_four_fix():
    """Fix polys with more than four sides
    """

    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('polyCleanupArgList 4 {"0", "1", "1", "0", "1", "0", "0", "0", "0", "1e-05", "0", "1e-05", "0", "1e-05", "0", "1", "0", "0"}')


def ncsc_normal_dir():
    """Select the normals that are turning the "wrong" way
    """

    a = []
    sel = api.ncsc_get_obj_from_pref()
    if sel:
        for index, obj in enumerate(sel):
            obj_face_normal = []
            dup_obj_face_normal = []
            if mc.objExists(obj):

                # Duplicate the original object and run "conform", to get the correct normal vector
                mc.select(obj)
                dup_obj = mc.duplicate(name="dup_" + obj,rr=False)[0]
                mc.polyNormal(normalMode=2, userNormalMode=1, ch=1)
                mc.select(clear=True)
                face_count = mc.polyEvaluate(dup_obj, f=True)

                if isinstance(face_count, int):

                    # Iterate through the duplicate and original object's faces and get the normal vector using api.face_normal
                    for i in range(face_count):
                        obj_face_normal.append(api.face_normal('{}.f[{}]'.format(obj, i)))
                        dup_obj_face_normal.append(api.face_normal('{}.f[{}]'.format(dup_obj, i)))

                    mc.select(clear=True)
                    # Compare face normals, and select the ones that are different on the original object
                    for index in range(len(obj_face_normal)):
                        if obj_face_normal[index] != dup_obj_face_normal[index]:
                            print obj_face_normal[index]
                            print dup_obj_face_normal[index]
                            mc.select(obj + '.f[{}]'.format(index), add=True)
                            a.extend(mc.ls(sl=True))
                mc.delete(dup_obj)
                mc.select(clear=True)
            else:
                mc.warning("No objects selected!")
            mc.select(a, add=True)


def ncsc_normal_dir_fix():
    """Reverse the selected polygons
    """

    selected = get_selected_components()
    if selected.faces:
        mc.polyNormal(normalMode=0, userNormalMode=0, ch=1)
        mc.select(clear=True)
    else:
        mc.warning("No faces have been selected! Run \"Normal Direction - Show\" first.")


def ncsc_non_manifold_faces():
    """Check for non manifold geometry and select it
    """

    a = []
    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('polyCleanupArgList 3 {"0", "2","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0"}')
            a.extend(mc.ls(sl=True))

    mc.select(a, add=True)

def ncsc_non_manifold_faces_fix():
    """Check for non manifold geometry and select it
    """

    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('polyCleanupArgList 3 {"0", "1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0"}')


def ncsc_lamina_faces():
    """Check for lamina faces and select them
    """

    a = []
    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","1","0" }')
            a.extend(mc.ls(sl=True))

    mc.select(a, add=True)

def ncsc_lamina_faces_fix():
    """Check for lamina faces and select them
    """

    sel = api.ncsc_get_obj_from_pref()

    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('polyCleanupArgList 4 { "0","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","1","0" }')
