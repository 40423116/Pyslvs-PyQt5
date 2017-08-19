# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from .QtModules import *
from .graphics.canvas import DynamicCanvas
from .graphics.color import colorIcons
from .info.info import VERSION
tr = QCoreApplication.translate

def init_Widgets(self):
    #QPainter Window
    self.DynamicCanvasView = DynamicCanvas()
    self.DynamicCanvasView.mouse_getClick.connect(self.addPointGroup)
    self.DynamicCanvasView.zoom_change.connect(self.setZoomBar)
    self.canvasSplitter.insertWidget(0, self.DynamicCanvasView)
    #Entiteis tables
    self.Entiteis_Point = PointTableWidget(self.Entiteis_Point_Widget)
    self.Entiteis_Point_Layout.addWidget(self.Entiteis_Point)
    self.Entiteis_Link = LinkTableWidget(self.Entiteis_Link_Widget)
    self.Entiteis_Link_Layout.addWidget(self.Entiteis_Link)
    self.Entiteis_Chain = ChainTableWidget(self.Entiteis_Chain_Widget)
    self.Entiteis_Chain_Layout.addWidget(self.Entiteis_Chain)
    self.Shaft.setColumnWidth(0, 60)
    self.Shaft.setColumnWidth(1, 85)
    self.Shaft.setColumnWidth(2, 85)
    self.Shaft.setColumnWidth(3, 110)
    self.Shaft.setColumnWidth(4, 110)
    self.Shaft.setColumnWidth(5, 110)
    self.Slider.setColumnWidth(0, 60)
    self.Slider.setColumnWidth(1, 90)
    self.Slider.setColumnWidth(2, 70)
    self.Slider.setColumnWidth(3, 70)
    self.Rod.setColumnWidth(0, 60)
    self.Rod.setColumnWidth(1, 90)
    self.Rod.setColumnWidth(2, 70)
    self.Rod.setColumnWidth(3, 70)
    self.Rod.setColumnWidth(4, 70)
    #Panel widget will hide when not using.
    self.panelWidget.hide()
    #Console dock will hide when startup.
    self.ConsoleWidget.hide()
    #Connect to GUI button switching.
    self.disconnectConsoleButton.setEnabled(not self.args.debug_mode)
    self.connectConsoleButton.setEnabled(self.args.debug_mode)
    #Splitter stretch factor.
    self.MainSplitter.setStretchFactor(0, 2)
    self.MainSplitter.setStretchFactor(1, 5)
    self.panels_splitter.setSizes([100, 500])
    #Version text
    self.menuBar.setCornerWidget(QLabel("Version {}.{}.{} ({})".format(*VERSION)))
    #Properties button on the Point tab widget.
    propertiesButton = QPushButton()
    propertiesButton.setIcon(QIcon(QPixmap(":/icons/properties.png")))
    propertiesButton.setToolTip("Properties")
    propertiesButton.setStatusTip("Properties of this workbook.")
    propertiesButton.clicked.connect(self.on_action_Property_triggered)
    self.PointTab.setCornerWidget(propertiesButton)
    #Focus to all table widgets.
    for table in [self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Chain, self.Shaft, self.Slider, self.Rod]:
        table.itemClicked.connect(self.tableFocusChange)
    #While value change, update the canvas widget.
    self.ZoomBar.valueChanged.connect(self.Reload_Canvas)
    self.LineWidth.valueChanged.connect(self.Reload_Canvas)
    self.Font_size.valueChanged.connect(self.Reload_Canvas)
    self.PathWidth.valueChanged.connect(self.Reload_Canvas)
    self.rotateAngle.valueChanged.connect(self.Reload_Canvas)
    #DynamicCanvasView Right-click menu
    self.DynamicCanvasView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.DynamicCanvasView.customContextMenuRequested.connect(self.on_painter_context_menu)
    self.popMenu_painter = QMenu(self)
    self.action_painter_right_click_menu_add = QAction("Add a Point", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_add)
    self.action_painter_right_click_menu_fix_add = QAction("Add a fixed Point", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_fix_add)
    self.action_painter_right_click_menu_path = QAction("Add a Path Point [Path Solving]", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_path)
    self.DynamicCanvasView.mouse_track.connect(self.context_menu_mouse_pos)
    #Entiteis_Point Right-click menu
    self.Entiteis_Point_Widget.customContextMenuRequested.connect(self.on_point_context_menu)
    self.popMenu_point = QMenu(self)
    self.action_point_right_click_menu_add = QAction("&Add", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_add)
    self.action_point_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_edit)
    self.action_point_right_click_menu_lock = QAction("&Fix / Unfix", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_lock)
    self.action_point_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_copy)
    self.action_point_right_click_menu_copyPoint = QAction("Copy point", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_copyPoint)
    self.action_point_right_click_menu_replace = QAction("&Replace", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_replace)
    self.popMenu_point.addSeparator()
    self.action_point_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_delete)
    #Entiteis_Link Right-click menu
    self.Entiteis_Link_Widget.customContextMenuRequested.connect(self.on_link_context_menu)
    self.popMenu_link = QMenu(self)
    self.action_link_right_click_menu_add = QAction("&Add", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_add)
    self.action_link_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_edit)
    self.action_link_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_copy)
    self.action_link_right_click_menu_shaft = QAction("Turn to Shaft", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_shaft)
    self.popMenu_link.addSeparator()
    self.action_link_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_delete) 
    #Entiteis_Chain Right-click menu
    self.Entiteis_Chain_Widget.customContextMenuRequested.connect(self.on_chain_context_menu)
    self.popMenu_chain = QMenu(self)
    self.action_chain_right_click_menu_add = QAction("&Add", self)
    self.popMenu_chain.addAction(self.action_chain_right_click_menu_add)
    self.action_chain_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_chain.addAction(self.action_chain_right_click_menu_edit)
    self.action_chain_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_chain.addAction(self.action_chain_right_click_menu_copy)
    self.popMenu_chain.addSeparator()
    self.action_chain_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_chain.addAction(self.action_chain_right_click_menu_delete) 
    #Shaft Right-click menu
    self.Shaft_Widget.customContextMenuRequested.connect(self.on_shaft_context_menu)
    self.popMenu_shaft = QMenu(self)
    self.action_shaft_right_click_menu_add = QAction("&Add", self)
    self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_add)
    self.action_shaft_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_edit)
    self.action_shaft_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_copy)
    self.popMenu_shaft.addSeparator()
    self.action_shaft_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_delete) 
    #Slider Right-click menu
    self.Slider_Widget.customContextMenuRequested.connect(self.on_slider_context_menu)
    self.popMenu_slider = QMenu(self)
    self.action_slider_right_click_menu_add = QAction("&Add", self)
    self.popMenu_slider.addAction(self.action_slider_right_click_menu_add)
    self.action_slider_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_slider.addAction(self.action_slider_right_click_menu_edit)
    self.action_slider_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_slider.addAction(self.action_slider_right_click_menu_copy)
    self.popMenu_slider.addSeparator()
    self.action_slider_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_slider.addAction(self.action_slider_right_click_menu_delete) 
    #Rod Right-click menu
    self.Rod_Widget.customContextMenuRequested.connect(self.on_rod_context_menu)
    self.popMenu_rod = QMenu(self)
    self.action_rod_right_click_menu_add = QAction("&Add", self)
    self.popMenu_rod.addAction(self.action_rod_right_click_menu_add)
    self.action_rod_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_rod.addAction(self.action_rod_right_click_menu_edit)
    self.action_rod_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_rod.addAction(self.action_rod_right_click_menu_copy)
    self.popMenu_rod.addSeparator()
    self.action_rod_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_rod.addAction(self.action_rod_right_click_menu_delete)

