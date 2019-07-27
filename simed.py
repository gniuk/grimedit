#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Copyright 2019 by gniuk. All rights reserved.
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

class Simed(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600,600)
        self.setWindowTitle("simed")
        self.show()

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape or e.key() == Qt.Key_Q):
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    simed = Simed()
    sys.exit(app.exec_())
