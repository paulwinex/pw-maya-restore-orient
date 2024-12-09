from itertools import chain
from typing import Union

import maya.api.OpenMaya as om
import maya.cmds as cmds
from pymel.core import *

class SelectionError(Exception):
    pass


world_axis_list = {
    'x': dt.Vector(1, 0, 0),
    'y': dt.Vector(0, 1, 0),
    'z': dt.Vector(0, 0, 1)
}

# MAYA GEOMETRY

def get_transform_node_from_selection():
    sel = selected()
    if not sel:
        raise SelectionError('Nothing selected')
    sel = sel[0]
    if isinstance(sel, nt.Transform):
        return sel
    if isinstance(sel, (MeshFace, MeshEdge, MeshVertex)):
        return sel.node().getTransform()
    raise SelectionError('Unsupported selection')

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


def get_lowest_y_coord_for_list(objects) -> float:
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


def get_lowes_y_pos(*objects: str) -> float:
    if not objects:
        raise ValueError('Empty list')
    shapes = list(*chain(cmds.listRelatives(x, allDescendents=True, type='mesh') for x in objects))
    if not shapes:
        raise ValueError('No mesh objects found')
    return get_lowest_y_coord_for_list(shapes)


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
    max_x = min_x = max_y = min_y = max_z = min_z = None
    for point in iter_object_points(obj):
        max_x = max((max_x, point.x)) if max_x is not None else point.x
        max_y = max((max_y, point.y)) if max_y is not None else point.y
        max_z = max((max_z, point.z)) if max_z is not None else point.z
        min_x = min((min_x, point.x)) if min_x is not None else point.x
        min_y = min((min_y, point.y)) if min_y is not None else point.y
        min_z = min((min_z, point.z)) if min_z is not None else point.z
    assert all( isinstance(x, float) for x in (max_x, max_y, max_z, min_x, min_y, min_z)), 'Empty object'
    return dt.Vector(tuple((om.MVector(max_x, max_y, max_z) + om.MVector(min_x, min_y, min_z)) / 2))


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


def get_object_vertex_count(obj):
    return sum([polyEvaluate(s, v=True) for s in iter_shapes(obj)])


def get_center_point_from_selection():
    sel = selected(fl=1)
    max_x = min_x = max_y = min_y = max_z = min_z = None
    def use_point(pt):
        nonlocal max_x, min_x, max_y, min_y, max_z, min_z
        max_x = max(max_x, pt.x) if max_x is not None else pt.x
        min_x = min(min_x, pt.x) if min_x is not None else pt.x
        max_y = max(max_y, pt.y) if max_y is not None else pt.y
        min_y = min(min_y, pt.y) if min_y is not None else pt.y
        max_z = max(max_z, pt.z) if max_z is not None else pt.z
        min_z = min(min_z, pt.z) if min_z is not None else pt.z
    if not sel:
        return
    for item in sel:
        if isinstance(item, MeshVertex):
            use_point(item.getPosition('world'))
        elif isinstance(item, MeshFace):
            for pt in item.getPoints('world'):
                use_point(pt)
        elif isinstance(item, MeshEdge):
            pt1, pt2 = item.connectedVertices()
            use_point(pt1.getPosition('world'))
            use_point(pt2.getPosition('world'))
        elif isinstance(item, nt.Transform):
            use_point(item.getBoundingBox().max())
            use_point(item.getBoundingBox().min())
        elif isinstance(item, nt.Mesh):
            for pt in iter_object_points(str(item)):
                use_point(pt)
    if any(val is None for val in (max_x, min_x, max_y, min_y, max_z, min_z)):
        return None
    average_x = (max_x + min_x) / 2
    average_y = (max_y + min_y) / 2
    average_z = (max_z + min_z) / 2
    return dt.Vector(average_x, average_y, average_z)


# CONVERT GEO TO...


