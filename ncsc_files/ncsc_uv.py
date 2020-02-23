""" scripts related to the UV module """

import os

try:
    import maya.cmds as mc
    import maya.mel as mel
except ImportError:
    pass


def ncsc_overlapping_uvs():
    sel = mc.ls(sl=True)
    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('textureWindowUpdatePopup( "polyTexturePlacementPanel1popupMenus", "polyTexturePlacementPanel1", "textureWindow");')
            mel.eval('changeSelectMode -component; setComponentPickMask "Facet" true; selectType -ocm -alc false; selectType -msh true; selectType -sf false -se false -suv false -cv false;')
            mel.eval('hilite {} ;'.format(obj))
            mel.eval('TextureViewWindow;')
            mel.eval('texturePanelShow;')
            mel.eval('selectUVOverlappingComponents 1 0')


def ncsc_inverted_uvs():
    sel = mc.ls(sl=True)
    for obj in sel:
        if mc.objExists(obj):
            mc.select(obj)
            mel.eval('textureWindowUpdatePopup( "polyTexturePlacementPanel1popupMenus", "polyTexturePlacementPanel1", "textureWindow");')
            mel.eval('changeSelectMode -component; setComponentPickMask "Facet" true; selectType -ocm -alc false; selectType -msh true; selectType -sf false -se false -suv false -cv false;')
            mel.eval('hilite {} ;'.format(obj))
            mel.eval('TextureViewWindow;')
            mel.eval('texturePanelShow;')
            mel.eval('selectUVFaceOrientationComponents {} 0 2 1')
