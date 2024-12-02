from itertools import chain
import maya.api.OpenMaya as om
import maya.cmds as cmds
from pymel.core import *


def get_lowest_point_for_object(obj):
    selectionList = om.MSelectionList()
    selectionList.add(obj)
    dagPath = selectionList.getDagPath(0)
    mesh = om.MFnMesh(dagPath)
    points = mesh.getPoints(om.MSpace.kWorld)
    min_y = float('inf')
    for point in points:
        if point.y < min_y:
            min_y = point.y

    return min_y


def get_lowest_point_for_list(objects):
    min_y = float('inf')

    selectionList = om.MSelectionList()
    for obj in objects:
        selectionList.add(obj)

    for i in range(selectionList.length()):
        dagPath = selectionList.getDagPath(i)
        mesh = om.MFnMesh(dagPath)
        points = mesh.getPoints(om.MSpace.kWorld)

        for point in points:
            if point.y < min_y:
                min_y = point.y

    return min_y

def get_lowes_point(*objects: str):
    if not objects:
        raise ValueError('Empty list')
    shapes = list(*chain(cmds.listRelatives(x, allDescendents=True, type='mesh') for x in objects))
    if not shapes:
        raise ValueError('No mesh objects found')
    print('Compute objects count:', len(shapes))
    return get_lowest_point_for_list(shapes)


def iter_object_points(obj):
    selectionList = om.MSelectionList()
    shapes = cmds.listRelatives(obj, allDescendents=True, type='mesh')
    for shape in shapes:
        selectionList.add(shape)
    for i in range(selectionList.length()):
        dagPath = selectionList.getDagPath(i)
        mesh = om.MFnMesh(dagPath)

        points = mesh.getPoints(om.MSpace.kWorld)
        for point in points:
            yield point


def get_object_center(obj):
    obj = str(obj)
    max_x = min_x = max_y = min_y = max_z = min_z = 0
    for point in iter_object_points(obj):
        max_x = max((max_x, point.x))
        max_y = max((max_y, point.y))
        max_z = max((max_z, point.z))
        min_x = min((min_x, point.x))
        min_y = min((min_y, point.y))
        min_z = min((min_z, point.z))
    return (om.MVector(max_x, max_y, max_z) + om.MVector(min_x, min_y, min_z)) / 2


def get_selection_center():
    sel = selected()
    if not sel:
        return dt.Vector()
    pos_array = []
    for s in sel:
        if isinstance(s, MeshEdge):
            for p in s.connectedVertices():
                pos_array.append(p.getPosition('world'))
        elif isinstance(s, MeshFace):
            pos_array.extend([dt.Vector(x) for x in s.getPoints('world')])
        elif isinstance(s, MeshVertex):
            pos_array.append(s.getPosition('world'))
    pos = sum(pos_array, dt.Vector()) / len(pos_array)
    return pos



def iter_shapes(obj):
    shapes = obj.listRelatives(s=1, allDescendents=1)
    for s in shapes:
        yield s


def freeze_transformations(obj):
    with UndoChunk():
        for tr in obj.listRelatives(allDescendents=1, typ=nt.Transform):
            makeIdentity(tr, apply=True, t=1, r=1, s=1, n=0, pn=1)
            xform(tr, piv=[0, 0, 0], ws=True)
        makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0, pn=1)
        xform(obj, piv=[0, 0, 0], ws=True)