def get_1axis_from_selection():
    sel = selected(fl=1)
    if not sel:
        raise SelectionError('Nothing is selected')
    if len(sel) == 1:
        if isinstance(sel[0], MeshFace):
            return sel[0].getNormal('world').normal()
        elif isinstance(sel[0], MeshVertex):
            return sel[0].getNormal('world').normal()
        elif isinstance(sel[0], MeshEdge):
            pt1, pt2 = sel[0].connectedVertices()
            return (pt1.getPosition('world') - pt2.getPosition('world')).normal()
    elif len(sel) == 2:
        if all(isinstance(x, MeshVertex) for x in sel):
            return (sel[1].getPosition('world') - sel[0].getPosition('world')).normal()
    if all(isinstance(x, MeshEdge) for x in sel):
        normals = []
        for edge in sel:
            pt11, pt12 = edge.connectedVertices()
            normals.append((pt11.getPosition('world') - pt12.getPosition('world')).normal())
        average_axis = sum(normals) / len(normals)
        return average_axis.normal()
    raise SelectionError('Wrong selection')


def get_3axis_from_selection():
    sel = selected(fl=1)
    if not sel:
        raise SelectionError('Nothing is selected')
    if len(sel) == 1:
        if isinstance(sel[0], MeshEdge):
            print('From 1 Edge')
            return get_3axis_from_edge(sel[0])
        elif isinstance(sel[0], MeshVertex):
            print('From 1 Point')
            return get_3axis_from_1_point(sel[0])
        elif isinstance(sel[0], MeshFace):
            print('From Face')
            return get_3axis_from_face(sel[0])
    elif len(sel) == 2:
        if all([isinstance(x, MeshVertex) for x in sel]):
            print('From 2 points')
            return get_3axis_from_2_points(*sel)
        elif all([isinstance(x, MeshEdge) for x in sel]):
            print('From 2 edges')
            return get_3axis_from_2_edge(*sel)
        elif isinstance(sel[0], MeshVertex) and isinstance(sel[1], MeshEdge):
            print('From 1 Point and 1 Edge [1]')
            return get_3axis_from_1_point_and_1_edge(sel[0], sel[1])
        elif isinstance(sel[1], MeshVertex) and isinstance(sel[0], MeshEdge):
            print('From 1 Point and 1 Edge [2]')
            return get_3axis_from_1_point_and_1_edge(sel[1], sel[0])
        elif all(isinstance(x, MeshFace) for x in sel):
            print('From 2 Faces')
            return get_3axis_from_multiple_faces(sel)
    elif len(sel) == 3:
        if all([isinstance(x, MeshVertex) for x in sel]):
            print('From 3 Points')
            return get_3axis_from_3_points(*sel)
    elif len(sel) == 4:
        if all([isinstance(x, MeshVertex) for x in sel]):
            return get_3axis_from_4_points(*sel)
    elif all(isinstance(x, MeshFace) for x in sel):
        print('By Multiply faces')
        return get_3axis_from_multiple_faces(sel)
    elif all(isinstance(x, MeshEdge) for x in sel):
        print('By Multiply edges')
        return get_3axis_from_multiple_edges(sel)
    raise SelectionError('Wrong selection')


def get_3axis_from_edge(edge: MeshEdge):
    pt1, pt2 = edge.connectedVertices()
    x = (pt1.getPosition('world') - pt2.getPosition('world')).normal()
    f1, f2 = ls(edge.connectedFaces(), fl=1)
    y = ((f1.getNormal('world') + f1.getNormal('world')) / 2).normal()
    z = x.cross(y)
    return fix_basis(x.normal(), y.normal(), z.normal())


def get_3axis_from_1_point(pt: dt.Point):
    y = pt.getNormal('world').normal()
    longest_edge = max([(edge.getLength('world'), edge) for edge in pt.connectedEdges()])[1]
    pt2 = [x for x in longest_edge.connectedVertices() if not x == pt][0]
    x = (pt.getPosition('world') - pt2.getPosition('world')).normal()
    z = x.cross(y)
    return fix_basis(x.normal(), y.normal(), z.normal())


