""" scripts related to the Naming module """

import os
import maya.OpenMaya as om

try:
    import maya.cmds as mc
    import maya.mel as mel
except ImportError:
    pass


def ncsc_materials():

    # Iterate through material nodes
    sel = mc.ls(materials=True)
    for mat in sel:
        if "tex_" not in mat:
            nn = "tex_{}".format(mat)
            try:
                mc.rename(mat, nn)
                om.MGlobal.displayInfo("## Material prefix has been added to \"{}\"".format(mat))
            except:
                pass

    # Iterate through shading group nodes
    sel = mc.ls(type="shadingEngine")
    for sg in sel:
        if "sg_" not in sg:
            nn = "sg_{}".format(sg)
            try:
                mc.rename(sg, nn)
                om.MGlobal.displayInfo("## Material prefix has been added to \"{}\"".format(sg))
            except:
                pass


def ncsc_suffix():
    shape_list = mc.ls(type='nurbsCurve')
    if shape_list:
        shape_transform_list = mc.listRelatives(shape_list, parent=True)
    else:
        shape_transform_list = []

    mesh_list = mc.ls(type='mesh')
    if mesh_list:
        mesh_transform_list = mc.listRelatives(mesh_list, parent=True)
    else:
        mesh_transform_list = []

    nurbs_list = mc.ls(type='nurbsSurface')
    if nurbs_list:
        nurbs_transform_list = mc.listRelatives(nurbs_list, parent=True)
    else:
        nurbs_transform_list = []

    for obj in mesh_transform_list:
        if "_geo" not in obj:
            nn = "{}_geo".format(obj)
            try:
                mc.rename(obj, nn)
                om.MGlobal.displayInfo("## Geometry suffix has been added to \"{}\"".format(obj))
            except:
                pass

    sel = mc.ls(transforms=True, shapes=False)
    for grp in sel:
        if grp not in shape_transform_list + shape_list + mesh_transform_list + nurbs_transform_list:
            if "_grp" not in grp and "_geo" not in grp:
                nn = "{}_grp".format(grp)
                try:
                    mc.rename(grp, nn)
                    om.MGlobal.displayInfo("## Group suffix has been added to \"{}\"".format(grp))
                except:
                    pass