def action_Enabled(self):
    TWO_POINT = len(self.File.Lists.PointList)>1
    THREE_POINT = len(self.File.Lists.PointList)>2
    #Warning
    for lable in [self.reqLine, self.reqShaft]:
        lable.setVisible(not TWO_POINT)
    for lable in [self.reqChain, self.reqSlider, self.reqRod]:
        lable.setVisible(not THREE_POINT)
    #Add
    for action in [self.action_New_Line, self.action_Set_Shaft, self.action_link_right_click_menu_add, self.action_shaft_right_click_menu_add]:
        action.setEnabled(TWO_POINT)
    for action in [self.action_New_Stay_Chain, self.action_Set_Slider, self.action_Set_Rod,
            self.action_chain_right_click_menu_add, self.action_slider_right_click_menu_add,
            self.action_rod_right_click_menu_add]:
        action.setEnabled(THREE_POINT)
    #Edit
    self.action_Edit_Point.setEnabled(self.Entiteis_Point.rowCount()>1)
    self.action_Edit_Linkage.setEnabled(self.Entiteis_Link.rowCount()>0)
    self.action_Edit_Stay_Chain.setEnabled(self.Entiteis_Chain.rowCount()>0)
    self.action_Edit_Shaft.setEnabled(self.Shaft.rowCount()>0)
    self.action_Edit_Slider.setEnabled(self.Slider.rowCount()>0)
    self.action_Edit_Rod.setEnabled(self.Rod.rowCount()>0)
    self.action_link_right_click_menu_edit.setEnabled(self.Entiteis_Link.rowCount()>0)
    self.action_chain_right_click_menu_edit.setEnabled(self.Entiteis_Chain.rowCount()>0)
    self.action_shaft_right_click_menu_edit.setEnabled(self.Shaft.rowCount()>0)
    self.action_slider_right_click_menu_edit.setEnabled(self.Slider.rowCount()>0)
    self.action_rod_right_click_menu_edit.setEnabled(self.Rod.rowCount()>=1)
    #Delete
    self.action_Delete_Point.setEnabled(self.Entiteis_Point.rowCount()>1)
    self.action_Delete_Linkage.setEnabled(self.Entiteis_Link.rowCount()>0)
    self.action_Delete_Stay_Chain.setEnabled(self.Entiteis_Chain.rowCount()>0)
    self.action_Delete_Shaft.setEnabled(self.Shaft.rowCount()>0)
    self.action_Delete_Slider.setEnabled(self.Slider.rowCount()>0)
    self.action_Delete_Piston_Spring.setEnabled(self.Rod.rowCount()>0)
    self.Parameter_delete.setEnabled(self.Parameter_list.rowCount()>0)
    self.action_link_right_click_menu_delete.setEnabled(self.Entiteis_Link.rowCount()>0)
    self.action_chain_right_click_menu_delete.setEnabled(self.Entiteis_Chain.rowCount()>0)
    self.action_shaft_right_click_menu_delete.setEnabled(self.Shaft.rowCount()>0)
    self.action_slider_right_click_menu_delete.setEnabled(self.Slider.rowCount()>0)
    self.action_rod_right_click_menu_delete.setEnabled(self.Rod.rowCount()>=1)
    #Path
    self.action_Path_Track.setEnabled(self.Shaft.rowCount()>0)
    for action in [self.action_Path_coordinate, self.action_Save_path_only, self.action_Path_Clear]:
        action.setEnabled(bool(self.File.Lists.pathData))
    #Panel
    self.Measurement.setEnabled(self.Entiteis_Point.rowCount()>1)
    self.AuxLine.setEnabled(self.Entiteis_Point.rowCount()>1)
    self.Drive_shaft.setEnabled(self.Shaft.rowCount()>0)
    self.Drive_shaft_activated.setEnabled(self.Shaft.rowCount()>0)
    self.Drive_rod.setEnabled(self.Rod.rowCount()>0)
    self.Drive_rod_activated.setEnabled(self.Rod.rowCount()>0)
    #Others
    self.action_Output_to_Solvespace.setEnabled(self.Entiteis_Link.rowCount()>0 or self.Entiteis_Chain.rowCount()>0)
    self.action_DXF_2D_models.setEnabled(self.Entiteis_Link.rowCount()>0 or self.Entiteis_Chain.rowCount()>0)
    self.action_Replace_Point.setEnabled(TWO_POINT)
    self.action_point_right_click_menu_replace.setEnabled(TWO_POINT)
    self.action_Batch_moving.setEnabled(TWO_POINT)

