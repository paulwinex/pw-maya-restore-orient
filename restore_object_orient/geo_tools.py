from itertools import chain
import maya.api.OpenMaya as om
import maya.cmds as cmds


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


def get_object_center(obj):
    total_points = om.MFloatPointArray()
    vertex_count = 0

    # Создаем MSelectionList один раз
    selectionList = om.MSelectionList()
    shapes = cmds.listRelatives(obj, allDescendents=True, type='mesh')
    for shape in shapes:
        selectionList.add(shape)

    # Итерируем по всем объектам в MSelectionList
    for i in range(selectionList.length()):
        dagPath = selectionList.getDagPath(i)
        mesh = om.MFnMesh(dagPath)

        points = mesh.getPoints(om.MSpace.kWorld)
        for point in points:
            total_points.append(point)
        vertex_count += len(points)

    if vertex_count == 0:
        return om.MVector(0, 0, 0)

    center_sum = om.MVector(0, 0, 0)
    for point in total_points:
        center_sum += om.MVector(point)

    center_vector = center_sum / vertex_count
    return center_vector
