# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ADREMToolDialog
                                 A QGIS plugin
 No desrciption yet
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-02-05
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Louis- FULL 2021
        email                : louis.andrianaivo@polito.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QFileInfo
from qgis.PyQt.QtWidgets import QDialog, QMessageBox, QFileDialog

from .utility import myCSV

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'adrem_tool_dialog_base.ui'))


class ADREMToolDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ADREMToolDialog, self).__init__(parent)
        self.setupUi(self)
        ###########################################################################################
        # filters
        ###########################################################################################
        self.mainView.setFilter("DXF Files (*.dxf)")
        self.boundary_shp.setFilter("SHape Files (*.shp)")
        self.residentialShape.setFilter("Shapes Files (*.shp)")
        self.industrialShape.setFilter("Shapes Files (*.shp)")

        self.shallow_csv.setFilter("CSV Files (*.csv)")
        self.deep_csv.setFilter("CSV Files (*.csv)")
        self.aquifer_csv.setFilter("CSV Files (*.csv)")
        
        self.hide_widget_page_1()

        ###########################################################################################
        self.update_prev_next_buttons()
        self.stackedWidget.currentChanged.connect(self.update_prev_next_buttons)
        self.pushButtonNext.clicked.connect(self.__next__)
        self.pushButtonPrevious.clicked.connect(self.prev)
        self.outputDirtoolButton.clicked.connect(self.select_directory)
        self.outputDir.setText('')
        self.pushButtonNext.setFocus()
        ############################################################################################
    def hide_widget_page_1(self):
        ################################################################################
        ## hides the widgets ###########################################################
        ################################################################################
        
        self.widgetAquifer.hide()
        self.widgetDeep.hide()
        self.widgetShallow.hide()

    def update_prev_next_buttons(self):
        i = self.stackedWidget.currentIndex()
        self.pushButtonPrevious.setEnabled( i > 0)

    def __next__(self):
        i = self.stackedWidget.currentIndex()
        if i < 3:
            if i==0:
                ok = self.validate_inputs()
            if i==1:
                ok = self.validate_page_1()
            elif i==2:
                ok = self.validate_output()
            if ok == True:
                if i < 2:
                    self.stackedWidget.setCurrentIndex(i + 1)
                    if i == 1:
                        self.pushButtonNext.setText('Submit')
                else:
                    self.accept()
    
    def prev(self):
        i = self.stackedWidget.currentIndex()
        if i == 1:
            self.hide_widget_page_1()
        self.stackedWidget.setCurrentIndex(i - 1)
        if i != 2:
            self.pushButtonNext.setText('Next>')
        
            
    def select_directory(self):
        path = QFileDialog.getExistingDirectory(
            self,
            'Select the Directory fro your Plugin',
            ''
        )
        self.outputDir.setText(path)

    def validate_inputs(self):
        self.filename_mainView = self.mainView.filePath()
        self.filename_boundary_shp = self.boundary_shp.filePath()
        ### compulsory fields
        if self.filename_mainView == "" or \
            self.filename_boundary_shp == "":
            msg = (' Main View and Boundary are required')
            QMessageBox.warning(
                self, ' Invalid fields ',
                msg
            )
            return False

        self.filename_residentialShape = self.residentialShape.filePath()
        self.filename_industrialShape = self.industrialShape.filePath()
        ## at least one of this 
        if self.filename_residentialShape == "" and \
            self.filename_industrialShape == "":
            msg = (' At least one Area must be given')
            QMessageBox.warning(
                self, ' Invalid fields ',
                msg
            )
            return False

        self.filename_shallow_csv = self.shallow_csv.filePath()
        self.filename_deep_csv = self.deep_csv.filePath()
        self.filename_aquifer_csv = self.aquifer_csv.filePath()
        #print(self.filename_aquifier_csv)
        if self.filename_shallow_csv == "" and \
            self.filename_aquifer_csv == "" and \
            self.filename_deep_csv == "":
            msg = (' At least one must be given')
            QMessageBox.warning(
                self, ' Invalid fields ',
                msg
            )
            return False

        # delimiter
        self.del_sha_csv = self.delimiterShallowcomboBox.currentText()
        #QgsMessageLog.logMessage('Debug : delimiter for shallow {}'.format(self.del_sha_csv))
        self.del_deep_csv = self.delimiterDeepcomboBox.currentText()
        #QgsMessageLog.logMessage('Debug : delimiter for deep {}'.format(self.del_deep_csv))
        self.del_aqui_csv = self.delimiterAquifercomboBox.currentText()
        #QgsMessageLog.logMessage('Debug : delimiter for aquifer {}'.format(self.del_aqui_csv))
        if (self.filename_shallow_csv):
            shallow__ = myCSV(path=self.filename_shallow_csv,delimiter=self.del_sha_csv)
            self.shallow_combo = shallow__.getheader()
            if len(self.shallow_combo) < 4:
                msg = ('Not enough fields, verify your files\n as well as the delimiter\n{}'.format(self.filename_shallow_csv))
                QMessageBox.warning(
                    self, ' Invalid CSV or delimiter ',
                    msg
                )
                return False
            else:
                self.widgetShallow.show()
                # populate combobox
                self.shallowXcomboBox.clear()
                self.shallowXcomboBox.addItems(self.shallow_combo)
                self.shallowYcomboBox.clear()
                self.shallowYcomboBox.addItems(self.shallow_combo)

        if (self.filename_deep_csv):
            deep__ = myCSV(path=self.filename_deep_csv,delimiter=self.del_deep_csv)
            self.deep_combo = deep__.getheader()
            if len(self.deep_combo) < 4:
                msg = ('Not enough fields, verify your files\n as well as the delimiter\n{}'.format(self.filename_deep_csv))
                QMessageBox.warning(
                    self, ' Invalid CSV or delimiter ',
                    msg
                )
                return False
            else:
                self.widgetDeep.show()
                # populate combobox
                self.deepXcomboBox.clear()
                self.deepXcomboBox.addItems(self.deep_combo)
                self.deepYcomboBox.clear()
                self.deepYcomboBox.addItems(self.deep_combo)

        if (self.filename_aquifer_csv):
            aquifer__ = myCSV(path=self.filename_aquifer_csv,delimiter=self.del_aqui_csv)
            self.aquifer_combo = aquifer__.getheader()
            if len(self.aquifer_combo) < 4:
                msg = ('Not enough fields, verify your files\n as well as the delimiter\n{}'.format(self.filename_aquifer_csv))
                QMessageBox.warning(
                    self, ' Invalid CSV or delimiter ',
                    msg
                )
                return False
            else:
                self.widgetAquifer.show()
                # populate the combobox
                self.aquiferXcomboBox.clear()
                self.aquiferXcomboBox.addItems(self.aquifer_combo)
                self.aquiferYcomboBox.clear()
                self.aquiferYcomboBox.addItems(self.aquifer_combo)
                
        return True

    def validate_page_1(self):
        if self.filename_shallow_csv:
            if self.shallowXcomboBox.currentIndex() == self.shallowYcomboBox.currentIndex():
                msg = ("The coordinates cant be in the same column\n Please verify carefuly")
                QMessageBox.warning(
                    self, ' Invalid selection (shallow soil) ',
                msg
                )
                return False
            else:
                self._sha_x = self.shallowXcomboBox.currentText()
                self._sha_y = self.shallowYcomboBox.currentText()
        if self.filename_deep_csv:
            if self.deepXcomboBox.currentIndex() == self.deepYcomboBox.currentIndex():
                msg = ("The coordinates cant be in the same column\n Please verify carefuly")
                QMessageBox.warning(
                    self, ' Invalid selection (deep soil)',
                msg
                )
                return False
            else:
                self._deep_x = self.deepXcomboBox.currentText()
                self._deep_y = self.deepYcomboBox.currentText()
        if self.filename_aquifer_csv:
            if self.aquiferXcomboBox.currentIndex() == self.aquiferYcomboBox.currentIndex():
                msg = ("The coordinates cant be in the same column\n Please verify carefuly")
                QMessageBox.warning(
                    self, ' Invalid selection (aquifer) ',
                msg
                )
                return False
            else:
                self._aqui_x = self.aquiferXcomboBox.currentText()
                self._aqui_y = self.aquiferYcomboBox.currentText()
        return True

    def validate_output(self):
        good_dir = False
        if len(self.outputDir.text()) > 0:
            if QFileInfo(self.outputDir.text()).exists():
                if QFileInfo(self.outputDir.text()).isWritable():
                    good_dir = True
                else:
                    msg = "Output Directory is write-protected."
            else:
                msg = "Directory does not exists."
        else:
            msg = "Plese slect an output directory."
        if not good_dir:
            QMessageBox.warning(
                self,
                'Error',
                msg
            )
        return good_dir

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            pass