def showUndoWindow(self, FileState):
    self.undoView = QUndoView(FileState)
    self.undoView.setEmptyLabel("~ Start Pyslvs")
    self.UndoRedoLayout.addWidget(self.undoView)
    separator = QAction(self)
    separator.setSeparator(True)
    self.menu_Edit.insertAction(self.action_Search_Points, separator)
    self.action_Redo = FileState.createRedoAction(self, 'Redo')
    self.action_Undo = FileState.createUndoAction(self, 'Undo')
    self.action_Redo.setShortcut("Ctrl+Shift+Z")
    self.action_Redo.setStatusTip("Backtracking undo action.")
    self.action_Redo.setIcon(QIcon(QPixmap(":/icons/redo.png")))
    self.action_Undo.setShortcut("Ctrl+Z")
    self.action_Undo.setStatusTip("Recover last action.")
    self.action_Undo.setIcon(QIcon(QPixmap(":/icons/undo.png")))
    self.menu_Edit.insertAction(separator, self.action_Undo)
    self.menu_Edit.insertAction(separator, self.action_Redo)

class BaseTableWidget(QTableWidget):
    def __init__(self, RowCount, HorizontalHeaderItems, parent=None):
        super(BaseTableWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setRowCount(RowCount)
        self.setColumnCount(len(HorizontalHeaderItems)+1)
        for i, e in enumerate(['Name']+HorizontalHeaderItems):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(e))

