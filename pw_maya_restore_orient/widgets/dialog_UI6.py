# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_ObjectOrient(object):
    def setupUi(self, ObjectOrient):
        if not ObjectOrient.objectName():
            ObjectOrient.setObjectName(u"ObjectOrient")
        ObjectOrient.resize(358, 762)
        self.clise_act = QAction(ObjectOrient)
        self.clise_act.setObjectName(u"clise_act")
        self.manual_act = QAction(ObjectOrient)
        self.manual_act.setObjectName(u"manual_act")
        self.centralwidget = QWidget(ObjectOrient)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.obj_btp = QGroupBox(self.centralwidget)
        self.obj_btp.setObjectName(u"obj_btp")
        self.verticalLayout_2 = QVBoxLayout(self.obj_btp)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.set_obj_btn = QPushButton(self.obj_btp)
        self.set_obj_btn.setObjectName(u"set_obj_btn")
        font = QFont()
        font.setPointSize(12)
        self.set_obj_btn.setFont(font)

        self.verticalLayout_2.addWidget(self.set_obj_btn)

        self.obj_name_lb = QLabel(self.obj_btp)
        self.obj_name_lb.setObjectName(u"obj_name_lb")
        self.obj_name_lb.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.obj_name_lb)


        self.verticalLayout_3.addWidget(self.obj_btp)

        self.align_grp = QGroupBox(self.centralwidget)
        self.align_grp.setObjectName(u"align_grp")
        self.verticalLayout = QVBoxLayout(self.align_grp)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.align_btn = QPushButton(self.align_grp)
        self.align_btn.setObjectName(u"align_btn")
        self.align_btn.setMinimumSize(QSize(0, 40))
        font1 = QFont()
        font1.setPointSize(14)
        self.align_btn.setFont(font1)

        self.verticalLayout.addWidget(self.align_btn)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.axis_x_btn = QPushButton(self.align_grp)
        self.axis_x_btn.setObjectName(u"axis_x_btn")
        self.axis_x_btn.setMinimumSize(QSize(0, 40))
        self.axis_x_btn.setMaximumSize(QSize(1000, 16777215))
        self.axis_x_btn.setFont(font1)

        self.horizontalLayout.addWidget(self.axis_x_btn)

        self.axis_y_btn = QPushButton(self.align_grp)
        self.axis_y_btn.setObjectName(u"axis_y_btn")
        self.axis_y_btn.setMinimumSize(QSize(0, 40))
        self.axis_y_btn.setMaximumSize(QSize(1000, 16777215))
        self.axis_y_btn.setFont(font1)

        self.horizontalLayout.addWidget(self.axis_y_btn)

        self.axis_z_btn = QPushButton(self.align_grp)
        self.axis_z_btn.setObjectName(u"axis_z_btn")
        self.axis_z_btn.setMinimumSize(QSize(0, 40))
        self.axis_z_btn.setMaximumSize(QSize(1000, 16777215))
        self.axis_z_btn.setFont(font1)

        self.horizontalLayout.addWidget(self.axis_z_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.align_grp)

        self.rotate_grp = QGroupBox(self.centralwidget)
        self.rotate_grp.setObjectName(u"rotate_grp")
        self.gridLayout = QGridLayout(self.rotate_grp)
        self.gridLayout.setObjectName(u"gridLayout")
        self.rotate_to_x_btn = QPushButton(self.rotate_grp)
        self.rotate_to_x_btn.setObjectName(u"rotate_to_x_btn")

        self.gridLayout.addWidget(self.rotate_to_x_btn, 0, 0, 1, 2)

        self.rotate_to_y_btn = QPushButton(self.rotate_grp)
        self.rotate_to_y_btn.setObjectName(u"rotate_to_y_btn")

        self.gridLayout.addWidget(self.rotate_to_y_btn, 0, 2, 1, 2)

        self.rotate_to_z_btn = QPushButton(self.rotate_grp)
        self.rotate_to_z_btn.setObjectName(u"rotate_to_z_btn")

        self.gridLayout.addWidget(self.rotate_to_z_btn, 0, 4, 1, 2)

        self.x_rot_add_btn = QPushButton(self.rotate_grp)
        self.x_rot_add_btn.setObjectName(u"x_rot_add_btn")
        self.x_rot_add_btn.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.x_rot_add_btn, 3, 0, 1, 1)

        self.x_rot_sub_btn = QPushButton(self.rotate_grp)
        self.x_rot_sub_btn.setObjectName(u"x_rot_sub_btn")
        self.x_rot_sub_btn.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.x_rot_sub_btn, 3, 1, 1, 1)

        self.y_rot_add_btn = QPushButton(self.rotate_grp)
        self.y_rot_add_btn.setObjectName(u"y_rot_add_btn")
        self.y_rot_add_btn.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.y_rot_add_btn, 3, 2, 1, 1)

        self.y_rot_sub_btn = QPushButton(self.rotate_grp)
        self.y_rot_sub_btn.setObjectName(u"y_rot_sub_btn")
        self.y_rot_sub_btn.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.y_rot_sub_btn, 3, 3, 1, 1)

        self.z_rot_add_btn = QPushButton(self.rotate_grp)
        self.z_rot_add_btn.setObjectName(u"z_rot_add_btn")
        self.z_rot_add_btn.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.z_rot_add_btn, 3, 4, 1, 1)

        self.z_rot_sub_btn = QPushButton(self.rotate_grp)
        self.z_rot_sub_btn.setObjectName(u"z_rot_sub_btn")
        self.z_rot_sub_btn.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.z_rot_sub_btn, 3, 5, 1, 1)

        self.rotate_to_xz_btn = QPushButton(self.rotate_grp)
        self.rotate_to_xz_btn.setObjectName(u"rotate_to_xz_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rotate_to_xz_btn.sizePolicy().hasHeightForWidth())
        self.rotate_to_xz_btn.setSizePolicy(sizePolicy)
        self.rotate_to_xz_btn.setMaximumSize(QSize(1000, 16777215))

        self.gridLayout.addWidget(self.rotate_to_xz_btn, 2, 0, 1, 2)

        self.rotate_to_xy_btn = QPushButton(self.rotate_grp)
        self.rotate_to_xy_btn.setObjectName(u"rotate_to_xy_btn")
        sizePolicy.setHeightForWidth(self.rotate_to_xy_btn.sizePolicy().hasHeightForWidth())
        self.rotate_to_xy_btn.setSizePolicy(sizePolicy)
        self.rotate_to_xy_btn.setMaximumSize(QSize(1000, 16777215))

        self.gridLayout.addWidget(self.rotate_to_xy_btn, 2, 2, 1, 2)

        self.rotate_to_yz_btn = QPushButton(self.rotate_grp)
        self.rotate_to_yz_btn.setObjectName(u"rotate_to_yz_btn")
        sizePolicy.setHeightForWidth(self.rotate_to_yz_btn.sizePolicy().hasHeightForWidth())
        self.rotate_to_yz_btn.setSizePolicy(sizePolicy)
        self.rotate_to_yz_btn.setMaximumSize(QSize(1000, 16777215))

        self.gridLayout.addWidget(self.rotate_to_yz_btn, 2, 4, 1, 2)


        self.verticalLayout_3.addWidget(self.rotate_grp)

        self.set_origin_grp = QGroupBox(self.centralwidget)
        self.set_origin_grp.setObjectName(u"set_origin_grp")
        self.gridLayout_3 = QGridLayout(self.set_origin_grp)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.set_origin_to_base_btn = QPushButton(self.set_origin_grp)
        self.set_origin_to_base_btn.setObjectName(u"set_origin_to_base_btn")
        self.set_origin_to_base_btn.setMaximumSize(QSize(1000, 16777215))
        self.set_origin_to_base_btn.setFont(font)

        self.gridLayout_3.addWidget(self.set_origin_to_base_btn, 0, 0, 1, 1)

        self.set_origin_to_selected_btn = QPushButton(self.set_origin_grp)
        self.set_origin_to_selected_btn.setObjectName(u"set_origin_to_selected_btn")
        self.set_origin_to_selected_btn.setMaximumSize(QSize(1000, 16777215))
        self.set_origin_to_selected_btn.setFont(font)

        self.gridLayout_3.addWidget(self.set_origin_to_selected_btn, 0, 2, 1, 1)

        self.set_origin_to_center_btn = QPushButton(self.set_origin_grp)
        self.set_origin_to_center_btn.setObjectName(u"set_origin_to_center_btn")
        self.set_origin_to_center_btn.setMaximumSize(QSize(1000, 16777215))
        self.set_origin_to_center_btn.setFont(font)

        self.gridLayout_3.addWidget(self.set_origin_to_center_btn, 0, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.set_origin_grp)

        self.finalize_grp = QGroupBox(self.centralwidget)
        self.finalize_grp.setObjectName(u"finalize_grp")
        self.gridLayout_2 = QGridLayout(self.finalize_grp)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.freeze_btn = QPushButton(self.finalize_grp)
        self.freeze_btn.setObjectName(u"freeze_btn")
        self.freeze_btn.setMinimumSize(QSize(0, 40))
        self.freeze_btn.setFont(font)

        self.gridLayout_2.addWidget(self.freeze_btn, 0, 0, 1, 1)

        self.reset_btn = QPushButton(self.finalize_grp)
        self.reset_btn.setObjectName(u"reset_btn")
        self.reset_btn.setMinimumSize(QSize(0, 40))
        self.reset_btn.setFont(font)

        self.gridLayout_2.addWidget(self.reset_btn, 0, 1, 1, 1)

        self.restore_btn = QPushButton(self.finalize_grp)
        self.restore_btn.setObjectName(u"restore_btn")
        self.restore_btn.setMinimumSize(QSize(0, 40))
        self.restore_btn.setFont(font)

        self.gridLayout_2.addWidget(self.restore_btn, 1, 0, 1, 2)


        self.verticalLayout_3.addWidget(self.finalize_grp)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.help_label_lb = QLabel(self.centralwidget)
        self.help_label_lb.setObjectName(u"help_label_lb")
        self.help_label_lb.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.help_label_lb)

        self.help_btn = QPushButton(self.centralwidget)
        self.help_btn.setObjectName(u"help_btn")
        self.help_btn.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.help_btn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        ObjectOrient.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ObjectOrient)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 358, 34))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        ObjectOrient.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.clise_act)
        self.menuHelp.addAction(self.manual_act)

        self.retranslateUi(ObjectOrient)

        QMetaObject.connectSlotsByName(ObjectOrient)
    # setupUi

    def retranslateUi(self, ObjectOrient):
        ObjectOrient.setWindowTitle(QCoreApplication.translate("ObjectOrient", u"Object Orient", None))
        self.clise_act.setText(QCoreApplication.translate("ObjectOrient", u"Close", None))
        self.manual_act.setText(QCoreApplication.translate("ObjectOrient", u"Manual", None))
        self.obj_btp.setTitle(QCoreApplication.translate("ObjectOrient", u"Crrent Object", None))
        self.set_obj_btn.setText(QCoreApplication.translate("ObjectOrient", u"Set Object", None))
        self.obj_name_lb.setText(QCoreApplication.translate("ObjectOrient", u"Object Not Set", None))
        self.align_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Align Selected ", None))
        self.align_btn.setText(QCoreApplication.translate("ObjectOrient", u"Quick Align ", None))
        self.axis_x_btn.setText(QCoreApplication.translate("ObjectOrient", u"X", None))
        self.axis_y_btn.setText(QCoreApplication.translate("ObjectOrient", u"Y", None))
        self.axis_z_btn.setText(QCoreApplication.translate("ObjectOrient", u"Z", None))
        self.rotate_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Rotate Selected To", None))
        self.rotate_to_x_btn.setText(QCoreApplication.translate("ObjectOrient", u"X", None))
        self.rotate_to_y_btn.setText(QCoreApplication.translate("ObjectOrient", u"Y", None))
        self.rotate_to_z_btn.setText(QCoreApplication.translate("ObjectOrient", u"Z", None))
        self.x_rot_add_btn.setText(QCoreApplication.translate("ObjectOrient", u"+90", None))
        self.x_rot_sub_btn.setText(QCoreApplication.translate("ObjectOrient", u"-90", None))
        self.y_rot_add_btn.setText(QCoreApplication.translate("ObjectOrient", u"+90", None))
        self.y_rot_sub_btn.setText(QCoreApplication.translate("ObjectOrient", u"-90", None))
        self.z_rot_add_btn.setText(QCoreApplication.translate("ObjectOrient", u"+90", None))
        self.z_rot_sub_btn.setText(QCoreApplication.translate("ObjectOrient", u"-90", None))
        self.rotate_to_xz_btn.setText(QCoreApplication.translate("ObjectOrient", u"XZ", None))
        self.rotate_to_xy_btn.setText(QCoreApplication.translate("ObjectOrient", u"XY", None))
        self.rotate_to_yz_btn.setText(QCoreApplication.translate("ObjectOrient", u"YZ", None))
        self.set_origin_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Set Origin To", None))
