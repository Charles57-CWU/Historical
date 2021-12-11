from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic

from OpenGL.GL import *

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
        number_of_classes = self.dataset.number_of_classes
        class_names_array = self.dataset.class_names_array
        count_per_class_array = self.dataset.count_per_class_array
        number_of_samples = self.dataset.number_of_samples
        number_of_features = self.dataset.number_of_features

        # display data
        dataset_info_string = ('Number of Classes: ' + str(number_of_classes) +
                               '\n\n' + 'Number of Features: ' + str(number_of_features) +
                               '\n\n' + 'Number of Samples: ' + str(number_of_samples))

        # loop through class names
        print('here?')
        counter = 1
        for ele in count_per_class_array:
            dataset_info_string += ('\n\n' + 'Class ' + str(counter) + ': ' + str(class_names_array[counter - 1]) +
                                    '\n' + '--Count: ' + str(ele) +
                                    '\n' + '--Color: ' + self.colors.colors_names_array[counter - 1])
            counter += 1
        print(dataset_info_string)
        # print text to box
        data_info = self.findChild(QtWidgets.QTextBrowser, 'datasetInfoBrowser')
        data_info.setText(dataset_info_string)

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
            DICP.makeDICP(request_plot)

        pcp_checked = self.findChild(QtWidgets.QRadioButton, 'pcpCheck')
        if pcp_checked.isChecked():
            PCP.makePCP(request_plot)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()