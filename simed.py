#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Copyright 2019 by gniuk. All rights reserved.
"""

import os
import sys
import time
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen
# import ToolPanel
from PyQt5.QtWidgets import QHBoxLayout, QToolButton
from PyQt5.QtGui import QIcon, QScreen
from PyQt5.QtCore import QSize

# class Simed(QMainWindow):
class Simed(QWidget):

    def __init__(self, image_path=None, image_content=None, phyScrH=1080):
        if image_path==None and image_content==None:
            print("No image input. Exit.")
            sys.exit(1)
        super().__init__()
        self.initUI(image_path, image_content, phyScrH)
        self.initStatus()
        self.initPanelUI()

    def initUI(self, image_path, image_content, phyScrH):
        self.imgLabel = QLabel(self) # we don't need this label. what lable actually is? But: QLabel is used for displaying text or an image.
        if image_path:
            self.pixmap = QPixmap(image_path)
        else:
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(image_content)
        # self.resize(self.pixmap.width(),self.pixmap.height())
        if self.pixmap.height() + 35 > phyScrH:
            self.resize(self.pixmap.width(),self.pixmap.height())
        else:
            self.resize(self.pixmap.width(),self.pixmap.height()+35)
        # self.imgLabel.setPixmap(self.pixmap)

        self.setWindowTitle("simed")
        self.show()

    def initPanelUI(self):
        self.g_toolPanel = ToolPanel(self)
        self.g_toolPanel.setGeometry(self.rect().right()-359, self.rect().bottom()-35, 350, 35)
        self.g_toolPanel.resize(359, self.g_toolPanel.height())
        self.g_toolPanel.setParent(self)
        self.g_toolPanel.show()

    def initStatus(self):
        self.g_mousePressed = False
        self.g_mouseReleased = True
        self.g_drawStarted = False
        self.g_selectedTool = None
        self.g_drawShapeView = {
                              None: self.g_drawNoneView,
                              'Line': self.g_drawLineView,
                              'Rec': self.g_drawRecView,
                              'Elli': self.g_drawElliView
                             }
        self.g_drawShapePixmap = {
                                'Line': self.g_drawLinePixmap,
                                'Rec': self.g_drawRecPixmap,
                                'Elli': self.g_drawElliPixmap
                               }
        self.g_penStyle = QPen(Qt.red, 4)
        self.g_undoStack = []     # push pixmap snapshot into stack before a drawing on current pixmap

    def g_drawNoneView(self, painter):
        painter.setPen(self.g_penStyle)
        painter.drawPixmap(self.pixmap.rect(), self.pixmap)

    def g_drawLineView(self, painter):
        """Draw on mainwindow Widget, it is fake drawing, just for viewing.
        """
        painter.setPen(self.g_penStyle)
        painter.drawPixmap(self.pixmap.rect(), self.pixmap)
        if self.g_mousePressed:
            painter.drawLine(self.startX,self.startY, self.endX,self.endY)

    def g_drawLinePixmap(self):
        """Draw on pixmap, do real pixel modify.
        """
        painter = QPainter(self.pixmap) # draw on pixmap
        painter.setPen(self.g_penStyle)
        painter.drawLine(self.startX,self.startY, self.endX,self.endY)
        painter.end()
        self.update()

    def g_drawRecView(self,painter):
        painter.setPen(self.g_penStyle)
        painter.drawPixmap(self.pixmap.rect(), self.pixmap)
        if self.g_mousePressed:
            painter.drawRect(self.startX,self.startY, self.endX-self.startX,self.endY-self.startY)

    def g_drawRecPixmap(self):
        painter = QPainter(self.pixmap) # draw on pixmap
        painter.setPen(self.g_penStyle)
        painter.drawRect(self.startX,self.startY, self.endX-self.startX,self.endY-self.startY)
        painter.end()
        self.update()

    def g_drawElliView(self,painter):
        painter.setPen(self.g_penStyle)
        painter.drawPixmap(self.pixmap.rect(), self.pixmap)
        if self.g_mousePressed:
            painter.drawEllipse(self.startX,self.startY, self.endX-self.startX,self.endY-self.startY)

    def g_drawElliPixmap(self):
        painter = QPainter(self.pixmap) # draw on pixmap
        painter.setPen(self.g_penStyle)
        painter.drawEllipse(self.startX,self.startY, self.endX-self.startX,self.endY-self.startY)
        painter.end()
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        self.g_drawShapeView[self.g_selectedTool](painter)
        painter.end()

    def keyPressEvent(self, e):
        """Override the default key press event handler.
        """
        # print(dir(e))
        if e.key() == Qt.Key_Escape:
            # self.g_saveWithClipboard()
            self.g_quit()
        if e.modifiers() & Qt.ControlModifier:
            if e.key() == Qt.Key_Z:
                self.g_undoDraw()

    def g_undoDraw(self):
        if self.g_undoStack:
            self.pixmap = self.g_undoStack.pop()
            print("old pixmap at: {}".format(self.pixmap))
            self.update()

    def g_saveWithClipboard(self):
        picDir = os.path.expanduser('~') + '/Picture'
        try:
            # Maybe the best compatibility :)
            os.mkdir(picDir)
        except:
            pass
        screentShotDir = picDir + '/ScreenShot'
        try:
            os.mkdir(screentShotDir)
        except:
            pass
        pic = "".join([screentShotDir, '/', time.strftime("%Y%m%d-%H-%M-%S"), '.png'])
        self.pixmap.save(pic, 'PNG')
        with open(pic, 'rb') as f:
            subprocess.Popen(['wl-copy'], stdin=f)
        self.g_quit()

    def g_quit(self):
        self.g_toolPanel.close()
        self.close()

    def mousePressEvent(self, e):
        print(type(e))
        self.startX = e.x()
        self.startY = e.y()
        print(self.startX, self.startY)
        self.g_mousePressed = True
        # if self.g_selectedTool == 1:

    def mouseReleaseEvent(self, e):
        self.endX = e.x()
        self.endY = e.y()
        self.g_mousePressed = False

        # save the pixmap snapshot for undo
        if self.g_selectedTool:
            if self.endX != self.startX and self.endY != self.startY:
                self.g_undoStack.append(QPixmap(self.pixmap))
                print("modified pixmap at {}, size = {} Bytes".format(self.pixmap, self.pixmap.__sizeof__()))
                self.g_drawShapePixmap[self.g_selectedTool]()
    def mouseMoveEvent(self, e):
        # print(dir(e))
        self.endX = e.x(); self.endY = e.y()
        print("mousebuttonpress:{},{}".format(e.MouseButtonPress, type(e.MouseButtonPress)))
        if self.g_mousePressed:
            print(type(e),type(e.MouseButtonPress))
            self.update()

    def g_selectRect(self):
        self.g_selectedTool = 'Rec'
        print("Rectangle Tool selected")

    def g_selectLine(self):
        self.g_selectedTool = 'Line'
        print("Line Tool selected")

    def g_selectEllipse(self):
        self.g_selectedTool = 'Elli'
        print("Ellipse Tool selected")



class ToolPanel(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mWindow = mainWindow
        self.initToolLayout()

    def initToolLayout(self):
        self.rectBtn = QToolButton(self)
        self.rectBtn.setIcon(QIcon('images/rect.png'))
        self.rectBtn.setFixedSize(35,35)
        self.rectBtn.setIconSize(QSize(22,22))
        self.rectBtn.clicked.connect(self.mWindow.g_selectRect)
        self.elliBtn = QToolButton(self)
        self.elliBtn.setIcon(QIcon('images/ellipse.png'))
        self.elliBtn.setFixedSize(35,35)
        self.elliBtn.setIconSize(QSize(23,23))
        self.elliBtn.clicked.connect(self.mWindow.g_selectEllipse)
        self.lineBtn = QToolButton(self)
        self.lineBtn.setIcon(QIcon('images/arrow.png'))
        self.lineBtn.setFixedSize(35,35)
        self.lineBtn.setIconSize(QSize(22,22))
        self.lineBtn.clicked.connect(self.mWindow.g_selectLine)

        self.brushBtn = QToolButton(self)
        self.brushBtn.setIcon(QIcon('images/brush.png'))
        self.brushBtn.setFixedSize(35,35)
        self.brushBtn.setIconSize(QSize(24,24))
        self.mosaicBtn = QToolButton(self)
        self.mosaicBtn.setIcon(QIcon('images/mosaic.png'))
        self.mosaicBtn.setFixedSize(35,35)
        self.mosaicBtn.setIconSize(QSize(22,22))
        self.textBtn = QToolButton(self)
        self.textBtn.setIcon(QIcon('images/text.png'))
        self.textBtn.setFixedSize(35,35)
        self.textBtn.setIconSize(QSize(22,22))
        self.undoBtn = QToolButton(self)
        self.undoBtn.setIcon(QIcon('images/undo.png'))
        self.undoBtn.setFixedSize(35,35)
        self.undoBtn.setIconSize(QSize(23,23))
        self.undoBtn.clicked.connect(self.mWindow.g_undoDraw)
        self.saveBtn = QToolButton(self)
        self.saveBtn.setIcon(QIcon('images/save.png'))
        self.saveBtn.setFixedSize(35,35)
        self.saveBtn.setIconSize(QSize(22,22))
        self.saveBtn.clicked.connect(self.mWindow.g_saveWithClipboard)
        self.cancelBtn = QToolButton(self)
        self.cancelBtn.setIcon(QIcon('images/cancel.png'))
        self.cancelBtn.setFixedSize(35,35)
        self.cancelBtn.setIconSize(QSize(22,22))
        self.cancelBtn.clicked.connect(self.mWindow.g_quit)
        self.finishBtn = QToolButton(self)
        self.finishBtn.setIcon(QIcon('images/finish.png'))
        self.finishBtn.setFixedSize(35,35)
        self.finishBtn.setIconSize(QSize(25,23))
        self.finishBtn.clicked.connect(self.mWindow.g_saveWithClipboard)

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.rectBtn)
        self.hLayout.addWidget(self.elliBtn)
        self.hLayout.addWidget(self.lineBtn)
        self.hLayout.addWidget(self.brushBtn)
        self.hLayout.addWidget(self.mosaicBtn)
        self.hLayout.addWidget(self.textBtn)
        self.hLayout.addWidget(self.undoBtn)
        self.hLayout.addWidget(self.saveBtn)
        self.hLayout.addWidget(self.cancelBtn)
        self.hLayout.addWidget(self.finishBtn)
        self.hLayout.setSpacing(1)
        self.hLayout.setContentsMargins(0,0,0,0)

        self.setLayout(self.hLayout)


if __name__ == '__main__':
    app = QApplication([])
    phyScreenHeight = app.primaryScreen().size().height()
    print("phyScreenHeight: {}".format(phyScreenHeight))

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        image_content = None
    else:
        image_path = None
        with open(0, 'rb') as f:
            image_content = f.read()
            if not image_content:
                sys.exit(1)
    simed = Simed(image_path, image_content, phyScreenHeight)
    sys.exit(app.exec_())