def get_3axis_from_face(face: MeshFace):
    edges = [face.node().e[x] for x in face.getEdges()]
    len_edge_map = {round(x.getLength('world'), 3): x for x in edges}
    if len(set(len_edge_map.keys())) == 1:
        base_edge = sorted(len_edge_map.values(), key=lambda e: e.index())[0]
    else:
        base_edge = max(len_edge_map.items())[1]
    pt1, pt2 = sorted(base_edge.connectedVertices())
    x = (pt2.getPosition('world') - pt1.getPosition('world')).normal()
    y = face.getNormal('world').normal()
    z = x.cross(y)
    return fix_basis(x, y, z)


def get_3axis_from_multiple_faces(faces: list[MeshFace]) -> tuple[dt.Vector, ...]:
    assert len(faces) >= 2
    y: dt.Vector = sum([face.getNormal('world').normal() for face in faces]) / len(faces)
    if y.length() > 0.2:
        x = y.cross(dt.Vector(1, 0, 0))
        z = x.cross(y)
        return fix_basis(x, y, z)
    else:
        # probably is circle loop?
        print('Circular loop')
        x = faces[0].getNormal('world').normal()
        next_index = len(faces)//4 if len(faces) > 3 else [-1]
        z = faces[next_index].getNormal('world').normal()
        y = z.cross(x)
        x = z.cross(y)
        return fix_basis(x, y, z)


def get_3axis_from_multiple_edges(edges: list[MeshEdge]) -> tuple[dt.Vector, ...]:
    assert len(edges) > 2
    normals = []
    if is_edge_loop_closed(edges):
        print('For edge loop')
        points = [edge.connectedVertices()[0].getPosition('world') for edge in edges]
        center = sum(points) / len(points)
        x = (points[0] - center).normal()
        second_point_index = len(points)//4 if len(points) > 3 else len(points)//4
        z = (points[second_point_index] - center).normal()
        y  = z.cross(x)
        x = z.cross(y)
        return fix_basis(x, y, z)
    else:
        print('For edge chain')
        for edge in edges:
            pt1, pt2 = edge.connectedVertices()
            normals.append(pt1.getNormal('world') + pt2.getNormal('world'))
        average_normal: dt.Vector = sum(normals) / len(normals)
        z = average_normal.normal()
        _x, _y, y = get_3axis_from_edge(edges[0])
        x = z.cross(_x)
        y = x.cross(z)
        return fix_basis(x.normal(), z.normal(), y.normal())


def get_3axis_from_2_points(pt1: dt.Point, pt2: dt.Point) -> tuple[dt.Vector, ...]:
    x = (pt1.getPosition('world') - pt2.getPosition('world'))
    y = ((pt1.getNormal('world') + pt2.getNormal('world')) / 2)
    z = x.cross(y)
    return fix_basis(x.normal(), y.normal(), z.normal())


def get_3axis_from_2_edge(e1: MeshEdge, e2: MeshEdge) -> tuple[dt.Vector, ...]:
    pt11, pt12 = e1.connectedVertices()
    pt21, pt22 = e2.connectedVertices()
    return get_3axis_from_4_points(pt11, pt12, pt21, pt22)


def get_3axis_from_1_point_and_1_edge(pt: dt.Point, edge: MeshEdge) -> tuple[dt.Vector, ...]:
    pt1, pt2 = edge.connectedVertices()
    a, b = pt1.getPosition('world'), pt2.getPosition('world')
    x = (a - b).normal()
    p = pt.getPosition('world')
    p2 = b + x * x.dot(p - b)
    z = (p2 - p).normal()
    y = x.cross(z)
    aver_nrm = sum([pt.getNormal('world') for pt in (pt, pt1, pt2)])
    if aver_nrm.dot(y) < 0:
        y *= -1
    return fix_basis(x, y, z)


