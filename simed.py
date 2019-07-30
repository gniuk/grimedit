#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Copyright 2019 by gniuk. All rights reserved.
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen

# class Simed(QMainWindow):
class Simed(QWidget):

    def __init__(self, image_path=None, image_content=None):
        if image_path==None and image_content==None:
            print("No image input. Exit.")
            sys.exit(1)
        super().__init__()
        self.initUI(image_path, image_content)
        self.initStatus()

    def initUI(self, image_path, image_content):
        self.imgLabel = QLabel(self) # we don't need this label. what lable actually is? But: QLabel is used for displaying text or an image.
        if image_path:
            self.pixmap = QPixmap(image_path)
        else:
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(image_content)
        self.resize(self.pixmap.width(),self.pixmap.height())
        # self.resize(600,600)
        # self.imgLabel.setPixmap(self.pixmap)

        self.setWindowTitle("simed")
        self.show()

    def initStatus(self):
        # self.painter = QPainter(self.pixmap)
        self.mousePressed = False # contained in event. maybe not needed
        self.mouseReleased = True
        self.drawStarted = False
        self.selectedTool = None

        # now try to paint
        # self.paint(self)
    def paintEvent(self, e):
        # need a new painter each time
        print("Paint?")
        # self.painter.begin(self) # what is begin?
        painter = QPainter(self) # draw on widget just for animate drawing
        # painter = self.painter
        # painter.begin(self)
        painter.drawPixmap(self.pixmap.rect(), self.pixmap) # if I draw, then I don't need label to show?
        print("what is self.rect(): {}, {}".format(self.rect(), dir(self.rect)))
        # if (ev.MouseButtonPress):
        if self.mousePressed:
            # painter.drawPixmap(self.rect(), self.pixmap)
            # painter.setPen(QPen(Qt.red, 4, Qt.DashDotLine))
            painter.setPen(QPen(Qt.red, 4))
            # painter.drawRect(40,40,400,200)
            painter.drawRect(self.startX,self.startY, self.endX-self.startX,self.endY-self.startY)
            # painter.drawPixmap(self.rect(), self.pixmap)
        painter.end()

    def keyPressEvent(self, e):
        """Override the default key press event handler.
        """
        if e.key() == Qt.Key_Escape:
            # save the image to file for debugging
            self.pixmap.save("/tmp/fordebug.png", "PNG")
            # self.grab().save("/tmp/fordebug.png", "PNG")
            self.close()

    def mousePressEvent(self, e):
        print(type(e))
        # print(dir(e))
        self.startX = e.x()
        self.startY = e.y()
        print(self.startX, self.startY)
        # print(e.DragEnter)
        self.mousePressed = True
        # if self.selectedTool == 1:

    def mouseReleaseEvent(self, e):
        self.endX = e.x()
        self.endY = e.y()
        print(self.endX, self.endY)
        self.mousePressed = False
        # save the previous lines or rects here to redraw in the paintEvent?
        # self.prevDraw.append(self.mRect)
        painter = QPainter(self.pixmap) # do the pixmap change! Maybe use stack to save state for undo.
        painter.setPen(QPen(Qt.red, 4))
        painter.drawRect(self.startX,self.startY, self.endX-self.startX,self.endY-self.startY)
        painter.end()
        self.update() # BAD, rect disappear on widget. But the pixmap changed, so not matter.
    def mouseMoveEvent(self, e):
        # print(dir(e))
        x = e.x()
        y = e.y()
        self.endX = x; self.endY = y
        print("x: {}, y: {}".format(x, y))
        print("mousebuttonpress:{},{}".format(e.MouseButtonPress, type(e.MouseButtonPress)))
        # if (e.MouseButtonPress):
        if self.mousePressed:
            # print("mousebuttonpress:{},{}".format(e.MouseButtonPress, type(e.MouseButtonPress)))
            print(type(e),type(e.MouseButtonPress))
            print("origin: ({}, {})".format(x, y))
            self.update()

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
