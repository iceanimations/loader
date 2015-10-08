import pymel.core as pc
import re
from collections import OrderedDict

object_mattes = {}
object_mattes['ID_MOS']=(1,2,3)        #mansour, obaid, salem
object_mattes['ID_NNS']=(4,5,6)
object_mattes['ID_MKS']=(7,8,9)
object_mattes['ID_STB']=(10,11,12)
object_mattes['ID_HPP']=(13,14,15)

material_mattes = {}
material_mattes['ID_FHE']=(1,2,3)
material_mattes['ID_THT']=(4,5,6)
material_mattes['ID_CTS']=(7,8,9)
material_mattes['ID_Cornea']=(10,11,12)


object_mattesDD = {}
object_mattesDD['ID_CDB']=(1,2,3)        #mansour, obaid, salem
object_mattesDD['ID_SFM']=(4,5,6)
object_mattesDD['ID_VMM']=(7,8,9)
object_mattesDD['ID_MAM']=(10,11,12)
object_mattesDD['ID_MMM']=(13,14,15)
object_mattesDD['ID_SRE']=(16,17,18)

material_mattesDD = {}
material_mattesDD['ID_BFO']=(1,2,3)
material_mattesDD['ID_TIT']=(4,5,6)
material_mattesDD['ID_EYE']=(7,8,9)


requiredTypes = [
    'Ambient Occlusion',
    'Depth',
    'Diffuse Filter',
    'Diffuse Lighting',
    'Global Illumination',
    'Reflections',
    'Refractions',
    'Specular Lighting',
    'Sub Surface Scatter']

def redshiftAOVExists(name):
    for node in pc.ls(type='RedshiftAOV'):
        if (node.name().split(":")[-1] == name or
                (pc.attributeQuery('name', n=node, exists=True)
                    and node.attr('name').get() == name)):
            return True
    return False

def redshiftUpdateActiveAovList():
    try:
        if not pc.about(batch=True):
            pc.mel.redshiftUpdateActiveAovList()
    except:
        pass


def addPasses(*args):
    existingTypes = [node.aovType.get() for node in pc.ls(type='RedshiftAOV')]
    passTypes = [typ for typ in requiredTypes if typ not in existingTypes]
    map(lambda x: pc.rsCreateAov(type=x), passTypes)
    try:
        if not pc.about(batch=True):
            pc.mel.redshiftUpdateActiveAovList()
    except:
        pass


def addMaterialIDs(*args):
    for name, ids in material_mattes.items():
        if redshiftAOVExists(name):
            pc.warning('%s already Exists'%name)
            continue
        node = pc.PyNode(pc.rsCreateAov(type='Puzzle Matte'))
        node.rename(name)
        if pc.attributeQuery('name', n=node, exists=True):
            node.attr('name').set(name)
        node.mode.set(0)
        node.redId.set(ids[0])
        node.greenId.set(ids[1])
        node.blueId.set(ids[2])

    redshiftUpdateActiveAovList()


def addObjectIDs(*argsobject_mattes):
    for name, ids in object_mattes.items():
        if redshiftAOVExists(name):
            pc.warning('%s already Exists'%name)
            continue
        node = pc.PyNode(pc.rsCreateAov(type='Puzzle Matte'))
        node.rename(name)
        if pc.attributeQuery('name', n=node, exists=True):
            node.attr('name').set(name)
        node.mode.set(1)
        node.redId.set(ids[0])
        node.greenId.set(ids[1])
        node.blueId.set(ids[2])

    redshiftUpdateActiveAovList()


def addObjectIDsFromSelection(*args):
    selectedNodes = pc.ls(sl=True, type='transform')
    maxid = 0
    objid_names = OrderedDict()
    for node in selectedNodes:
        node = pc.PyNode(node)
        try:
            name = node.namespaceList()[0]
        except:
            name = node.name().split('|')[-1]
        name = name.split(':')[0].split('_')[0]
        shapes = node.getShapes(type='mesh')
        if shapes:
            try:
                maxid = max([shape.rsObjectId.get() for shape in shapes])
            except ValueError:
                continue
        else:
            continue
        if maxid:
            objid_names[maxid] = name

    current_matte = None
    matte_name = 'ID'
    for idx, objId in enumerate(objid_names.keys()):
        if idx % 3 == 0:
            current_matte = pc.PyNode(pc.rsCreateAov(type='Puzzle Matte'))
            current_matte.redId.set(objId)
            matte_name = 'ID'
        elif idx % 3 == 1:
            current_matte.greenId.set(objId)
        else:
            current_matte.blueId.set(objId)

        matte_name += '_' + objid_names[objId]
        current_matte.rename(matte_name)
        if pc.attributeQuery('name', n=node, exists=True):
            current_matte.attr('name').set(matte_name)

    redshiftUpdateActiveAovList()

def correctObjectID(*args):
    for tr in pc.ls(type='transform', sl=1):
        shapes = tr.getShapes(type='mesh')
        maxid = max([shape.rsObjectId.get() for shape in shapes])
        for shape in shapes:
            shape.rsObjectId.set(maxid)

def fixAOVPrefixes(*args):

    prefixString='<Camera>\<RenderLayer>\<RenderLayer>_<AOV>\<RenderLayer>_<AOV>_'

    for node in pc.ls(type='RedshiftAOV'):
        name = node.name().split('|')[-1].split(':')[-1]
        if name.startswith('rsAov_'):
            name = name[6:]
        if pc.attributeQuery('name', n=node, exists=True):
            node.attr('name').set(name)
        ps = re.compile('<AOV>', re.I).sub(name, prefixString)
        node.filePrefix.set(ps)
        node.exrCompression.set(3)
        
def addMaterialIDs_DingDong(*args):
    for name, ids in material_mattesDD.items():
        if redshiftAOVExists(name):
            pc.warning('%s already Exists'%name)
            continue
        node = pc.PyNode(pc.rsCreateAov(type='Puzzle Matte'))
        node.rename(name)
        if pc.attributeQuery('name', n=node, exists=True):
            node.attr('name').set(name)
        node.mode.set(0)
        node.redId.set(ids[0])
        node.greenId.set(ids[1])
        node.blueId.set(ids[2])

    redshiftUpdateActiveAovList()
    
def addObjectIDs_DingDong(*argsobject_mattes):
    for name, ids in object_mattesDD.items():
        if redshiftAOVExists(name):
            pc.warning('%s already Exists'%name)
            continue
        node = pc.PyNode(pc.rsCreateAov(type='Puzzle Matte'))
        node.rename(name)
        if pc.attributeQuery('name', n=node, exists=True):
            node.attr('name').set(name)
        node.mode.set(1)
        node.redId.set(ids[0])
        node.greenId.set(ids[1])
        node.blueId.set(ids[2])

    redshiftUpdateActiveAovList()


def rsAOVToolShow():
    winname = 'rsAOVToolsUI'
    if pc.window(winname, exists=True):
        pc.deleteUI(winname)

    with pc.window(winname, w=200) as win:
        with pc.columnLayout(w=200):
            for func in [addPasses, addMaterialIDs, addObjectIDs,
                    correctObjectID, addObjectIDsFromSelection,
                    fixAOVPrefixes, addMaterialIDs_DingDong,
                    addObjectIDs_DingDong]:
                pc.button(label=func.func_name, c=func, w=200)
    win.show()


if __name__ == '__main__':
    rsAOVToolShow()