def get_3axis_from_3_points(pt1: dt.Point, pt2: dt.Point, pt3: dt.Point) -> tuple[dt.Vector, ...]:
    p1, p2, p3 = pt1.getPosition('world'), pt2.getPosition('world'), pt3.getPosition('world')
    d1 = [(p1 - p2).normal().dot((p1 - p3).normal()), p1]
    d2 = [(p2 - p1).normal().dot((p2 - p3).normal()), p2]
    d3 = [(p3 - p1).normal().dot((p3 - p2).normal()), p3]
    fp1 = min([d1, d2, d3])[1]
    fp2, fp3 = [x for x in (p1, p2, p3) if x != fp1]
    other_points = [((fp1 - fp2).length(), fp2), ((fp1 - fp3).length(), fp3)]
    short, long = [x[1] for x in sorted(other_points)]
    aver_nrm = sum([pt.getNormal('world') for pt in (pt1, pt2, pt3)])
    x = (long - dt.Vector(fp1)).normal()
    y = x.cross((fp1 - short).normal())
    if y.dot(aver_nrm.normal()) < 0:
        y *= -1
    z = x.cross(y)
    return fix_basis(x, y, z)


def get_3axis_from_4_points(pt11: dt.Point, pt12: dt.Point, pt21: dt.Point, pt22: dt.Point) -> tuple[dt.Vector, ...]:
    v1 = (pt11.getPosition('world') - pt12.getPosition('world')).normal()
    v2 = (pt21.getPosition('world') - pt22.getPosition('world')).normal()
    d = v1.dot(v2)
    if d < 0:
        v2 = (pt22.getPosition('world') - pt21.getPosition('world')).normal()
    if abs(d) > 0.5:
        v2 = (pt11.getPosition('world') - pt21.getPosition('world')).normal()
    x = v1.normal()
    aver_nrm = sum([pt.getNormal('world') for pt in (pt11, pt12, pt21, pt22)])
    y = x.cross(v2.normal()).normal()
    if y.dot(aver_nrm) < 0:
        y *= -1
    z = x.cross(y)
    return fix_basis(x, y, z)


def faces_to_basis(faces) -> tuple[dt.Vector, ...]:
    y: dt.Vector = sum([face.getNormal('world') for face in faces]) / len(faces)
    x: dt.Vector = y.cross(dt.Vector(1, 0, 0))
    z: dt.Vector = x.cross(y)
    return fix_basis(x, y, z)

# Geo Operations

def rotate_to_world_axis(src_axis: dt.Vector, world_axis: str, reverse_axis: bool = False):
    if not src_axis:
        return
    target_axis = world_axis_list[world_axis]
    print_vectors(src_axis)
    rotation_axis = src_axis.cross(target_axis)
    print_vectors(rotation_axis)
    if rotation_axis.length() < 0.1:
        for a in world_axis_list.values():
            if abs(a.dot(src_axis)) < 0.1:
                continue
            rotation_axis = abs(a)#.cross(src_axis)
            break
        else:
            print('Error rotate axis')
    print_vectors(rotation_axis)
    if rotation_axis.length() < 0.1:
        raise Exception('Error rotate axis')
    if reverse_axis:
        target_axis = -target_axis
    print_vectors(target_axis)
    print_vectors(rotation_axis)
    # if src_axis * target_axis < 0:
    #     print('REVERSE 2')
    #     target_axis = -target_axis
    angle = src_axis.angle(target_axis)
    print_vectors(rotation_axis)
    quaternion = dt.Quaternion(angle, rotation_axis)
    rotation_matrix = dt.TransformationMatrix()
    rotation_matrix.addRotationQuaternion(*list(quaternion), dt.Space.kWorld)
    return rotation_matrix


