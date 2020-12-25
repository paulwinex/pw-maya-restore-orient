from __future__ import absolute_import
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from functools import partial
from .widgets import dialog_UI
from pymel.core import *
from . import actions
reload(dialog_UI)
reload(actions)

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

        self.x_add_btn.clicked.connect(partial(self.on_rotate, 'x', 90))
        self.y_add_btn.clicked.connect(partial(self.on_rotate, 'y', 90))
        self.z_add_btn.clicked.connect(partial(self.on_rotate, 'z', 90))
        self.x_sub_btn.clicked.connect(partial(self.on_rotate, 'x', -90))
        self.y_sub_btn.clicked.connect(partial(self.on_rotate, 'y', -90))
        self.z_sub_btn.clicked.connect(partial(self.on_rotate, 'z', -90))

        self.drop_btn.clicked.connect(self.on_drop)
        self.set_origin_btn.clicked.connect(self.on_origin)
        self.freeze_btn.clicked.connect(self.on_freeze)
        self.reset_btn.clicked.connect(self.on_reset)
        self.restore_btn.clicked.connect(self.on_restore)

        self.orient = None  # type: actions.ObjOrient
        self.set_ui_enabled(False)
        self.restore_btn.setEnabled(False)

    def set_ui_enabled(self, val):
        self.orient_grp.setEnabled(bool(val))
        self.transf_grp.setEnabled(bool(val))
        self.freeze_btn.setEnabled(bool(val))
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
        reload(actions)
        self.orient = actions.ObjOrient(obj)
        self.obj_name_lb.setText(obj.name())
        self.set_ui_enabled(True)
        self.restore_btn.setEnabled(False)

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

    def on_drop(self):
        if not self.orient:
            return
        self.orient.drop_down()

    def on_origin(self):
        if not self.orient:
            return
        self.orient.move_to_origin()

    def on_freeze(self):
        if self.orient:
            try:
                self.orient.freeze_transformations()
                self.restore_btn.setEnabled(True)
                self.reset_btn.setEnabled(False)
            except Exception as e:
                PopupError(str(e))

    def on_reset(self):
        if not self.orient:
            return
        if self.orient.freezed:
            PopupError('Object already Freezed')
        self.orient.reset()
        self.restore_btn.setEnabled(False)

    def on_restore(self):
        if not self.orient:
            return
        try:
            self.orient.move_to_start_position()
        except Exception as e:
            PopupError(str(e))
        self.freeze_btn.setEnabled(False)
