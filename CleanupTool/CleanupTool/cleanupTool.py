# coding:utf-8

from PySide import QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pymel.all as pm

class CleanUpUI(MayaQWidgetDockableMixin, QtGui.QDialog):
    def __init__(self, parent=None):
        super(CleanUpUI, self).__init__(parent)
        self.setWindowTitle('Clean up tool')
        self.setFixedWidth(400)
        
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
        
        scroll_area = QtGui.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(scroll_area)
        
        main_widget   = QtGui.QWidget()
        widget_layout = QtGui.QVBoxLayout()
        widget_layout.setContentsMargins(0,0,0,0)
        widget_layout.setAlignment(QtCore.Qt.AlignTop)
        main_widget.setLayout(widget_layout)
        scroll_area.setWidget(main_widget)
        
        interpWidget = CleanUpWidget()
        
        widget_layout.addWidget(interpWidget)

class CleanUpWidget(QtGui.QFrame):
    def __init__(self):
        super(CleanUpWidget, self).__init__()
        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        
        # Window
        self.setWindowTitle('CleanUp Widget')
        #self.setFixedHeight(400)
        
        # Layout
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(5)
        
        #
        self.result = QtGui.QTextEdit()
        self.result.setReadOnly(True)
        bttnLayout = QtGui.QHBoxLayout()
        self.resetBttn = QtGui.QPushButton('Reset')
        self.bttn = QtGui.QPushButton('Clean Up')
        bttnLayout.addWidget(self.resetBttn)
        bttnLayout.addWidget(self.bttn)
        layout.addWidget(self.result)
        layout.addLayout(bttnLayout)
        
        self.bttn.clicked.connect(self.cleanUp)
        self.resetBttn.clicked.connect(self.reset)
        
    def reset(self):
        self.result.clear()
        
    def cleanUp(self):
        green = QtGui.QColor(123,252,0)
        red   = QtGui.QColor(255,0,0)
        
        ref = pm.ls(referencedNodes=True)
        if ref:
            self.reset()
            self.result.setFontPointSize(8)
            self.result.setTextColor(red)
            self.result.append('Reference node exists in the scene.')
            return
        
        self.result.clear()
        self.result.setFontPointSize(12)
        self.result.setTextColor(green)
        self.result.append('Start clean up.')
        
        # Unknown Node
        self.result.setFontPointSize(12)
        self.result.setTextColor(green)
        self.result.append('\n[Unknown Node]')
        unknownNodes = pm.ls(type='unknown')
        if unknownNodes:
            for unknown in unknownNodes:
                try:
                    unknown.unlock()
                    pm.delete(unknown)
                    self.result.setFontPointSize(8)
                    self.result.setTextColor(green)
                    self.result.append('Removed {}.'.format(unknown.name()))
                except:
                    self.result.setFontPointSize(8)
                    self.result.setTextColor(red)
                    self.result.append('Remove failed {}.'.format(unknown.name()))
        
        # Unused Plugin
        self.result.setFontPointSize(12)
        self.result.setTextColor(green)
        self.result.append('\n[Unknown Plugin]')
        oldplugins = pm.unknownPlugin(q=True, list=True)
        if oldplugins:
            for plugin in oldplugins:
                try:
                    pm.unknownPlugin(plugin, remove=True)
                    self.result.setFontPointSize(8)
                    self.result.setTextColor(green)
                    self.result.append('Removed {}.'.format(plugin))
                except:
                    self.result.setFontPointSize(8)
                    self.result.setTextColor(red)
                    self.result.append('Remove failed {}.'.format(plugin))
        
        # Turtle
        self.result.setFontPointSize(12)
        self.result.setTextColor(green)
        self.result.append('\n[Turtle]')
        try:
            turtleNodes = pm.ls('Turtle*')
            if turtleNodes:
                for node in turtleNodes:
                    node.unlock()
                    pm.delete( node )
                    self.result.setFontPointSize(8)
                    self.result.setTextColor(green)
                    self.result.append('Removed {}.'.format(node))
            pm.unloadPlugin('Turtle.mll', f=True)
        except:
            self.result.setFontPointSize(8)
            self.result.setTextColor(red)
            self.result.append('Remove failed {}.'.format('Turtle'))
    
        # Fur
        self.result.setFontPointSize(12)
        self.result.setTextColor(green)
        self.result.append('\n[Fur]')
        try:
            pm.unloadPlugin('Fur.mll', f=True)
        except:
            pass
        
        self.result.setFontPointSize(12)
        self.result.setTextColor(green)
        self.result.append('\nFinished.')
        
        # Optimize
        #pm.mel.eval('scOpt_performOneCleanup({"deformerOption", "unusedSkinInfsOption", "groupIDnOption", "shaderOption", "ptConOption", "pbOption", "snapshotOption", "unitConversionOption", "brushOption", "referencedOption", "unknownNodesOption", "shadingNetworksOption"});')
        #pm.mel.eval("cleanUpScene 3")
                
def main(dockable=False):
    global dialog

    try:
        dialog.close()
        dialog.deleteLater()
    except: 
        pass
    
    dialog = CleanUpUI()
    
    if dockable:
        dialog.show(dockable=dockable, area='right', floating=False)
    else:
        dialog.show()