def _rotate_to_world_plane(src_axis: dt.Vector, obj, world_axis1: str, world_axis2: str, rotation_axis: dt.Vector = None):
    obj = PyNode(obj)
    world_axis_list = {
        'x': dt.Vector(1, 0, 0),
        'y': dt.Vector(0, 1, 0),
        'z': dt.Vector(0, 0, 1)
    }
    axis1 = world_axis_list[world_axis1]
    axis2 = world_axis_list[world_axis2]
    plane_normal = axis1.cross(axis2)
    projection = src_axis - (src_axis.dot(plane_normal) / plane_normal.dot(plane_normal)) * plane_normal
    projection.normalize()
    target_axis = projection
    if src_axis.dot(target_axis) < 0:
        target_axis = -target_axis
    angle = src_axis.angle(target_axis)
    rotation_axis = rotation_axis or src_axis.cross(target_axis)
    quaternion = dt.Quaternion(angle, rotation_axis)
    rotation_matrix = dt.TransformationMatrix()
    rotation_matrix.addRotationQuaternion(*list(quaternion), dt.Space.kWorld)
    curr_matrix = obj.getMatrix()
    new_matrix = curr_matrix * rotation_matrix
    obj.setMatrix(new_matrix, worldSpace=True)


def rotate_to_world_plane(src_axis: dt.Vector, obj,
                          world_axis1: str, world_axis2: str,
                          rotation_axis: str = None):
    print(f'Rotate to plane {world_axis1}{world_axis2} by {rotation_axis if rotation_axis else "closest"}')
    obj = PyNode(obj)
    world_axis_list = {
        'x': dt.Vector(1, 0, 0),
        'y': dt.Vector(0, 1, 0),
        'z': dt.Vector(0, 0, 1)
    }
    axis1 = world_axis_list[world_axis1]
    axis2 = world_axis_list[world_axis2]

    if rotation_axis:
        rotation_axis = world_axis_list.get(rotation_axis)
    plane_normal = axis1.cross(axis2)
    plane_normal.normalize()
    projection = src_axis - (src_axis.dot(plane_normal) / plane_normal.dot(plane_normal)) * plane_normal
    projection.normalize()
    target_axis = projection
    if src_axis.dot(target_axis) < 0:
        target_axis = -target_axis

    if rotation_axis:
        rotation_axis.normalize()
        proj_src = src_axis - (src_axis.dot(rotation_axis) / rotation_axis.dot(rotation_axis)) * rotation_axis
        proj_target = target_axis - (target_axis.dot(rotation_axis) / rotation_axis.dot(rotation_axis)) * rotation_axis
        proj_src.normalize()
        proj_target.normalize()
        angle = proj_src.angle(proj_target)
        cross_product = proj_src.cross(proj_target)
        if cross_product.dot(rotation_axis) < 0:
            angle = -angle
    else:
        rotation_axis = src_axis.cross(target_axis)
        rotation_axis.normalize()
        angle = src_axis.angle(target_axis)
    quaternion = dt.Quaternion(angle, rotation_axis)
    rotation_matrix = dt.TransformationMatrix()
    rotation_matrix.addRotationQuaternion(*list(quaternion), dt.Space.kWorld)
    rotate_object_to_matrix(obj,  rotation_matrix)
    # curr_matrix = obj.getMatrix()
    # new_matrix = curr_matrix * rotation_matrix
    # obj.setMatrix(new_matrix, worldSpace=True)


def is_edge_loop_closed(edges):
    if not edges:
        return False
    vertex_to_edges = {}
    for edge in edges:
        vertices = edge.connectedVertices()
        for vertex in vertices:
            vertex_index = vertex.index()
            if vertex_index not in vertex_to_edges:
                vertex_to_edges[vertex_index] = []
            vertex_to_edges[vertex_index].append(edge)
    start_vertex_index = next(iter(vertex_to_edges))
    current_vertex_index = start_vertex_index
    visited_edges = set()

    while True:
        connected_edges = vertex_to_edges[current_vertex_index]
        if not connected_edges:
            return False
        next_edge = None
        for edge in connected_edges:
            if edge.index() not in visited_edges:
                next_edge = edge
                break
        if next_edge is None:
            return current_vertex_index == start_vertex_index
        visited_edges.add(next_edge.index())
        vertices = next_edge.connectedVertices()
        next_vertex_index = vertices[0].index() if vertices[0].index() != current_vertex_index else vertices[1].index()
        current_vertex_index = next_vertex_index
    return False


