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
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect

# class Simed(QMainWindow):
class Simed(QWidget):

    def __init__(self, image_path=None, image_content=None):
        if image_path==None and image_content==None:
            print("No image input. Exit.")
            sys.exit(1)
        super().__init__()
        self.initUI(image_path, image_content)
        self.initStatus()
        self.initPanelUI()

    def initUI(self, image_path, image_content):
        self.imgLabel = QLabel(self) # we don't need this label. what lable actually is? But: QLabel is used for displaying text or an image.
        if image_path:
            self.pixmap = QPixmap(image_path)
        else:
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(image_content)
        self.resize(self.pixmap.width(),self.pixmap.height())
        # self.imgLabel.setPixmap(self.pixmap)

        self.setWindowTitle("simed")
        self.show()

    def initPanelUI(self):
        self.g_toolPanel = ToolPanel(self)
        # self.g_toolPanel.setGeometry(500,500,600,600)
        self.hLayout = QHBoxLayout(self)
        self.hLayout.addWidget(self.g_toolPanel)
        self.hLayout.setContentsMargins(0,0,0,0)
        self.g_toolPanel.setObjectName("ToolPanel")
        self.g_toolPanel.setStyleSheet("QWidget#control{background-color: #eaecf0;}")

        self.g_toolPanel.setGeometry(self.rect().right()-543, self.rect().bottom()-6, 543, 25)
        self.g_toolPanel.show()

    def initStatus(self):
        self.g_mousePressed = False # contained in event. maybe not needed
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
            # save the image to file for debugging
            # self.pixmap.save("/tmp/fordebug.png", "PNG")
            # self.grab().save("/tmp/fordebug.png", "PNG")
            self.g_saveWithClipboard()
            self.g_toolPanel.close()
            self.close()
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
        self.rectBtn.setIcon(QIcon('images/rect.jpg'))
        self.rectBtn.setFixedSize(30,30)
        self.rectBtn.clicked.connect(self.mWindow.g_selectRect)
        self.lineBtn = QToolButton(self)
        self.lineBtn.setIcon(QIcon('images/line.jpg'))
        self.lineBtn.setFixedSize(30,30)
        self.lineBtn.clicked.connect(self.mWindow.g_selectLine)
        self.elliBtn = QToolButton(self)
        self.elliBtn.setIcon(QIcon('images/elli.jpg'))
        self.elliBtn.setFixedSize(30,30)
        self.elliBtn.clicked.connect(self.mWindow.g_selectEllipse)
        self.hLayout = QHBoxLayout(self)
        self.hLayout.addWidget(self.rectBtn)
        self.hLayout.addWidget(self.lineBtn)
        self.hLayout.addWidget(self.elliBtn)
        # self.hLayout.addStretch(1)
        self.hLayout.setSpacing(1)
        self.hLayout.setContentsMargins(0,0,0,0)

        self.setLayout(self.hLayout)


if __name__ == '__main__':
    app = QApplication([])

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        image_content = None
    else:
        image_path = None
        with open(0, 'rb') as f:
            image_content = f.read()
    simed = Simed(image_path, image_content)
    sys.exit(app.exec_())
