""" scripts related to the GEO module """

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
    """Select the normals that are turning the "wrong" way
    """

    sel = mc.ls(sl=True)

    if sel:
        obj_face_normal = []
        dup_obj_face_normal = []
        for index, obj in enumerate(sel):
            face_count = mc.polyEvaluate(obj, f=True)
            # Iterate through the object's faces and get the normal vector using api.face_normal
            for index in range(face_count):
                obj_face_normal.append(api.face_normal('{}.f[{}]'.format(obj,index)))

            # Duplicate the original object and run "conform", to get the correct normal vector
            dup_obj = mc.duplicate(rr=True)[0]
            mc.polyNormal(dup_obj, normalMode=2, userNormalMode=0, ch=1)
            mc.select(clear=True)
            face_count = mc.polyEvaluate(dup_obj, f=True)
            # Iterate through the duplicate object's faces and get the normal vector using api.face_normal
            for index in range(face_count):
                dup_obj_face_normal.append(api.face_normal('{}.f[{}]'.format(dup_obj, index)))

            mc.select(clear=True)
            # Compare face normals, and select the ones that are different on the original object
            for index in range(len(obj_face_normal)):
                if obj_face_normal[index] != dup_obj_face_normal[index]:
                    mc.select(obj + '.f[{}]'.format(index), add=True)

            face_sel = mc.ls(sl=True)

            return face_sel
    else:
        mc.warning("No objects selected!")


def ncsc_normal_dir_fix(poly_sel):
    """Reverse the selected polygons
    """

    if poly_sel:
        mc.polyNormal(normalMode=0, userNormalMode=0, ch=1)
    else:
        mc.warning("No faces have been selected! Run \"Face Normal Direction - Perform\" first.")


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


def ncsc_lamina_faces():
    """Check for lamina faces and select them
    """

    api.ncsc_get_obj_from_pref()
    mel.eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","1","0" }')


def ncsc_lamina_faces_fix():
    """Check for lamina faces and select them
    """

    api.ncsc_get_obj_from_pref()
    mel.eval('polyCleanupArgList 4 { "0","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","1","0" }')