def rotate_object_to_matrix(obj: nt.Transform, mx: dt.TransformationMatrix):
    curr_matrix = obj.getMatrix()
    obj.setMatrix(curr_matrix * mx, worldSpace=True)

# TRIGONOMETRY


def vector_list_to_basis(p1: dt.Point, p2: dt.Point, p3: dt.Point) -> tuple[dt.Vector, ...]:
    x = (p1 - p2).normal()
    y = x.cross((p3 - p2).normal())
    z = x.cross(y).normal()
    return fix_basis(x, y, z)


def fix_basis(x: dt.Vector, y: dt.Vector, z: dt.Vector) -> tuple[dt.Vector, ...]:
    x = x.normal()
    y = y.normal()
    z = z.normal()
    if x.cross(y).dot(z) < 0:
        z *= -1
    return x, y, z


def basis_to_transformation_matrix(x: dt.Vector, y: dt.Vector, z: dt.Vector, pos=None) -> dt.TransformationMatrix:
    mx = dt.TransformationMatrix(x.x, x.y, x.z, 0,
                                 y.x, y.y, y.z, 0,
                                 z.x, z.y, z.z, 0)
    if pos:
        mx.setTranslation(tuple(pos), 'world')
    return mx


def transformation_matrix_to_basis(mx: dt.Matrix) -> tuple[dt.Vector, ...]:
    return (dt.Vector(mx[0][0], mx[0][1], mx[0][2]),
            dt.Vector(mx[1][0], mx[1][1], mx[1][2]),
            dt.Vector(mx[2][0], mx[2][1], mx[2][2])
            )


def get_rotation_matrix(axis: str, degree: float, center=None) -> dt.TransformationMatrix:
    """
    Return rotation matrix by axis and degree
    """
    euler_rotate = [0, 0, 0]
    index = dict(x=0, y=1, z=2)[axis.lower().strip('-')]
    euler_rotate[index] += degree * (-1 if '-' in axis else 1)
    m = dt.TransformationMatrix()
    m.setRotatePivot(tuple(center), 'object', True)
    m.setRotation(euler_rotate)
    return m


def closest_axis(vector: dt.Vector, axis_name=False) -> Union[dt.Vector, str]:
    # world_axis = {
    #     'x': dt.Vector([1, 0, 0]),
    #     'y': dt.Vector([0, 1, 0]),
    #     'z': dt.Vector([0, 0, 1]),
    #     '-x': dt.Vector([-1, 0, 0]),
    #     '-y': dt.Vector([0, -1, 0]),
    #     '-z': dt.Vector([0, 0, -1])
    # }
    world_axis = {**world_axis_list, **{f'-{k}': v*-1 for k, v in world_axis_list.items()}}

    closest_axis_key = None
    max_cosine = -1

    for axis_key, axis_vector in world_axis.items():
        cosine = vector * axis_vector
        if cosine > max_cosine:
            max_cosine = cosine
            closest_axis_key = axis_key

    if axis_name:
        return closest_axis_key
    else:
        return world_axis[closest_axis_key]


def align_up_to(x: dt.Vector, y: dt.Vector, z: dt.Vector, to_axis: str) -> tuple[dt.Vector, ...]:
    c = dt.Vector()
    if to_axis == 'x':
        rm = get_rotation_matrix('z', -90, c)
    elif to_axis == '-x':
        rm = get_rotation_matrix('z', 90, c)
    elif to_axis == 'y':
        return x, y, z
    elif to_axis == '-y':
        rm = get_rotation_matrix('z', 180, c)
    elif to_axis == 'z':
        rm = get_rotation_matrix('x', 90, c)
    elif to_axis == '-z':
        rm = get_rotation_matrix('x', -90, c)
    else:
        raise Exception(f'Invalid axis {to_axis}')
    mx = basis_to_transformation_matrix(x, y, z, c)
    r_mx = rm * mx
    return transformation_matrix_to_basis(r_mx)