class PointTableWidget(BaseTableWidget):
    def __init__(self, parent=None):
        super(PointTableWidget, self).__init__(1, ['X', 'Y', 'Fixed', 'Color', 'Current'], parent)
        self.setVerticalHeaderItem(0, QTableWidgetItem('Origin'))
        for i, e in enumerate(['Point0', '0.0', '0.0', '', 'Red', "(0.0, 0.0)"]):
            item = QTableWidgetItem(e)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i==3:
                item.setCheckState(Qt.Checked)
            if i==4:
                item.setIcon(colorIcons()['Red'])
            self.setItem(0, i, item)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 40)
        self.setColumnWidth(4, 90)
        self.setColumnWidth(5, 60)
        self.draged = False
    
    def mousePressEvent(self, event):
        super(PointTableWidget, self).mousePressEvent(event)
        if event.button()==Qt.LeftButton:
            self.draged = True
    
    def mouseReleaseEvent(self, event):
        super(PointTableWidget, self).mouseReleaseEvent(event)
        self.draged = False
    
    def mouseMoveEvent(self, event):
        if self.draged:
            drag = QDrag(self)
            mimeData = QMimeData()
            a = list()
            for r in self.selectedRanges():
                a += [str(i) for i in range(r.topRow(), r.bottomRow()+1)]
            mimeData.setText(';'.join(set(a)))
            drag.setMimeData(mimeData)
            drag.exec_()

class DropTableWidget(BaseTableWidget):
    def __init__(self, RowCount, HorizontalHeaderItems, parent=None):
        super(DropTableWidget, self).__init__(RowCount, HorizontalHeaderItems, parent)
        self.setAcceptDrops(True)
    
    def dragMoveEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        event.accept()

class LinkTableWidget(DropTableWidget):
    def __init__(self, parent=None):
        super(LinkTableWidget, self).__init__(0, ["Start Side", "End Side", "Length"], parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 60)
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasText():
            if len(mimeData.text().split(';'))==2:
                event.acceptProposedAction()
            else:
                event.ignore()
    
    def dropEvent(self, event):
        index = [int(e) for e in event.mimeData().text().split(';')]
        print(index)
        event.acceptProposedAction()

class ChainTableWidget(DropTableWidget):
    def __init__(self, parent=None):
        super(ChainTableWidget, self).__init__(0, ['Point[1]', 'Point[2]', 'Point[3]', '[1]-[2]', '[2]-[3]', '[1]-[3]'], parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 60)
        self.setColumnWidth(6, 60)
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasText():
            if len(mimeData.text().split(';'))==3:
                event.acceptProposedAction()
            else:
                event.ignore()
    
    def dropEvent(self, event):
        index = [int(e) for e in event.mimeData().text().split(';')]
        print(index)
        event.acceptProposedAction()
