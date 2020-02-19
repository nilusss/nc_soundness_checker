""" scripts related to the Transform module """

import os

import ncsc_API as api

try:
    import maya.cmds as mc
    import maya.mel as mel
except ImportError:
    pass


def ncsc_freeze_trans():
    """Freeze transforms on the selected node
    """

    api.ncsc_get_meshes_from_sel()
    try:
        mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    except:
        mc.warning("No objects selected!")


def ncsc_place_top_node():
    """Selects all geometry in the scene and places it in a top node
    """

    sel = mc.ls(geometry=True)
    if not sel:
        mc.warning("You need to have geometry in your scene")
    elif mc.objExists("geo") or mc.objExists("*_grp"):
        mc.warning("You already have a \"geo\" node")
    else:
        filepath = mc.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        asset_name = filename.split("_")[0].split(".")[0]
        grp_node_name = asset_name + "_grp"
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


def ncsc_zero_pivot():
    """Places the node pivot in world 0, 0, 0
    """

    sel = mc.ls(sl=True)
    if sel:
        for sel in sel:
            temp_transform = mc.createNode("transform")  # Create a temporary transform at world origin.
            mc.matchTransform(sel, temp_transform, position=True)  # Align your object to the transform.
            mc.delete(temp_transform)  # Delete the transform.
    else:
        mc.warning("Please select a node to zero out!")


def ncsc_move_above_zero():
    """Move geometry above -0.005
    """

    sel = mc.ls(sl=True)

    for obj in sel:

        bbox = mc.polyEvaluate(boundingBox=True)

        y = str(bbox[1]).split(",")[0].replace("(", "")
        clean_y = float(y.replace("-", ""))
        if float(y) < 0:
            cur_y = mc.getAttr(obj + '.ty')
            new_y = float(clean_y) + float(cur_y)
            mc.setAttr(obj + '.ty', new_y)
        else:
            mc.warning("Object is not below 0 in world Y")


def ncsc_add_padding():
    pass