def closest_world_axis_matrix(x: dt.Vector, y: dt.Vector, z: dt.Vector) -> dt.TransformationMatrix:
    """
    Rotate the given basis vectors (x, y, z) to align with the closest world axes.
    If axis_name is provided, the y vector will be aligned with the specified axis.
    """
    closest_x = closest_axis(x.normal()).normal()
    closest_y = closest_axis(y.normal()).normal()
    closest_z = closest_y.cross(closest_x.normal()).normal()
    return basis_to_transformation_matrix(fix_basis(closest_x, closest_y, closest_z))


def rotation_matrix_to_closest_world_axis(x: dt.Vector, y: dt.Vector, z: dt.Vector) -> dt.TransformationMatrix:
    """
    Rotate the given basis vectors (x, y, z) to align with the closest world axes.
    If axis_name is provided, the y vector will be aligned with the specified axis.
    """
    closest_x = closest_axis(x.normal()).normal()
    closest_y = closest_axis(y.normal()).normal()
    closest_z = closest_y.cross(closest_x.normal()).normal()
    src_matrix = basis_to_transformation_matrix(*fix_basis(x, y, z))
    target_matrix = basis_to_transformation_matrix(*fix_basis(closest_x, closest_y, closest_z))
    rotation_matrix = src_matrix.asMatrixInverse() * target_matrix
    return rotation_matrix


def rotation_matrix_to_axis(x, y, z, axis_to_rotate: str, reverse_axis: bool = False, align_x: bool = None)-> dt.TransformationMatrix:
    """
    Rotate Y axis from basis to specified world axis (x, y, z, -x, -y, -z)
    1. Get world axis by name
    2. Get rotation matrix to selected axis
    3. Rotate X axis to next world axis
    """
    x, y, z = fix_basis(x, y ,z)
    if reverse_axis:
        axis_to_rotate = reversed_axis_name(axis_to_rotate)
    target_y = get_world_axis_by_name(axis_to_rotate).normal()
    target_z = target_y.cross(x.normal())
    if target_z.length() < 0.1:
        target_z = target_y.cross(y.normal())
    target_x = target_z.cross(target_y)
    target_basis = fix_basis(target_x, target_y, target_z)  # fix z direction
    rotation_matrix = rotation_matrix_between_basis(x, y, z, *target_basis)
    # if align_x:
        # TODO
        # new_basis = transformation_matrix_to_basis(rotation_matrix)
        # next_axis = get_next_axis_name(axis_to_rotate)
        # new_mx = rotation_matrix_to_axis(*new_basis, axis_to_rotate=main_axis, reverse_axis=reverse_axis)
        # x = get_world_axis_by_name(align_x_to).normal()
        # rotation_matrix = rotation_matrix_between_basis(x, y, z, *target_basis)
    return  rotation_matrix



def rotation_matrix_between_basis(x1, y1, z1, x2, y2, z2):
    """
    Compute the rotation matrix that transforms the basis (x1, y1, z1) to (x2, y2, z2).
    """
    mx1 = basis_to_transformation_matrix(x1, y1, z1)
    mx2 = basis_to_transformation_matrix(x2, y2, z2)
    rotation_matrix = mx2.asMatrixInverse() * mx1
    return rotation_matrix


def get_world_axis_by_name(name: str) -> dt.Vector:
    world_axis = dict(
        x=dt.Vector([1, 0, 0]),
        y=dt.Vector([0, 1, 0]),
        z=dt.Vector([0, 0, 1])
    )
    axis = world_axis[name.strip('-')]
    if '-' in name:
        axis *= -1
    return axis


def reversed_axis_name(axis_name: str):
    if '-' in axis_name:
        return axis_name.replace('-', '')
    else:
        return '-' + axis_name


def get_next_axis_name(axis_name):
    return (['x', 'y', 'z', 'x'].index(axis_name.lower().strip('-')) + 1) % 3


def print_vectors(*vectors: list):
    for vec in vectors:
        print(*[f'{round(val, 2):>5}' for val in vec])
