"""
GUI_APP.py is the main executable and holds information related to the main window

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""
import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtGui
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
import SHOW_HIDE_CLASSES


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
        self.feature_table = self.findChild(QtWidgets.QTableWidget, 'featureTable')
        self.warnings = WARNINGS.getWarning()
        self.colors = COLORS.getColors()
        self.class_count = None
        self.feature_count = None
        self.sample_count = None
        self.count_per_class_array = None
        self.class_to_plot = None
        self.dataframe = None
        self.index_starts = None
        self.vertex_count = None
        self.plot_widget = MAINPLOT.makePlot(0, 0, 0, 0, 0, 0, self.plot_type)
        self.feature_table.__class__.dropEvent = self.featureSwap
        self.feature_position_array = None
        self.feature_names_array = None

        self.is_placeholder = True

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
        self.show_markers = self.findChild(QtWidgets.QCheckBox, 'markerCheck')

        self.update_feature_button_pressed = self.findChild(QtWidgets.QPushButton, 'replotFeatureButton')
        self.update_feature_button_pressed.clicked.connect(self.replotFeatures)

    def test(self):
        print('hi')

    # upload dataset
    def uploadDataset(self):
        # if self.plot_layout:
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
        self.class_to_plot = np.repeat(1, self.class_count)
        print(self.class_to_plot)
        class_names_array = self.dataset.class_names_array
        self.count_per_class_array = self.dataset.count_per_class_array
        # sample and feature information
        self.sample_count = self.dataset.sample_count
        self.feature_count = self.dataset.feature_count
        self.feature_names_array = self.dataset.feature_names_array
        self.feature_position_array = np.arange(1, self.feature_count + 1)

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
        feature_info_string = 'Features:\n\n'
        counter = 0
        for ele in self.feature_names_array:
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

        self.feature_table.setRowCount(self.feature_count)
        self.feature_table.setColumnCount(1)
        self.feature_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Feature Order'))
        # table properties
        self.feature_table.setDragEnabled(True)
        self.feature_table.setAcceptDrops(True)
        self.feature_table.setDropIndicatorShown(True)
        self.feature_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # table data
        header = self.feature_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        counter = 0
        for ele in self.feature_names_array:
            item = QtWidgets.QTableWidgetItem(str(ele) + ' - (X' + str(counter) + ')')
            self.feature_table.setItem(counter, 0, item)
            counter += 1

    def featureSwap(self, event):
        moved_from = self.feature_table.currentRow()
        from_item = self.feature_table.item(moved_from, 0).text()
        moved_to = self.feature_table.rowAt(event.pos().y())
        to_item = self.feature_table.item(moved_to, 0).text()

        self.feature_table.item(moved_from, 0).setText(to_item)
        self.feature_table.item(moved_to, 0).setText(from_item)

        place_holder = self.feature_names_array[moved_from]
        self.feature_names_array[moved_from] = self.feature_names_array[moved_to]
        self.feature_names_array[moved_to] = place_holder

        place_holder = self.feature_position_array[moved_from]
        self.feature_position_array[moved_from] = self.feature_position_array[moved_to]
        self.feature_position_array[moved_to] = place_holder
        self.plot_widget.feature_positions = self.feature_position_array

        event.accept()

    def replotFeatures(self):
        if not self.dataset:
            self.warnings.noDataWarning()
            return
        self.dataframe = self.dataframe[self.feature_names_array]
        self.createPlot()

    # exit the app
    def exitApp(self):
        print("Exit pressed")
        self.close()

    # make the plot
    def createPlot(self):
        if self.plot_layout:
            self.plot_layout.removeWidget(self.plot_widget)

        # check for data before generating plot
        if not self.dataset:
            self.warnings.noDataWarning()
            return

        dic_checked = self.findChild(QtWidgets.QRadioButton, 'dicCheck')
        if dic_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
            self.plot_type = 'DICP'
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, self.feature_position_array,
                                                 self.plot_type)

        pcp_checked = self.findChild(QtWidgets.QRadioButton, 'pcpCheck')
        if pcp_checked.isChecked():
            self.plot_type = 'PCP'
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, self.feature_position_array,
                                                 self.plot_type)

        ap_checked = self.findChild(QtWidgets.QRadioButton, 'apCheck')
        if ap_checked.isChecked():
            self.plot_type = 'AP'
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, self.feature_position_array,
                                                 self.plot_type)

        acpo_checked = self.findChild(QtWidgets.QRadioButton, 'acpoCheck')
        if acpo_checked.isChecked():
            self.plot_type = 'ACPO'
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, self.feature_position_array, 'ACPO')

        spc_checked = self.findChild(QtWidgets.QRadioButton, 'spcCheck')
        if spc_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
            self.plot_type = 'SPCP'
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, self.feature_position_array,
                                                 self.plot_type)

        glcs_checked = self.findChild(QtWidgets.QRadioButton, 'glcsCheck')
        if glcs_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
            self.plot_type = 'GLCSP'
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, self.feature_position_array,
                                                 self.plot_type)

        glcs_opt_checked = self.findChild(QtWidgets.QRadioButton, 'glcstCheck')
        if glcs_opt_checked.isChecked():
            if self.feature_count % 2 != 0:
                self.warnings.oddFeatureCount()
                return
            self.plot_type = 'GLCSP_OPT'
            self.plot_widget = MAINPLOT.makePlot(self.dataframe, self.class_count, self.feature_count,
                                                 self.sample_count,
                                                 self.count_per_class_array, self.feature_position_array,
                                                 self.plot_type)

        self.plot_layout = self.findChild(QtWidgets.QVBoxLayout, 'plotDisplay')
        if self.is_placeholder:
            place_holder = self.findChild(QtWidgets.QWidget, 'placeHolder')
            self.plot_layout.removeWidget(place_holder)
            self.is_placeholder = False

        self.plot_layout.addWidget(self.plot_widget)

    def updatePlot(self):
        if not self.dataset:
            self.warnings.noDataWarning()
            return

        if self.show_axes.checkState() == Qt.CheckState.Unchecked:
            self.plot_widget.plot_axes = False
        else:
            self.plot_widget.plot_axes = True
        if self.show_markers.checkState() == Qt.CheckState.Unchecked:
            self.plot_widget.plot_markers = False
        else:
            self.plot_widget.plot_markers = True

        for i in range(self.class_count):
            if not self.dataset:
                self.warnings.noDataWarning()
                return

            if self.show_axes.checkState() == Qt.CheckState.Unchecked:
                self.plot_widget.plot_axes = False
            else:
                self.plot_widget.plot_axes = True
            if self.show_markers.checkState() == Qt.CheckState.Unchecked:
                self.plot_widget.plot_markers = False
            else:
                self.plot_widget.plot_markers = True

            for i in range(self.class_count):
                if self.class_table.item(i, 0).checkState() == Qt.CheckState.Checked:
                    self.class_to_plot[i] = True
                else:
                    self.class_to_plot[i] = False

            class_dict = self.plot_widget.class_dict
            class_color_dict = self.plot_widget.class_color_dict

            marker_dict = self.plot_widget.marker_dict
            marker_color_dict = self.plot_widget.marker_color_dict

            update_classes = SHOW_HIDE_CLASSES.showHideClassInfo(class_dict, class_color_dict, marker_dict,
                                                                 marker_color_dict, self.class_to_plot,
                                                                 self.class_count, self.feature_count,
                                                                 self.sample_count,
                                                                 self.count_per_class_array, self.plot_type)

            self.plot_widget.class_vertices = update_classes.new_class_vertices
            self.plot_widget.class_colors = update_classes.new_class_colors
            self.plot_widget.current_class_index_starts = update_classes.new_index_starts
            self.plot_widget.current_class_vertex_count = update_classes.new_vertex_counts
            self.plot_widget.current_sample_count = update_classes.new_sample_count

            self.plot_widget.marker_vertices = update_classes.new_marker_vertices
            self.plot_widget.marker_colors = update_classes.new_marker_colors
            self.plot_widget.marker_index_starts = update_classes.new_marker_index_starts
            self.plot_widget.marker_vertex_count = update_classes.new_marker_vertex_counts
            self.plot_widget.current_marker_count = update_classes.new_marker_count

            self.plot_widget.update()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
