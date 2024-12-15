from __future__ import absolute_import
from importlib import reload

try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from .widgets import dialog_UI2 as dialog_UI
except ModuleNotFoundError:
    from PySide6.QtWidgets import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from .widgets import dialog_UI6 as dialog_UI
from functools import partial
import traceback
from pymel.core import *
from . import orient

reload(dialog_UI)


qMaya = ui.PyUI('MayaWindow').asQtObject()


class ObjectOrientDialog(QMainWindow, dialog_UI.Ui_ObjectOrient):
    manual_url = 'https://github.com/paulwinex/pw-maya-restore-orient'

    def __init__(self):
        super(ObjectOrientDialog, self).__init__(qMaya)
        self.setupUi(self)
        self.setWindowFlags(Qt.Tool)
        self._alter_widgets = []
        # Current Object
        self.set_obj_btn.clicked.connect(self.set_object)
        self.set_obj_btn.setProperty('btn_text', {'default': 'Set Object', 'ctrl': 'Unset'})
        # Align selected
        self.align_btn.clicked.connect(self.on_align_pressed)
        # self.align_btn.setProperty('btn_text', {'default': 'Quick Align', 'ctrl': 'Preview'})
        self.preview_btn.clicked.connect(self.create_preview_axis_for_selection)
        self.axis_x_btn.clicked.connect(partial(self.on_align_pressed, 'x'))
        self.axis_x_btn.setProperty('btn_text', {'default': 'X', 'shift': '-X'})
        self.axis_y_btn.clicked.connect(partial(self.on_align_pressed, 'y'))
        self.axis_y_btn.setProperty('btn_text', {'default': 'Y', 'shift': '-Y'})
        self.axis_z_btn.clicked.connect(partial(self.on_align_pressed, 'z'))
        self.axis_z_btn.setProperty('btn_text', {'default': 'Z', 'shift': '-Z'})
        self._alter_widgets.extend([
            self.set_obj_btn, self.align_btn, self.axis_x_btn, self.axis_y_btn, self.axis_z_btn,
        ])
        # Rotate selected to
        self.rotate_to_x_btn.clicked.connect(partial(self.rotate_to_world_axis, 'x'))
        self.rotate_to_x_btn.setProperty('btn_text', {'default': 'X', 'shift': '-X'})
        self.rotate_to_y_btn.clicked.connect(partial(self.rotate_to_world_axis, 'y'))
        self.rotate_to_y_btn.setProperty('btn_text', {'default': 'Y', 'shift': '-Y'})
        self.rotate_to_z_btn.clicked.connect(partial(self.rotate_to_world_axis, 'z'))
        self.rotate_to_z_btn.setProperty('btn_text', {'default': 'Z', 'shift': '-Z'})
        self._alter_widgets.extend([
            self.rotate_to_x_btn, self.rotate_to_y_btn, self.rotate_to_z_btn,
        ])

        self.rotate_to_xz_btn.clicked.connect(partial(self.rotate_to_world_plane, 'x', 'z'))
        self.rotate_to_xz_btn.setProperty('btn_text', {'default': 'XZ', 'shift': 'Xz', 'ctrl': 'xZ'})
        self.rotate_to_xy_btn.clicked.connect(partial(self.rotate_to_world_plane, 'x', 'y'))
        self.rotate_to_xy_btn.setProperty('btn_text', {'default': 'XY', 'shift': 'Xy', 'ctrl': 'xY'})
        self.rotate_to_yz_btn.clicked.connect(partial(self.rotate_to_world_plane, 'y', 'z'))
        self.rotate_to_yz_btn.setProperty('btn_text', {'default': 'YZ', 'shift': 'Yz', 'ctrl': 'yZ'})
        self._alter_widgets.extend([
            self.rotate_to_xz_btn, self.rotate_to_xy_btn, self.rotate_to_yz_btn,
        ])

        self.x_rot_add_btn.clicked.connect(partial(self.on_rotate_pressed, 'x', 1))
        self.x_rot_add_btn.setProperty('btn_text', {'default': '+90', 'shift': '+180', 'ctrl': '+45'})
        self.x_rot_sub_btn.clicked.connect(partial(self.on_rotate_pressed, 'x', -1))
        self.x_rot_sub_btn.setProperty('btn_text', {'default': '-90', 'shift': '-180', 'ctrl': '-45'})
        self.y_rot_add_btn.clicked.connect(partial(self.on_rotate_pressed, 'y', 1))
        self.y_rot_add_btn.setProperty('btn_text', {'default': '+90', 'shift': '+180', 'ctrl': '+45'})
        self.y_rot_sub_btn.clicked.connect(partial(self.on_rotate_pressed, 'y', -1))
        self.y_rot_sub_btn.setProperty('btn_text', {'default': '-90', 'shift': '-180', 'ctrl': '-45'})
        self.z_rot_add_btn.clicked.connect(partial(self.on_rotate_pressed, 'z', 1))
        self.z_rot_add_btn.setProperty('btn_text', {'default': '+90', 'shift': '+180', 'ctrl': '+45'})
        self.z_rot_sub_btn.clicked.connect(partial(self.on_rotate_pressed, 'z', -1))
        self.z_rot_sub_btn.setProperty('btn_text', {'default': '-90', 'shift': '-180', 'ctrl': '-45'})
        self._alter_widgets.extend([
            self.x_rot_add_btn, self.x_rot_sub_btn,
            self.y_rot_add_btn, self.y_rot_sub_btn,
            self.z_rot_add_btn, self.z_rot_sub_btn,
        ])
        # Set origin
        self.set_origin_to_base_btn.clicked.connect(self.on_origin_to_base_pressed)
        self.set_origin_to_base_btn.setProperty('btn_text', {'default': 'Base', 'ctrl': 'Drop Down'})
        self.set_origin_to_center_btn.clicked.connect(self.on_origin_to_center_pressed)
        self.set_origin_to_selected_btn.clicked.connect(self.on_origin_to_selected_pressed)
        self._alter_widgets.append(self.set_origin_to_base_btn)
        # Finalize
        self.freeze_btn.clicked.connect(self.on_freeze_pressed)
        self.reset_btn.clicked.connect(self.on_reset_pressed)
        self.restore_btn.clicked.connect(self.on_restore_pressed)
        # Other
        self.help_btn.clicked.connect(self.on_help_pressed)
        self.manual_act.triggered.connect(self.on_help_pressed)
        # Variables
        self.orient = None  # type: ignore
        self.setFocusPolicy(Qt.StrongFocus)
        self.shift_pressed = False
        self.control_pressed = False
        self.set_ui_enabled(False)
        self.update_texts()
        self.resize(320, 200)

    def set_ui_enabled(self, val: bool) -> None:
        self.align_grp.setEnabled(bool(val))
        self.rotate_grp.setEnabled(bool(val))
        self.set_origin_grp.setEnabled(bool(val))
        self.finalize_grp.setEnabled(bool(val))

    def set_object(self, obj: nt.Transform = None) -> None:
        self.reset_object()
        if self.control_pressed:
            return
        if not obj:
            from .tools import get_transform_node_from_selection
            try:
                obj = get_transform_node_from_selection()
            except Exception as e:
                PopupError(str(e))
                return
        if not isinstance(obj, nt.Transform):
            PopupError('Select Transform Node')
            return
        self.orient = orient.ObjOrient(obj)
        self.obj_name_lb.setText(obj.name())
        self.set_ui_enabled(True)

    def reset_object(self) -> None:
        self.orient = None
        self.set_ui_enabled(False)
        self.obj_name_lb.setText('Object Not Set')

    def create_preview_axis_for_selection(self, main_axis: str = None):
        if self.orient.preview_axis_exists():
            self.orient.clear_preview_axis()
            return
        try:
            self.orient.create_preview_axis(main_axis=main_axis, reverse_axis=self.shift_pressed)
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_align_pressed(self, main_axis: str = None):
        if not self.orient:
            PopupError('Object not set')
            return
        if self.orient.preview_axis_exists():
            self.orient.clear_preview_axis()
        if self.control_pressed:
            self.create_preview_axis_for_selection(main_axis)
        else:
            try:
                if main_axis:
                    self.orient.orient_to_axis(main_axis, self.shift_pressed)
                else:
                    self.orient.auto_orient()
            except Exception as e:
                PopupError(str(e))
                traceback.print_exc()

    def on_rotate_pressed(self, axis: str, mult: float):
        value = 90
        if self.shift_pressed:
            value = 180
        elif self.control_pressed:
            value = 45
        value *= mult
        if not self.orient:
            return
        self.orient.rotate_object(axis, value)

    def rotate_to_world_axis(self, axis: str) -> None:
        if not self.orient:
            return
        try:
            self.orient.rotate_to_world_axis(axis, self.shift_pressed)
        except Exception as e:
            traceback.print_exc()
            PopupError(str(e))

    def rotate_to_world_plane(self, axis1: str, axis2: str) -> None:
        if not self.orient:
            return
        rotation_axis = None
        if self.shift_pressed:
            rotation_axis = axis1
        elif self.control_pressed:
            rotation_axis = axis2
        try:
            self.orient.rotate_to_world_plane(axis1, axis2, rotation_axis)
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_origin_to_down_pressed(self) -> None:
        if not self.orient:
            return
        try:
            self.orient.drop_down(down_only=self.shift_pressed)
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_origin_to_base_pressed(self) -> None:
        if not self.orient:
            return
        try:
            if self.control_pressed:
                self.orient.drop_down()
            else:
                self.orient.move_to_origin()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_origin_to_center_pressed(self) -> None:
        if not self.orient:
            return
        try:
            self.orient.move_to_center()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_origin_to_selected_pressed(self) -> None:
        if not self.orient:
            return
        try:
            self.orient.move_to_selected()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_freeze_pressed(self) -> None:
        if self.orient:
            try:
                self.orient.freeze_transformations()
            except Exception as e:
                PopupError(str(e))
                traceback.print_exc()

    def on_reset_pressed(self) -> None:
        if not self.orient:
            return
        if self.orient.frozen:
            PopupError('Object already Frozen')
            return
        try:
            self.orient.reset()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_restore_pressed(self) -> None:
        if not self.orient:
            return
        try:
            self.orient.restore_init_transform()
        except Exception as e:
            PopupError(str(e))
            traceback.print_exc()

    def on_help_pressed(self):
        import webbrowser
        webbrowser.open(self.manual_url)

    # key callbacks

    def update_texts(self) -> None:
        for w in self._alter_widgets:
            btn_text = w.property('btn_text')
            if not btn_text:
                continue
            if self.control_pressed:
                w.setText(btn_text.get('ctrl', btn_text.get('default', '?')))
            elif self.shift_pressed:
                w.setText(btn_text.get('shift', btn_text.get('default', '?')))
            else:
                w.setText(btn_text.get('default', '?'))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = True
            self.control_pressed = False
        elif event.key() == Qt.Key_Control:
            self.shift_pressed = False
            self.control_pressed = True
        else:
            self.control_pressed = False
            self.shift_pressed = False
        self.update_texts()
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.control_pressed = False
        self.shift_pressed = False
        self.update_texts()
        return super().keyReleaseEvent(event)

    def leaveEvent(self, event):
        self.control_pressed = False
        self.shift_pressed = False
        self.update_texts()
        return super().leaveEvent(event)

    def enterEvent(self, event):
        self.activateWindow()
        super().enterEvent(event)