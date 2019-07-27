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
        pixmap = QPixmap(image_path)
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
    # app = QApplication(sys.argv)
    app = QApplication([])
    # simed = Simed('./sample.png')
    simed = Simed(sys.argv[1])
    sys.exit(app.exec_())