#if QT_CONFIG(tooltip)
        self.set_origin_to_base_btn.setToolTip(QCoreApplication.translate("ObjectOrient", u"<html><head/><body><p>Place the object on the zero plane with its lowest point.</p><p><span style=\" font-style:italic;\">Hold down Shift to also move the object to the center along the other axes.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.set_origin_to_base_btn.setText(QCoreApplication.translate("ObjectOrient", u"Base", None))
#if QT_CONFIG(tooltip)
        self.set_origin_to_selected_btn.setToolTip(QCoreApplication.translate("ObjectOrient", u"<html><head/><body><p>Calculate the center of the selected elements and move this point to the center of global coordinates.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.set_origin_to_selected_btn.setText(QCoreApplication.translate("ObjectOrient", u"Selected", None))
#if QT_CONFIG(tooltip)
        self.set_origin_to_center_btn.setToolTip(QCoreApplication.translate("ObjectOrient", u"<html><head/><body><p>Place the object with its center at the center of global coordinates.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.set_origin_to_center_btn.setText(QCoreApplication.translate("ObjectOrient", u"Center", None))
        self.finalize_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Finalize", None))
        self.freeze_btn.setText(QCoreApplication.translate("ObjectOrient", u"Freeze", None))
        self.reset_btn.setText(QCoreApplication.translate("ObjectOrient", u"Reset", None))
        self.restore_btn.setText(QCoreApplication.translate("ObjectOrient", u"Restore Initial Transform", None))
        self.help_label_lb.setText(QCoreApplication.translate("ObjectOrient", u"<html><head/><body><p>Hold down the <span style=\" font-weight:600;\">Shift</span> or <span style=\" font-weight:600;\">Ctrl</span> key <br/>to change the action mode.</p></body></html>", None))
        self.help_btn.setText(QCoreApplication.translate("ObjectOrient", u"?", None))
        self.menuFile.setTitle(QCoreApplication.translate("ObjectOrient", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("ObjectOrient", u"Help", None))
    # retranslateUi

