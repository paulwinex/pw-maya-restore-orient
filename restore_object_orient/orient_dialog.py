from __future__ import absolute_import
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from functools import partial
import traceback
from .widgets import dialog_UI
from pymel.core import *
from . import orient


qMaya = ui.PyUI('MayaWindow').asQtObject()


class ObjectOrientDialog(QWidget, dialog_UI.Ui_ObjectOrient):
    def __init__(self):
        super(ObjectOrientDialog, self).__init__(qMaya)
        self.setupUi(self)
        self.setWindowFlags(Qt.Tool)

        self.set_obj_btn.clicked.connect(self.set_object)
        self.axis_x_btn.clicked.connect(partial(self.on_align, 'x'))
        self.axis_y_btn.clicked.connect(partial(self.on_align, 'y'))
        self.axis_z_btn.clicked.connect(partial(self.on_align, 'z'))
        self.align_btn.clicked.connect(self.on_align)

        self.x_add90_btn.clicked.connect(partial(self.on_rotate, 'x', 90))
        self.y_add90_btn.clicked.connect(partial(self.on_rotate, 'y', 90))
        self.z_add90_btn.clicked.connect(partial(self.on_rotate, 'z', 90))
        self.x_add180_btn.clicked.connect(partial(self.on_rotate, 'x', 180))
        self.y_add180_btn.clicked.connect(partial(self.on_rotate, 'y', 180))
        self.z_add180_btn.clicked.connect(partial(self.on_rotate, 'z', 180))

        self.x_sub90_btn.clicked.connect(partial(self.on_rotate, 'x', -90))
        self.y_sub90_btn.clicked.connect(partial(self.on_rotate, 'y', -90))
        self.z_sub90_btn.clicked.connect(partial(self.on_rotate, 'z', -90))
        self.x_sub180_btn.clicked.connect(partial(self.on_rotate, 'x', -180))
        self.y_sub180_btn.clicked.connect(partial(self.on_rotate, 'y', -180))
        self.z_sub180_btn.clicked.connect(partial(self.on_rotate, 'z', -180))

        self.rotate_to_x_btn.clicked.connect(partial(self.rotate_to_world_axis, 'x'))
        self.rotate_to_y_btn.clicked.connect(partial(self.rotate_to_world_axis, 'y'))
        self.rotate_to_z_btn.clicked.connect(partial(self.rotate_to_world_axis, 'z'))

        self.rotate_to_xz_btn.clicked.connect(partial(self.rotate_to_world_plane, 'x', 'z'))
        self.rotate_to_xy_btn.clicked.connect(partial(self.rotate_to_world_plane, 'x', 'y'))
        self.rotate_to_yz_btn.clicked.connect(partial(self.rotate_to_world_plane, 'y', 'z'))
        self.rotate_to_yx_btn.clicked.connect(partial(self.rotate_to_world_plane, 'y', 'x'))
        self.rotate_to_zy_btn.clicked.connect(partial(self.rotate_to_world_plane, 'z', 'y'))
        self.rotate_to_zx_btn.clicked.connect(partial(self.rotate_to_world_plane, 'z', 'x'))

        self.drop_btn.clicked.connect(self.on_drop)
        self.to_center_btn.clicked.connect(self.on_base_to_center)
        self.to_selected_btn.clicked.connect(self.on_base_to_selected)
        self.freeze_btn.clicked.connect(self.on_freeze)
        self.reset_btn.clicked.connect(self.on_reset)
        self.restore_btn.clicked.connect(self.on_restore)

        self.orient = None  # type: ignore
        self.set_ui_enabled(False)
        self.restore_btn.setEnabled(False)
        self.resize(320, 200)

    def set_ui_enabled(self, val):
        self.orient_grp.setEnabled(bool(val))
        self.transf_grp.setEnabled(bool(val))
        self.set_origin_grp.setEnabled(bool(val))
        self.finalize_grp.setEnabled(bool(val))
        self.reset_btn.setEnabled(not self.orient.freezed if self.orient else False)

    def set_object(self, obj=None):
        if not obj:
            sel = selected()
            if not sel:
                PopupError('Nothing selected')
                return
            if len(sel) > 1:
                PopupError('Select single object only')
                return
            obj = sel[0]
        if not isinstance(obj, nt.Transform):
            PopupError('Select Transform Node')
            return
        self.orient = orient.ObjOrient(obj)
        self.obj_name_lb.setText(obj.name())
        self.set_ui_enabled(True)
        self.restore_btn.setEnabled(False)
        self.freeze_btn.setEnabled(True)

    def on_align(self, main_axis=None):
        if not self.orient:
            return
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ShiftModifier:
            if main_axis:
                main_axis = '-' + main_axis
        if self.orient.preview_axis_exists():
            self.orient.clear_preview_axis()
        if not modifiers == Qt.ControlModifier:
            preview = self.preview_cbx.isChecked()
            if preview:
                with UndoChunk():
                    self.orient.show_axis(main_axis=main_axis)
            else:
                with UndoChunk():
                    self.orient.orient(main_axis)

    def on_rotate(self, axis, value):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            value *= 2
        if not self.orient:
            return
        self.orient.rotate_object(axis, value)

    def rotate_to_world_axis(self, axis):
        if not self.orient:
            return
        try:
            self.orient.rotate_to_world_axis(axis)
        except Exception as e:
            traceback.print_exc()
            PopupError(str(e))

    def rotate_to_world_plane(self, axis1, axis2):
        if not self.orient:
            return
        rot_axis = dt.Vector(0, 1, 0) if QApplication.keyboardModifiers() == Qt.ShiftModifier else None
        try:
            self.orient.rotate_to_world_plane(axis1, axis2, rot_axis)
        except Exception as e:
            PopupError(str(e))

    def on_drop(self):
        if not self.orient:
            return
        try:
            self.orient.drop_down(to_center=QApplication.keyboardModifiers() == Qt.ShiftModifier)
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_origin(self):
        if not self.orient:
            return
        try:
            self.orient.move_to_origin()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_base_to_center(self):
        if not self.orient:
            return
        try:
            self.orient.move_to_center()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_base_to_selected(self):
        if not self.orient:
            return
        try:
            self.orient.move_to_selected()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_freeze(self):
        if self.orient:
            try:
                self.orient.freeze_transformations()
                self.restore_btn.setEnabled(True)
                self.reset_btn.setEnabled(False)
            except Exception as e:
                PopupError(str(e))
                traceback.print_exc()

    def on_reset(self):
        if not self.orient:
            return
        if self.orient.freezed:
            PopupError('Object already Freezed')
            return
        try:
            self.orient.reset()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()
        self.restore_btn.setEnabled(False)
        self.freeze_btn.setEnabled(True)

    def on_restore(self):
        if not self.orient:
            return
        try:
            self.orient.move_to_start_position()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()
        self.freeze_btn.setEnabled(False)
