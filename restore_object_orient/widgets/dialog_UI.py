# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_UI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ObjectOrient(object):
    def setupUi(self, ObjectOrient):
        if not ObjectOrient.objectName():
            ObjectOrient.setObjectName(u"ObjectOrient")
        ObjectOrient.resize(311, 752)
        self.verticalLayout_3 = QVBoxLayout(ObjectOrient)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.obj_btp = QGroupBox(ObjectOrient)
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

        self.orient_grp = QGroupBox(ObjectOrient)
        self.orient_grp.setObjectName(u"orient_grp")
        self.verticalLayout = QVBoxLayout(self.orient_grp)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.preview_cbx = QCheckBox(self.orient_grp)
        self.preview_cbx.setObjectName(u"preview_cbx")

        self.verticalLayout.addWidget(self.preview_cbx)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.align_btn = QPushButton(self.orient_grp)
        self.align_btn.setObjectName(u"align_btn")
        self.align_btn.setMinimumSize(QSize(0, 40))
        font1 = QFont()
        font1.setPointSize(14)
        self.align_btn.setFont(font1)

        self.horizontalLayout_2.addWidget(self.align_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label = QLabel(self.orient_grp)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.axis_x_btn = QPushButton(self.orient_grp)
        self.axis_x_btn.setObjectName(u"axis_x_btn")
        self.axis_x_btn.setMinimumSize(QSize(0, 40))
        self.axis_x_btn.setFont(font1)

        self.horizontalLayout.addWidget(self.axis_x_btn)

        self.axis_y_btn = QPushButton(self.orient_grp)
        self.axis_y_btn.setObjectName(u"axis_y_btn")
        self.axis_y_btn.setMinimumSize(QSize(0, 40))
        self.axis_y_btn.setFont(font1)

        self.horizontalLayout.addWidget(self.axis_y_btn)

        self.axis_z_btn = QPushButton(self.orient_grp)
        self.axis_z_btn.setObjectName(u"axis_z_btn")
        self.axis_z_btn.setMinimumSize(QSize(0, 40))
        self.axis_z_btn.setFont(font1)

        self.horizontalLayout.addWidget(self.axis_z_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(self.orient_grp)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.verticalLayout_3.addWidget(self.orient_grp)

        self.transf_grp = QGroupBox(ObjectOrient)
        self.transf_grp.setObjectName(u"transf_grp")
        self.gridLayout = QGridLayout(self.transf_grp)
        self.gridLayout.setObjectName(u"gridLayout")
        self.x_sub90_btn = QPushButton(self.transf_grp)
        self.x_sub90_btn.setObjectName(u"x_sub90_btn")
        self.x_sub90_btn.setMinimumSize(QSize(40, 25))
        self.x_sub90_btn.setMaximumSize(QSize(55, 25))
        self.x_sub90_btn.setFont(font)

        self.gridLayout.addWidget(self.x_sub90_btn, 0, 3, 1, 1)

        self.x_sub180_btn = QPushButton(self.transf_grp)
        self.x_sub180_btn.setObjectName(u"x_sub180_btn")
        self.x_sub180_btn.setMinimumSize(QSize(40, 25))
        self.x_sub180_btn.setMaximumSize(QSize(55, 25))
        self.x_sub180_btn.setFont(font)

        self.gridLayout.addWidget(self.x_sub180_btn, 0, 4, 1, 1)

        self.y_add90_btn = QPushButton(self.transf_grp)
        self.y_add90_btn.setObjectName(u"y_add90_btn")
        self.y_add90_btn.setMinimumSize(QSize(40, 25))
        self.y_add90_btn.setMaximumSize(QSize(55, 25))
        self.y_add90_btn.setFont(font)

        self.gridLayout.addWidget(self.y_add90_btn, 1, 1, 1, 1)

        self.y_add180_btn = QPushButton(self.transf_grp)
        self.y_add180_btn.setObjectName(u"y_add180_btn")
        self.y_add180_btn.setMinimumSize(QSize(40, 25))
        self.y_add180_btn.setMaximumSize(QSize(55, 25))
        self.y_add180_btn.setFont(font)

        self.gridLayout.addWidget(self.y_add180_btn, 1, 0, 1, 1)

        self.y_sub90_btn = QPushButton(self.transf_grp)
        self.y_sub90_btn.setObjectName(u"y_sub90_btn")
        self.y_sub90_btn.setMinimumSize(QSize(40, 25))
        self.y_sub90_btn.setMaximumSize(QSize(55, 25))
        self.y_sub90_btn.setFont(font)

        self.gridLayout.addWidget(self.y_sub90_btn, 1, 3, 1, 1)

        self.z_add90_btn = QPushButton(self.transf_grp)
        self.z_add90_btn.setObjectName(u"z_add90_btn")
        self.z_add90_btn.setMinimumSize(QSize(40, 25))
        self.z_add90_btn.setMaximumSize(QSize(55, 25))
        self.z_add90_btn.setFont(font)

        self.gridLayout.addWidget(self.z_add90_btn, 2, 1, 1, 1)

        self.z_sub90_btn = QPushButton(self.transf_grp)
        self.z_sub90_btn.setObjectName(u"z_sub90_btn")
        self.z_sub90_btn.setMinimumSize(QSize(40, 25))
        self.z_sub90_btn.setMaximumSize(QSize(55, 25))
        self.z_sub90_btn.setFont(font)

        self.gridLayout.addWidget(self.z_sub90_btn, 2, 3, 1, 1)

        self.x_add90_btn = QPushButton(self.transf_grp)
        self.x_add90_btn.setObjectName(u"x_add90_btn")
        self.x_add90_btn.setMinimumSize(QSize(40, 25))
        self.x_add90_btn.setMaximumSize(QSize(55, 25))
        self.x_add90_btn.setFont(font)

        self.gridLayout.addWidget(self.x_add90_btn, 0, 1, 1, 1)

        self.y_sub180_btn = QPushButton(self.transf_grp)
        self.y_sub180_btn.setObjectName(u"y_sub180_btn")
        self.y_sub180_btn.setMinimumSize(QSize(40, 25))
        self.y_sub180_btn.setMaximumSize(QSize(55, 25))
        self.y_sub180_btn.setFont(font)

        self.gridLayout.addWidget(self.y_sub180_btn, 1, 4, 1, 1)

        self.z_sub180_btn = QPushButton(self.transf_grp)
        self.z_sub180_btn.setObjectName(u"z_sub180_btn")
        self.z_sub180_btn.setMinimumSize(QSize(40, 25))
        self.z_sub180_btn.setMaximumSize(QSize(55, 25))
        self.z_sub180_btn.setFont(font)

        self.gridLayout.addWidget(self.z_sub180_btn, 2, 4, 1, 1)

        self.x_add180_btn = QPushButton(self.transf_grp)
        self.x_add180_btn.setObjectName(u"x_add180_btn")
        self.x_add180_btn.setMinimumSize(QSize(40, 25))
        self.x_add180_btn.setMaximumSize(QSize(55, 25))
        self.x_add180_btn.setFont(font)

        self.gridLayout.addWidget(self.x_add180_btn, 0, 0, 1, 1)

        self.z_add180_btn = QPushButton(self.transf_grp)
        self.z_add180_btn.setObjectName(u"z_add180_btn")
        self.z_add180_btn.setMinimumSize(QSize(40, 25))
        self.z_add180_btn.setMaximumSize(QSize(55, 25))
        self.z_add180_btn.setFont(font)

        self.gridLayout.addWidget(self.z_add180_btn, 2, 0, 1, 1)

        self.label_3 = QLabel(self.transf_grp)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 16pt \"Noto Sans\";")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.label_4 = QLabel(self.transf_grp)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"font: 16pt \"Noto Sans\";")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.label_5 = QLabel(self.transf_grp)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 16pt \"Noto Sans\";")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.verticalLayout_3.addWidget(self.transf_grp)

        self.set_origin_grp = QGroupBox(ObjectOrient)
        self.set_origin_grp.setObjectName(u"set_origin_grp")
        self.gridLayout_3 = QGridLayout(self.set_origin_grp)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.to_center_btn = QPushButton(self.set_origin_grp)
        self.to_center_btn.setObjectName(u"to_center_btn")
        self.to_center_btn.setFont(font)

        self.gridLayout_3.addWidget(self.to_center_btn, 0, 1, 1, 1)

        self.drop_btn = QPushButton(self.set_origin_grp)
        self.drop_btn.setObjectName(u"drop_btn")
        self.drop_btn.setFont(font)

        self.gridLayout_3.addWidget(self.drop_btn, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.set_origin_grp)

        self.finalize_grp = QGroupBox(ObjectOrient)
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


        self.retranslateUi(ObjectOrient)

        QMetaObject.connectSlotsByName(ObjectOrient)
    # setupUi

    def retranslateUi(self, ObjectOrient):
        ObjectOrient.setWindowTitle(QCoreApplication.translate("ObjectOrient", u"Object Orient", None))
        self.obj_btp.setTitle(QCoreApplication.translate("ObjectOrient", u"Object", None))
        self.set_obj_btn.setText(QCoreApplication.translate("ObjectOrient", u"Set Object", None))
        self.obj_name_lb.setText(QCoreApplication.translate("ObjectOrient", u"Object Not Set", None))
        self.orient_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Orient", None))
        self.preview_cbx.setText(QCoreApplication.translate("ObjectOrient", u"Preview Mode", None))
        self.align_btn.setText(QCoreApplication.translate("ObjectOrient", u"Align", None))
        self.label.setText(QCoreApplication.translate("ObjectOrient", u"Align Selected To Asxis", None))
        self.axis_x_btn.setText(QCoreApplication.translate("ObjectOrient", u"X", None))
        self.axis_y_btn.setText(QCoreApplication.translate("ObjectOrient", u"Y", None))
        self.axis_z_btn.setText(QCoreApplication.translate("ObjectOrient", u"Z", None))
        self.label_2.setText(QCoreApplication.translate("ObjectOrient", u"<html><head/><body><p><span style=\" font-style:italic;\">Hold Shift To Reverse</span></p></body></html>", None))
        self.transf_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Rotate / Transform", None))
        self.x_sub90_btn.setText(QCoreApplication.translate("ObjectOrient", u"-90", None))
        self.x_sub180_btn.setText(QCoreApplication.translate("ObjectOrient", u"-180", None))
        self.y_add90_btn.setText(QCoreApplication.translate("ObjectOrient", u"+90", None))
        self.y_add180_btn.setText(QCoreApplication.translate("ObjectOrient", u"+180", None))
        self.y_sub90_btn.setText(QCoreApplication.translate("ObjectOrient", u"-90", None))
        self.z_add90_btn.setText(QCoreApplication.translate("ObjectOrient", u"+90", None))
        self.z_sub90_btn.setText(QCoreApplication.translate("ObjectOrient", u"-90", None))
        self.x_add90_btn.setText(QCoreApplication.translate("ObjectOrient", u"+90", None))
        self.y_sub180_btn.setText(QCoreApplication.translate("ObjectOrient", u"-180", None))
        self.z_sub180_btn.setText(QCoreApplication.translate("ObjectOrient", u"-180", None))
        self.x_add180_btn.setText(QCoreApplication.translate("ObjectOrient", u"+180", None))
        self.z_add180_btn.setText(QCoreApplication.translate("ObjectOrient", u"+180", None))
        self.label_3.setText(QCoreApplication.translate("ObjectOrient", u"X", None))
        self.label_4.setText(QCoreApplication.translate("ObjectOrient", u"Y", None))
        self.label_5.setText(QCoreApplication.translate("ObjectOrient", u"Z", None))
        self.set_origin_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Set Origin", None))
        self.to_center_btn.setText(QCoreApplication.translate("ObjectOrient", u"Center", None))
        self.drop_btn.setText(QCoreApplication.translate("ObjectOrient", u"Bottom", None))
        self.finalize_grp.setTitle(QCoreApplication.translate("ObjectOrient", u"Finalize", None))
        self.freeze_btn.setText(QCoreApplication.translate("ObjectOrient", u"Freeze", None))
        self.reset_btn.setText(QCoreApplication.translate("ObjectOrient", u"Reset", None))
        self.restore_btn.setText(QCoreApplication.translate("ObjectOrient", u"Restore Transform", None))
    # retranslateUi

