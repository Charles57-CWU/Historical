"""
GUI_APP.py is the main executable and holds information related to the main window

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""
import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
import pandas as pd

# assistant classes
import COLORS
import WARNINGS
# dataset information
import DATA

# plot information
import MAINPLOT


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # load Ui from ui File made in QTDesigner
        super(Ui, self).__init__()
        uic.loadUi('visualizationGui.ui', self)

        # general variables
        self.dataset = None
        self.plot_type = None
        self.plot_layout = None
        self.class_table = None
        self.warnings = WARNINGS.getWarning()
        self.colors = COLORS.getColors()
        self.class_count = None
        self.feature_count = None
        self.sample_count = None
        self.count_per_class_array = None
        self.dataframe = None
        self.index_starts = None
        self.vertex_count = None
        self.plot_widget = MAINPLOT.makePlot(0, 0, 0, 0, 0, self.plot_type)

        # exit button
        self.exit_button_pressed = self.findChild(QtWidgets.QPushButton, 'exitButton')
        self.exit_button_pressed.clicked.connect(self.exitApp)

        # generate plot button
        self.plot_button_pressed = self.findChild(QtWidgets.QPushButton, 'makePlotButton')
        self.plot_button_pressed.clicked.connect(self.createPlot)

        # file upload button
        self.upload_button_pressed = self.findChild(QtWidgets.QPushButton, 'uploadButton')
        self.upload_button_pressed.clicked.connect(self.uploadDataset)

        # test button
        self.test_button_pressed = self.findChild(QtWidgets.QPushButton, 'testButton')
        self.test_button_pressed.clicked.connect(self.test)

        # update button
        self.update_plot_button_pressed = self.findChild(QtWidgets.QPushButton, 'updatePlotButton')
        self.update_plot_button_pressed.clicked.connect(self.updatePlot)

        self.show_axes = self.findChild(QtWidgets.QCheckBox, 'axesCheck')

    def test(self):
        print('hi')

    # upload dataset
    def uploadDataset(self):
        #if self.plot_layout:
        #    self.plot_layout.removeWidget(self.plot_widget)
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')

        # file explorer canceled without choosing name
        if filename[0] == '':
            return

        # get data
        self.dataset = DATA.getData(filename[0])
        dataset_name = self.dataset.dataset_name
        self.dataframe = self.dataset.dataframe

        # class information
        self.class_count = self.dataset.class_count
        class_names_array = self.dataset.class_names_array
        self.count_per_class_array = self.dataset.count_per_class_array
        # sample and feature information
        self.sample_count = self.dataset.sample_count
        self.feature_count = self.dataset.feature_count
        feature_names_array = self.dataset.feature_names_array

        # display class data
        class_info_string = ('Dataset Name: ' + dataset_name +
                             '\n\n' + 'Number of Classes: ' + str(self.class_count) +
                             '\n\n' + 'Number of Features: ' + str(self.feature_count) +
                             '\n\n' + 'Number of Samples: ' + str(self.sample_count))

        # loop through class names
        counter = 1
        for ele in class_names_array:
            class_info_string += ('\n\n' + 'Class ' + str(counter) + ' - ' + str(ele) +
                                  '\n' + '--Count: ' + str(self.count_per_class_array[counter - 1]) +
                                  '\n' + '--Color: ' + self.colors.colors_names_array[counter - 1])
            counter += 1

        # print text to box
        class_info = self.findChild(QtWidgets.QTextBrowser, 'datasetInfoBrowser')
        class_info.setText(class_info_string)

        # display feature data
        feature_info_string = ''
        counter = 1
        for ele in feature_names_array:
            feature_info_string += (str('X') + str(counter) + ' - ' + str(ele) + '\n\n')
            counter += 1

        # remove extra \n\n
        feature_info_string = feature_info_string[:len(feature_info_string) - 2]

        # print text to box
        feature_info = self.findChild(QtWidgets.QTextBrowser, 'attributeBrowser')
        feature_info.setText(feature_info_string)

        self.class_table = self.findChild(QtWidgets.QTableWidget, 'classTable')
        self.class_table.setRowCount(self.class_count)
        self.class_table.setColumnCount(1)
        self.class_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Class'))
        header = self.class_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        counter = 0
        for ele in class_names_array:
            class_color_string = str(ele) + ' - (' + self.colors.colors_names_array[counter] + ')'
            item = QtWidgets.QTableWidgetItem(class_color_string)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Checked)
            self.class_table.setItem(counter, 0, item)
            counter += 1

    # exit the app
    def exitApp(self):
        print("Exit pressed")
        self.close()

    # make the plot
    def createPlot(self):
        if self.plot_layout:
            self.plot_layout.removeWidget(self.plot_widget)

        # check for data before generating plot
        if self.dataset == '':
            self.warnings.noDataWarning()
            return

        dic_checked = self.findChild(QtWidgets.QRadioButton, 'dicCheck')
        if dic_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, 'DICP')

        pcp_checked = self.findChild(QtWidgets.QRadioButton, 'pcpCheck')
        if pcp_checked.isChecked():
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, 'PCP')

        ap_checked = self.findChild(QtWidgets.QRadioButton, 'apCheck')
        if ap_checked.isChecked():
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, 'AP')

        acpo_checked = self.findChild(QtWidgets.QRadioButton, 'acpoCheck')
        if acpo_checked.isChecked():
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, 'ACPO')

        spc_checked = self.findChild(QtWidgets.QRadioButton, 'spcCheck')
        if spc_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, 'SPCP')

        glcs_checked = self.findChild(QtWidgets.QRadioButton, 'glcsCheck')
        if glcs_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
           # self.plot_widget = GLCSP.makePlot(self.dataframe, self.class_count, self.feature_count, self.sample_count,
             #                                 self.count_per_class_array)

        glcst_checked = self.findChild(QtWidgets.QRadioButton, 'glcstCheck')
        if glcst_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
            #self.plot_widget = GLCSTP.makePlot(self.dataframe, self.class_count, self.feature_count, self.sample_count,
              #                                 self.count_per_class_array)

        self.plot_layout = self.findChild(QtWidgets.QVBoxLayout, 'plotDisplay')
        self.plot_layout.addWidget(self.plot_widget)

    def updatePlot(self):

        if self.show_axes.checkState() == Qt.CheckState.Unchecked:
            self.plot_widget.plot_axes = False
        else:
            self.plot_widget.plot_axes = True

        classes_to_display = []
        for i in range(self.class_count):
            if self.class_table.item(i, 0).checkState() == Qt.CheckState.Checked:
                classes_to_display.append(1)
            else:
                classes_to_display.append(0)

        current_class_index_starts = np.asarray([])
        current_class_vertex_count = np.asarray([])

        current_sample_count = 0
        counter = 0
        for i in range(self.class_count):
            if classes_to_display[i] == 1:
                current_sample_count += self.count_per_class_array[i]
                current_class_index_starts = np.concatenate((current_class_index_starts,
                                                             self.plot_widget.all_class_index_starts[
                                                             counter:counter + self.count_per_class_array[i]]), axis=0)
                current_class_vertex_count = np.concatenate(
                    (current_class_vertex_count, self.plot_widget.all_class_vertex_count[
                                                 counter:counter +
                                                         self.count_per_class_array[i]]),
                    axis=0)
            counter += self.count_per_class_array[i]

        self.plot_widget.current_class_index_starts = current_class_index_starts
        self.plot_widget.current_class_vertex_count = current_class_vertex_count
        self.plot_widget.current_sample_count = current_sample_count
        self.plot_widget.update()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
