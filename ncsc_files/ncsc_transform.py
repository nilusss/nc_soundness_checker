""" scripts related to the Transform module """

import os
import maya.OpenMaya as om
import ncsc_API as api

try:
    import maya.cmds as mc
    import maya.mel as mel
except ImportError:
    pass


def ncsc_freeze_trans(all=False):
    """Freeze transforms on the selected node
    """

    sel = mc.ls(sl=True)
    complete = True

    if all is True:
        sel = mc.ls(geometry=True, transforms=True)
        for obj in sel:
            mc.select(obj)
            try:
                mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
            except RuntimeError as e:
                om.MGlobal.displayError("## Node {}: ".format(obj) + str(e))
                complete = False
        mc.select(clear=True)
        if complete is True:
            om.MGlobal.displayInfo("## Froze transforms on all nodes!")
    elif sel:
        for obj in sel:
            try:
                mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
            except RuntimeError as e:
                om.MGlobal.displayError("## Node {}: ".format(obj) + str(e))
                complete = False
        if complete is True:
            om.MGlobal.displayInfo("## Froze transforms on selected node(s)!")
    else:
        mc.warning("No nodes have been selected!")


def ncsc_place_top_node():
    """Selects all geometry in the scene and places it in a top node
    """
    filepath = mc.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    asset_name = filename.split("_")[0].split(".")[0]
    grp_node_name = asset_name + "_grp"
    sel = mc.ls(geometry=True)
    if not sel:
        mc.warning("You need to have geometry in your scene")
    elif mc.objExists(grp_node_name):
        mc.warning("You already have a \"_grp\" node")
    else:
        grp_node = mc.createNode("transform", n=grp_node_name)
        sel = mc.ls(assemblies=True, l=True)
        temp_sel = []
        for s in range(len(sel)):
            temp_sel = mc.listRelatives(sel[s], s=True)
            if sel[s] == "|"+grp_node_name:
                continue
            if temp_sel is None or mc.objectType(temp_sel[0]) == "mesh":
                mc.parent(sel[s], grp_node)
        mc.select(grp_node_name)
        om.MGlobal.displayInfo("## Top node placed!")


def ncsc_zero_pivot(all=False):
    """Places the node pivot in world 0, 0, 0
    """

    sel = mc.ls(sl=True)

    if all is True:
        sel = mc.ls(geometry=True, transforms=True)
        for obj in sel:
            mc.select(obj)
            mc.move(0, 0, 0, ".scalePivot", ".rotatePivot", absolute=True)
        mc.select(clear=True)
        om.MGlobal.displayInfo("## Zeroed pivot on all nodes!")
    elif sel:
        for obj in sel:
            mc.select(obj)
            mc.move(0, 0, 0, ".scalePivot", ".rotatePivot", absolute=True)
        om.MGlobal.displayInfo("## Zeroed pivot on selected node(s)!")
    else:
        mc.warning("No nodes have been selected!")


def ncsc_center_pivot(all=False):
    """Centers the pivot
    """

    sel = mc.ls(sl=True)

    if all is True:
        sel = mc.ls(geometry=True, transforms=True)
        for obj in sel:
            mc.select(obj)
            mc.CenterPivot()
        mc.select(clear=True)
        om.MGlobal.displayInfo("## Centered pivot on all nodes")
    elif sel:
        for obj in sel:
            mc.select(obj)
            mc.CenterPivot()
        om.MGlobal.displayInfo("## Centered pivot on selected node(s)")
    else:
        mc.warning("No nodes have been selected!")


def ncsc_zero_object(all=False):
    """Places the node in world 0, 0, 0
    """

    sel = mc.ls(sl=True)

    if all is True:
        sel = []
        mesh = mc.ls(exactType="mesh")
        for obj in mesh:
            rel = mc.listRelatives(obj, parent=True)
            sel.extend(rel)
            for obj in sel:
                mc.select(obj)
                ncsc_freeze_trans()
                obj_space = mc.xform(obj, q=True, ws=True, rp=True)
                offset = [x * -1 for x in obj_space]
                mc.xform(obj, ws=True, t=offset)
        mc.select(clear=True)
        om.MGlobal.displayInfo("## Zeroed all nodes!")
    elif sel:
        for obj in sel:
            ncsc_freeze_trans()
            obj_space = mc.xform(obj, q=True, ws=True, rp=True)
            offset = [x * -1 for x in obj_space]
            mc.xform(obj, ws=True, t=offset)
        om.MGlobal.displayInfo("## Zeroed out selected node(s)!")
    else:
        mc.warning("No nodes have been selected!")


def ncsc_move_above_zero(all=False):
    """Move geometry above -0.005
    """

    sel = mc.ls(sl=True)

    if all is True:
        sel = mc.ls(transforms=True, shapes=False)
        for obj in sel:
            if mc.objectType('pCylinder2') == "transform":
                mc.select(obj)
                bbox = mc.polyEvaluate(boundingBox=True)
                try:
                    y = str(bbox[1]).split(",")[0].replace("(", "")
                    clean_y = float(y.replace("-", ""))
                    if float(y) < 0:
                        cur_y = mc.getAttr(obj + '.ty')
                        new_y = float(clean_y) + float(cur_y)
                        print mc.move(new_y, y=True, ws=True, a=True)
                        #mc.setAttr(obj + '.ty', new_y)
                except:
                    pass
        mc.select(clear=True)
        om.MGlobal.displayInfo("## All nodes have been moved above Y: -0.005")
    elif sel:
        for obj in sel:
            bbox = mc.polyEvaluate(boundingBox=True)
            y = str(bbox[1]).split(",")[0].replace("(", "")
            clean_y = float(y.replace("-", ""))
            if float(y) < 0:
                cur_y = mc.getAttr(obj + '.ty')
                new_y = float(clean_y) + float(cur_y)
                print mc.move(new_y, y=True, ws=True, a=True)
                #mc.setAttr(obj + '.ty', new_y)
        mc.select(clear=True)
        om.MGlobal.displayInfo("## Selected node(s) have been moved above Y: -0.005")
    else:
        mc.warning("No nodes have been selected!")
