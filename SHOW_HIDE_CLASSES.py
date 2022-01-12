"""
PLOT_OPENGL_INFORMATION.py holds information related to marker, axes, data, and label of a future plot

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""

import PCP
import ACP
import SPCP
import DICP
import GLCSP
import GLCSP_OPT

import numpy as np


def new_vertex_info(line_length, sample_count):
    data_plot_indices = np.arange(0, sample_count * line_length, line_length)
    data_vertices_per_line = np.repeat(line_length, sample_count)

    return data_plot_indices, data_vertices_per_line




class showHideClassInfo:
    def __init__(self, class_vertices, class_to_plot, class_count, feature_count, sample_count,
                 count_per_class_array, plot_type):

        # dataset information
        self.class_vertices = None
        self.class_array = None
        self.class_colors = None
        self.class_index_starts = None
        self.class_vertex_count = None

        # axes information
        self.axes_vertices = None
        self.axes_colors = None
        self.axes_index_starts = None
        self.axes_vertex_count = None
        self.axes_count = None

        # marker information
        self.marker_vertices = None
        self.marker_colors = None
        self.marker_index_starts = None
        self.marker_vertex_count = None
        self.marker_count = None
        print(plot_type)

        if plot_type == 'SPCP':
            print(np.shape(class_vertices))





