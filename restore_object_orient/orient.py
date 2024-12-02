# coding=utf-8
from pymel.core import *
import traceback
from .utils import compute_time
from . import geo_tools

class SelectionError(Exception):
    pass


class ObjOrient(object):
    grp_name = 'axis'
    axes = dict(
        x=dt.Vector([1, 0, 0]),
        y=dt.Vector([0, 1, 0]),
        z=dt.Vector([0, 0, 1])
    )
    colors = dict(r=13, g=14, b=15)
    scene_center = dt.Vector([0, 0, 0])

    def __init__(self, obj):
        self.object = obj
        self.init_points = self.get_init_points()
        self.base_point = None
        self.freezed = False
        self.init_mx = self.object.getMatrix(worldSpace=True)

    def reset(self):
        self.object.setMatrix(self.init_mx)

    @compute_time
    def get_init_points(self):
        import random
        if self.object_vertex_count < 4:
            raise Exception('So few vertices!')
        points = []
        all_shapes = self.object.listRelatives(s=1, allDescendents=1)
        if len(all_shapes) >= 3:
            random_shapes = random.sample(all_shapes, 3)
        else:
            random_shapes = all_shapes*3

        for sh in random_shapes:
            vtx = sh.vtx[random.randint(0, polyEvaluate(sh, v=True))]
            points.append((vtx, vtx.getPosition('world')))
        return points

    def _vector_list_to_basis(self, p1, p2, p3):
        x = (p1 - p2).normal()
        y = x.cross((p3 - p2).normal())
        z = x.cross(y).normal()
        return x.normal(), y.normal(), z.normal()

    @compute_time
    def move_to_start_position(self):
        if not self.freezed:
            raise Exception('Source object is not freezed')
        pi1, pi2, pi3 = [x[1] for x in self.init_points]
        x1, y1, z1 = self._vector_list_to_basis(pi1, pi2, pi3)

        curr_points = [PyNode(name).getPosition('world') for name, init_pt in self.init_points]
        pr1, pr2, pr3 = curr_points
        x2, y2, z2 = self._vector_list_to_basis(pr1, pr2, pr3)

        m1 = self.basis_to_transformation_matrix(x1, y1, z1, pi2)
        m2 = self.basis_to_transformation_matrix(x2, y2, z2, pr2)

        self.object.setMatrix(m2.asMatrixInverse() * m1)

    @property
    def object_vertex_count(self):
        return sum([polyEvaluate(s, v=True) for s in geo_tools.iter_shapes(self.object)])

    @property
    def center(self):
        from restore_object_orient.geo_tools import get_object_center
        return get_object_center(str(self.object))

    # ====================================

    def get_axis_from_selection(self):
        sel = selected(fl=1)
        if not sel:
            raise SelectionError('Nothing is selected')
        if len(sel) == 1:
            if isinstance(sel[0], MeshEdge):
                # по одной оси, вторая дефолтная
                print('From 1 Edge')
                return self.get_3axis_from_edge(sel[0])
            elif isinstance(sel[0], MeshVertex):
                # по одной точке. Вторая в центре
                print('From 1 Point')
                return self.get_3axis_from_1_point(sel[0])
            elif isinstance(sel[0], MeshFace):
                # по фейсу
                print('From Face')
                return self.get_3axis_from_face(sel[0])
        elif len(sel) == 2:
            if all([isinstance(x, MeshVertex) for x in sel]):
                # по двум точкам
                print('From 2 points')
                return self.get_3axis_from_2_points(*sel)
            elif all([isinstance(x, MeshEdge) for x in sel]):
                # по двум ребрам
                print('From 2 edges')
                return self.get_3axis_from_2_edge(*sel)
            elif isinstance(sel[0], MeshVertex) and isinstance(sel[1], MeshEdge):
                # по ребру и точке
                print('From 1 Pint and 1 Edge [1]')
                return self.get_3axis_from_1_point_and_1_edge(sel[0], sel[1])
            elif isinstance(sel[1], MeshVertex) and isinstance(sel[0], MeshEdge):
                # тоже по ребру и точке но в другом порядке
                print('From 1 Pint and 1 Edge [2]')
                return self.get_3axis_from_1_point_and_1_edge(sel[1], sel[0])
            elif all(isinstance(x, MeshFace) for x in sel):
                # по двум фейсам
                print('From 2 Faces')
                return self.get_3axis_from_multiple_faces(sel)
        elif len(sel) == 3:
            if all([isinstance(x, MeshVertex) for x in sel]):
                # по 3 точкам
                print('From 3 Pints')
                return self.get_3axis_from_3_points(*sel)
        elif len(sel) == 4:
            if all([isinstance(x, MeshVertex) for x in sel]):
                return self.get_3axis_from_4_points(*sel)
        elif all(isinstance(x, MeshFace) for x in sel):
            print('By Multiply fases')
            return self.get_3axis_from_multiple_faces(sel)
        elif all(isinstance(x, MeshEdge) for x in sel):
            print('By Multiply edges')
            return self.get_3axis_from_multiple_edges(sel)
        raise SelectionError('Wrong selection')

    @compute_time
    def get_3axis_from_edge(self, edge):
        pt1, pt2 = edge.connectedVertices()
        x = (pt1.getPosition('world') - pt2.getPosition('world')).normal()
        f1, f2 = ls(edge.connectedFaces(), fl=1)
        y = ((f1.getNormal('world') + f1.getNormal('world')) / 2).normal()
        z = x.cross(y)
        return self.fix_basis(x.normal(), y.normal(), z.normal())

    @compute_time
    def get_3axis_from_1_point(self, pt):
        y = pt.getNormal('world').normal()
        longest_edge = max([(edge.getLength('world'), edge) for edge in pt.connectedEdges()])[1]
        pt2 = [x for x in longest_edge.connectedVertices() if not x == pt][0]
        x = (pt.getPosition('world') - pt2.getPosition('world')).normal()
        z = x.cross(y)
        return self.fix_basis(x.normal(), y.normal(), z.normal())

    @compute_time
    def get_3axis_from_face(self, face):
        edges = [face.node().e[x] for x in face.getEdges()]
        e_map = {x.getLength('world'): x for x in edges}
        biggest = max(e_map.items())[1]
        pt1, pt2 = biggest.connectedVertices()
        x = (pt1.getPosition('world') - pt2.getPosition('world')).normal()
        y = face.getNormal('world').normal()
        z = x.cross(y)
        return self.fix_basis(x, y, z)

    @compute_time
    def get_3axis_from_multiple_faces(self, faces):
        y = sum([face.getNormal('world') for face in faces]) / len(faces)
        x = y.cross(dt.Vector(1,0,0))
        z = x.cross(y)
        return self.fix_basis(x, y, z)

    def get_3axis_from_multiple_edges(self, edges):
        normals = []
        for edge in edges:
            pt1, pt2 = edge.connectedVertices()
            normals.append(pt1.getNormal('world') + pt2.getNormal('world'))

        average_normal = sum(normals) / len(normals)
        y = average_normal.normal()
        _x, _y, _z = self.get_3axis_from_edge(edge)
        x = y.cross(_x)
        z = x.cross(y)
        return self.fix_basis(x.normal(), y.normal(), z.normal())



    @compute_time
    def get_3axis_from_2_points(self, pt1, pt2):
        x = (pt1.getPosition('world') - pt2.getPosition('world')).normal()
        y = ((pt1.getNormal('world') + pt2.getNormal('world')) / 2).normal()
        z = x.cross(y)
        return x, y, z

    @compute_time
    def get_3axis_from_2_edge(self, e1, e2):
        pt11, pt12 = e1.connectedVertices()
        pt21, pt22 = e2.connectedVertices()
        return self.get_3axis_from_4_points(pt11, pt12, pt21, pt22)

    @compute_time
    def get_3axis_from_1_point_and_1_edge(self, pt, edge):
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

        return self.fix_basis(x, y, z)

    @compute_time
    def get_3axis_from_3_points(self, pt1, pt2, pt3):
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
        return self.fix_basis(x, y, z)

    @compute_time
    def get_3axis_from_4_points(self, pt11, pt12, pt21, pt22):
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
        z = x.cross(y).normal()
        return self.fix_basis(x, y, z)

    # ========================================
    @compute_time
    def basis_to_transformation_matrix(self, x, y, z, pos=None):
        mx = dt.TransformationMatrix(x.x, x.y, x.z, 0,
                                     y.x, y.y, y.z, 0,
                                     z.x, z.y, z.z, 0)
        if pos:
            mx.setTranslation(tuple(pos), 'world')
        return mx

    @compute_time
    def transformation_matrix_to_basis(self, mx):
        return (dt.Vector(mx[0][0], mx[0][1], mx[0][2]),
                dt.Vector(mx[1][0], mx[1][1], mx[1][2]),
                dt.Vector(mx[2][0], mx[2][1], mx[2][2])
                )

    @compute_time
    def get_offset_matrix(self, mx):
        orig_mx = self.object.getMatrix(worldSpace=True)
        offset_m = dt.TransformationMatrix(orig_mx * mx.asMatrixInverse())
        return offset_m

    @compute_time
    def orient(self, main_axis=None):
        self.clear_preview_axis()
        x, y, z = [a.normal() for a in self.get_axis_from_selection()]
        print(x, y, z)
        if main_axis:
            x, y, z = self.align_up_to(x, y, z, main_axis)
        mx = self.basis_to_transformation_matrix(x, y, z, self.center)
        final_mx = self.get_offset_matrix(mx)
        with UndoChunk():
            self.object.setMatrix(final_mx)
            self.drop_down()

    @compute_time
    def get_rotation_matrix(self, axis, degree, center=None):
        """Возвращает матрицу поворота вокруг центра для задданного объекта"""
        rotate = [0, 0, 0]
        index = dict(x=0, y=1, z=2)[axis.lower().strip('-')]
        rotate[index] += degree * (-1 if '-' in axis else 1)
        m = dt.TransformationMatrix()
        m.setRotatePivot(tuple(center or self.center), 'object', True)
        m.setRotation(rotate)
        return m

    @compute_time
    def fix_basis(self, x, y, z):
        if x.cross(y).dot(z) < 0:
            z *= -1
        return x, y, z

    @compute_time
    def rotate_object(self, axis, degree):
        mx = self.get_rotation_matrix(axis, degree)
        self.object.setMatrix(self.object.getMatrix() * mx)
        self.drop_down()

    @compute_time
    def drop_down(self, basis=None):
        from restore_object_orient.geo_tools import get_lowes_point

        # offset = min([x.getPosition('world')[1] for x in self.iter_points(self.object)])
        offset = get_lowes_point(str(self.object))
        move(self.object, [0, -offset, 0], relative=True)

    @compute_time
    def move_to_origin(self):
        center = self.center
        move(self.object, [-center.x, 0, -center.z], relative=True)

    @compute_time
    def move_to_center(self):
        center = self.center
        move(self.object, [-center.x, -center.y, -center.z], relative=True)

    @compute_time
    def closest_axis(self, vector):
        axis = dict(
            x=dt.Vector([1, 0, 0]),
            y=dt.Vector([0, 1, 0]),
            z=dt.Vector([0, 0, 1])
        )
        values = {a: vector.normal().dot(axis[a]) for a in axis}
        return axis[sorted(values.keys(), key=lambda x: values[x])[-1]]

    @classmethod
    @compute_time
    def create_axis(cls, pt1, pt2=None, color=None, normalize=False, center=None):
        p1 = pt1
        p2 = pt2
        if not p2:
            p1 = dt.Vector([0, 0, 0])
            p2 = pt1
        crv = curve(d=1, p=[p1, p2], k=[0, 1])
        if color:
            val = cls.colors.get(color, 0)
            if val is not None:
                crv.getShape().overrideEnabled.set(True)
                crv.getShape().overrideColor.set(val)
        if center:
            move(crv, center)
        select(cl=1)
        return crv

    @compute_time
    def create_basis(self, x, y, z, scale=1, pos=None, parent_name=None):
        center = pos or geo_tools.get_selection_center()
        p = createNode('transform', name=parent_name or self.grp_name)
        p | self.create_axis(x * scale, color='r', center=center)
        p | self.create_axis(y * scale, color='g', center=center)
        p | self.create_axis(z * scale, color='b', center=center)
        return p

    @compute_time
    def show_axis(self, axes=None, scale=None, main_axis=None):
        if not axes:
            try:
                axes = [a.normal() for a in self.get_axis_from_selection()]
            except SelectionError as e:
                displayWarning(str(e))
                return
        scale = scale or sum(self.object.boundingBox().max()) / 3
        x, y, z = axes
        if main_axis:
            x, y, z = self.align_up_to(x, y, z, main_axis)
        print('X', x)
        print('Y', y)
        print('Z', z)
        sel = selected()
        self.clear_preview_axis()
        self.create_basis(x, y, z, scale=scale)
        select(sel)

    @compute_time
    def clear_preview_axis(self):
        if self.preview_axis_exists():
            delete(self.grp_name)

    @compute_time
    def preview_axis_exists(self):
        return objExists(self.grp_name)

    # @staticmethod
    # @compute_time
    # def get_selection_center():
    #     sel = selected()
    #     if not sel:
    #         return dt.Vector()
    #     pos_array = []
    #     for s in sel:
    #         if isinstance(s, MeshEdge):
    #             for p in s.connectedVertices():
    #                 pos_array.append(p.getPosition('world'))
    #         elif isinstance(s, MeshFace):
    #             pos_array.extend([dt.Vector(x) for x in s.getPoints('world')])
    #         elif isinstance(s, MeshVertex):
    #             pos_array.append(s.getPosition('world'))
    #     pos = sum(pos_array, dt.Vector()) / len(pos_array)
    #     return pos

    # @staticmethod
    # @compute_time
    # def iter_shapes(obj):
    #     shapes = obj.listRelatives(s=1, allDescendents=1)
    #     for s in shapes:
    #         yield s

    # @classmethod
    # @compute_time
    # def iter_points(cls, obj):
    #     for s in cls.iter_shapes(obj):
    #         for vtx in s.vtx:
    #             yield vtx

    @compute_time
    def freeze_transformations(self):
        geo_tools.freeze_transformations(self.object)
        self.freezed = True

    @compute_time
    def align_up_to(self, x, y, z, to_axis):
        c = dt.Vector()
        if to_axis == 'x':
            rm = self.get_rotation_matrix('z', -90, c)
        elif to_axis == '-x':
            rm = self.get_rotation_matrix('z', 90, c)
        elif to_axis == 'y':
            return x, y, z
        elif to_axis == '-y':
            rm = self.get_rotation_matrix('z', 180, c)
        elif to_axis == 'z':
            rm = self.get_rotation_matrix('x', 90, c)
        elif to_axis == '-z':
            rm = self.get_rotation_matrix('x', -90, c)
        else:
            raise
        mx = self.basis_to_transformation_matrix(x, y, z, c)
        r_mx = rm * mx
        return self.transformation_matrix_to_basis(r_mx)

    @compute_time
    def _create_offset_basis(self):
        pi1, pi2, pi3 = [x[1] for x in self.init_points]
        x1, y1, z1 = self._vector_list_to_basis(pi1, pi2, pi3)

        self.create_basis(x1.normal(), y1.normal(), z1.normal(), 30, pos=pi2)

        all_vtx = list(self.iter_points(self.object))
        curr_points = [(index, dt.Vector(all_vtx[index].getPosition('world'))) for index, init_pt in self.init_points]
        pr1, pr2, pr3 = [x[1] for x in curr_points]
        x2, y2, z2 = self._vector_list_to_basis(pr1, pr2, pr3)

        self.create_basis(x2.normal(), y2.normal(), z2.normal(), 30, pos=pr2)
