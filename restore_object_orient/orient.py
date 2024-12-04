from pymel.core import *
from . import tools



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

    def move_to_start_position(self):
        if not self.freezed:
            raise Exception('Source object is not freezed')
        pi1, pi2, pi3 = [x[1] for x in self.init_points]
        x1, y1, z1 = tools.vector_list_to_basis(pi1, pi2, pi3)

        curr_points = [vtx.getPosition('world') for vtx, init_pt in self.init_points]
        pr1, pr2, pr3 = curr_points
        x2, y2, z2 = tools.vector_list_to_basis(pr1, pr2, pr3)

        m1 = self.basis_to_transformation_matrix(x1, y1, z1, pi2)
        m2 = self.basis_to_transformation_matrix(x2, y2, z2, pr2)

        self.object.setMatrix(m2.asMatrixInverse() * m1)

    @property
    def object_vertex_count(self):
        return tools.get_object_vertex_count(self.object)

    @property
    def center(self):
        return tools.get_object_center(str(self.object))

    def rotate_to_world_axis(self, world_axis: str):
        src_axis = tools.get_1axis_from_selection()
        tools.rotate_to_world_axis(src_axis, self.object, world_axis)

    def rotate_to_world_plane(self, world_axis1: str, world_axis2: str, rot_axis = None):
        src_axis = tools.get_1axis_from_selection()
        tools.rotate_to_world_plane(src_axis, self.object, world_axis1, world_axis2, rot_axis)

    def get_offset_matrix(self, mx):
        orig_mx = self.object.getMatrix(worldSpace=True)
        offset_m = dt.TransformationMatrix(orig_mx * mx.asMatrixInverse())
        return offset_m

    def orient(self, main_axis=None):
        self.clear_preview_axis()
        x, y, z = [a.normal() for a in tools.get_3axis_from_selection()]
        if main_axis:
            x, y, z = tools.align_up_to(x, y, z, main_axis)
        mx = tools.basis_to_transformation_matrix(x, y, z, self.center)
        final_mx = self.get_offset_matrix(mx)
        with UndoChunk():
            self.object.setMatrix(final_mx)
            self.drop_down()

    def rotate_object(self, axis, degree):
        mx = tools.get_rotation_matrix(axis, degree, center=self.center)
        self.object.setMatrix(self.object.getMatrix() * mx)
        self.drop_down()

    def drop_down(self, to_center=False):
        from restore_object_orient.tools import get_lowes_point

        offset = get_lowes_point(str(self.object))
        pos = dt.Vector(0, -offset, 0)
        if to_center:
            center = dt.Vector(*tools.get_object_center(self.object))
            center.y = 0
            pos -= center
        move(self.object, tuple(pos), relative=True)

    def move_to_origin(self):
        center = self.center
        move(self.object, [-center.x, 0, -center.z], relative=True)

    def move_to_center(self):
        center = self.center
        move(self.object, [-center.x, -center.y, -center.z], relative=True)

    def move_to_selected(self):
        if not self.object:
            return
        selected_center = tools.get_center_point_from_selection()
        if not selected_center:
            return
        curr_pos = self.object.t.get()
        new_pos = curr_pos - selected_center
        move(self.object, new_pos, relative=False)

    @classmethod
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

    def create_basis(self, x, y, z, scale=1, pos=None, parent_name=None):
        center = pos or tools.get_selection_center()
        p = createNode('transform', name=parent_name or self.grp_name)
        p | self.create_axis(x * scale, color='r', center=center)
        p | self.create_axis(y * scale, color='g', center=center)
        p | self.create_axis(z * scale, color='b', center=center)
        return p

    def show_axis(self, axes=None, scale=None, main_axis=None):
        if not axes:
            try:
                axes = [a.normal() for a in tools.get_3axis_from_selection()]
            except tools.SelectionError as e:
                displayWarning(str(e))
                return
        scale = scale or sum(self.object.boundingBox().max()) / 3
        x, y, z = axes
        if main_axis:
            x, y, z = self.align_up_to(x, y, z, main_axis)
        sel = selected()
        self.clear_preview_axis()
        self.create_basis(x, y, z, scale=scale)
        select(sel)

    def clear_preview_axis(self):
        if self.preview_axis_exists():
            delete(self.grp_name)

    def preview_axis_exists(self):
        return objExists(self.grp_name)

    def freeze_transformations(self):
        tools.freeze_transformations(self.object)
        self.freezed = True

    def _create_offset_basis(self):
        pi1, pi2, pi3 = [x[1] for x in self.init_points]
        x1, y1, z1 = tools.vector_list_to_basis(pi1, pi2, pi3)

        self.create_basis(x1.normal(), y1.normal(), z1.normal(), 30, pos=pi2)

        all_vtx = list(tools.iter_object_points(self.object))
        curr_points = [(index, dt.Vector(all_vtx[index].getPosition('world'))) for index, init_pt in self.init_points]
        pr1, pr2, pr3 = [x[1] for x in curr_points]
        x2, y2, z2 = tools.vector_list_to_basis(pr1, pr2, pr3)

        self.create_basis(x2.normal(), y2.normal(), z2.normal(), 30, pos=pr2)
