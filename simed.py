#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Copyright 2019 by gniuk. All rights reserved.
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap

class Simed(QWidget):

    def __init__(self, image_path=None, image_content=None):
        if image_path==None and image_content==None:
            print("No image input. Exit.")
            sys.exit(1)
        super().__init__()
        self.initUI(image_path, image_content)

    def initUI(self, image_path, image_content):
        label = QLabel(self)
        if image_path:
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap()
            pixmap.loadFromData(image_content)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        self.setWindowTitle("simed")
        self.show()

    def keyPressEvent(self, e):
        """Override the default key press event handler.
        """
        if (e.key() == Qt.Key_Escape or e.key() == Qt.Key_Q):
            self.close()

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
