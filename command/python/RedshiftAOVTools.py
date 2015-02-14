import pymel.core as pc
import re

def addPasses(*args):
    types = [
        'Ambient Occlusion',
        'Depth',
        'Diffuse Filter',
        'Diffuse Lighting',
        'Global Illumination',
        'Reflections',
        'Refractions',
        'Specular Lighting',
        'Sub Surface Scatter']
    map(lambda x: pc.rsCreateAov(type=x), types)
    try:
        if not pc.about(batch=True):
            pc.mel.redshiftUpdateActiveAovList()
    except:
        pass


def addMaterialIDs(*args):

    mattes = {}
    mattes['ID_FHE']=(1,2,3)
    mattes['ID_THT']=(4,5,6)
    mattes['ID_CTS']=(7,8,9)

    for name, ids in mattes.items():
        if pc.objExists(name):
            pc.warning('%s already Exists'%name)
        node = pc.PyNode(pc.rsCreateAov(type='Puzzle Matte'))
        node.rename(name)
        node.mode.set(0)
        node.redId.set(ids[0])
        node.greenId.set(ids[1])
        node.blueId.set(ids[2])

    try:
        if not pc.about(batch=True):
            pc.mel.redshiftUpdateActiveAovList()
    except:
        pass


def addObjectIDs(*args):
    mattes = {}
    mattes['ID_MOS']=(1,2,3)
    mattes['ID_NNS']=(4,5,6)
    mattes['ID_MKS']=(7,8,9)
    mattes['ID_STB']=(10,11,12)
    mattes['ID_HPP']=(13,14,15)

    for name, ids in mattes.items():
        if pc.objExists(name):
            pc.warning('%s already Exists'%name)
        node = pc.PyNode(pc.rsCreateAov(type='Puzzle Matte'))
        node.rename(name)
        node.mode.set(1)
        node.redId.set(ids[0])
        node.greenId.set(ids[1])
        node.blueId.set(ids[2])

    try:
        if not pc.about(batch=True):
            pc.mel.redshiftUpdateActiveAovList()
    except:
        pass

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
        ps = re.compile('<AOV>', re.I).sub(name, prefixString)
        node.filePrefix.set(ps)


def rsAOVToolShow():
    winname = 'rsAOVToolsUI'
    if pc.window(winname, exists=True):
        pc.deleteUI(winname)

    with pc.window(winname, w=200) as win:
        with pc.columnLayout(w=200):
            for func in [addMaterialIDs, addObjectIDs, correctObjectID,
                    fixAOVPrefixes, addPasses]:
                pc.button(label=func.func_name, c=func, w=200)
    win.show()

if __name__ == '__main__':
    rsAOVToolShow()
