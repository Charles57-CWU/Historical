from PyQt5 import QtWidgets
from PyQt5 import uic
import pandas as pd

# colors
import COLORS

# dataset information
import DATA

# plot information
import DICP
import PCP

import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # load Ui from ui File made in QTDesigner
        super(Ui, self).__init__()
        uic.loadUi('visualizationGui.ui', self)

        # general variables
        self.dataset = ''
        self.colors = COLORS.getColors()
        self.class_count = 0
        self.feature_count = 0
        self.sample_count = 0
        self.count_per_class_array = []
        self.dataframe = ''

        # exit button
        self.exit_button_pressed = self.findChild(QtWidgets.QPushButton, 'exitButton')
        self.exit_button_pressed.clicked.connect(self.exitApp)

        # generate plot button
        self.plot_button_pressed = self.findChild(QtWidgets.QPushButton, 'makePlotButton')
        self.plot_button_pressed.clicked.connect(self.createPlot)

        # file upload button
        self.upload_button_pressed = self.findChild(QtWidgets.QPushButton, 'uploadButton')
        self.upload_button_pressed.clicked.connect(self.uploadDataset)

    # upload dataset
    def uploadDataset(self):
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
            feature_info_string += (str('D') + str(counter) + ' - ' + str(ele) + '\n\n')
            counter += 1

        # remove extra \n\n
        class_data_string = feature_info_string[:len(feature_info_string) - 2]

        # print text to box
        feature_info = self.findChild(QtWidgets.QTextBrowser, 'attributeBrowser')
        feature_info.setText(feature_info_string)

    # exit the app
    def exitApp(self):
        print("Exit pressed")
        self.close()

    # make the plot
    def createPlot(self):

        # check for data before generating plot
        if self.dataset == '':
            no_data_message = QtWidgets.QMessageBox()
            no_data_message.setWindowTitle('Warning: No dataset')
            no_data_message.setText('Please upload dataset before generating plot.')
            no_data_message.setIcon(QtWidgets.QMessageBox.Warning)
            no_data_message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            no_data_message.exec()
            return

        # generate plot
        request_plot = self.findChild(QtWidgets.QOpenGLWidget, 'mainVisual')

        dic_checked = self.findChild(QtWidgets.QRadioButton, 'dicCheck')
        if dic_checked.isChecked():
            DICP.makeDICP(request_plot, self.dataframe, self.class_count, self.feature_count, self.sample_count,
                          self.count_per_class_array)

        pcp_checked = self.findChild(QtWidgets.QRadioButton, 'pcpCheck')
        if pcp_checked.isChecked():
            PCP.makePCP(request_plot, self.dataframe, self.class_count, self.feature_count, self.sample_count,
                        self.count_per_class_array)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
