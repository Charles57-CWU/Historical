"""
GLCSLP.py holds the information to render a parallel coordinate plot

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""

import numpy as np
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
from sklearn.preprocessing import MinMaxScaler
from PyQt5.QtWidgets import QOpenGLWidget

import COLORS

"""
class makePlot(QOpenGLWidget):
    width = 800
    height = 600

    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array, parent=None):
        super(makePlot, self).__init__(parent)
        #print(dataframe)
        self.dataframe = dataframe
        self.class_count = class_count
        self.feature_count = feature_count
        self.sample_count = sample_count
        self.count_per_class_array = count_per_class_array

        # get vertice information
        data, color_array = getVertexAndColors(self.dataframe, self.class_count, self.feature_count, self.sample_count,
                                               self.count_per_class_array)
        self.data = data.astype('float32')
        self.color_array = color_array.astype('float32')

        axes_vertex_array, axes_color_array = get_axes(self.feature_count)
        self.axes_vertex_array = np.asarray(axes_vertex_array, dtype='float32')
        self.axes_color = axes_color_array.astype('float32')
"""