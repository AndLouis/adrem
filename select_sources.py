import os

from qgis.PyQt import (QtGui, QtWidgets, uic)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'select_sources_base.ui')
    )

class SelectSourceDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(SelectSourceDialog, self).__init__(parent)
        self.setupUi(self)

