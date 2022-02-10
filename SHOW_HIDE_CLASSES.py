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


def new_class_vertex_info(line_length, class_count, class_to_plot, class_position_array, count_per_class_array, class_dict, class_color_dict):
    new_class_vertices = [[0, 0]]
    new_class_colors = [[0, 0, 0]]
    new_sample_count = 0
    new_index_starts = []
    new_vertex_counts = []

    j = 0
    for i in range(class_count):
        if class_to_plot[i]:
            k = j + count_per_class_array[class_position_array[i]] * line_length
            temp_starts = np.arange(j, k, line_length)
            new_index_starts = np.concatenate((new_index_starts, temp_starts))
            j = k

            temp_counts = np.repeat(line_length, count_per_class_array[class_position_array[i]])
            new_vertex_counts = np.concatenate((new_vertex_counts, temp_counts))

            new_sample_count += count_per_class_array[class_position_array[i]]

            new_class_vertices = np.concatenate((new_class_vertices, class_dict[class_position_array[i]]))
            new_class_colors = np.concatenate((new_class_colors, class_color_dict[class_position_array[i]]))

    new_class_vertices = np.delete(new_class_vertices, 0, axis=0)
    new_class_vertices = new_class_vertices.astype('float32')
    new_class_colors = np.delete(new_class_colors, 0, axis=0)
    new_class_colors = new_class_colors.astype('float32')

    return new_class_vertices, new_class_colors, new_sample_count, new_vertex_counts, new_index_starts


def new_marker_vertex_info(marker_per_line, class_count, marker_to_plot, class_position_array, count_per_class_array, marker_dict, marker_color_dict):
    new_marker_vertices = [[0, 0]]
    new_marker_colors = [[0, 0, 0]]
    new_marker_count = 0
    new_index_starts = []
    new_vertex_counts = []

    j = 0
    for i in range(class_count):
        if marker_to_plot[i]:
            k = j + count_per_class_array[class_position_array[i]] * marker_per_line
            temp_starts = np.arange(j, k, marker_per_line)
            new_index_starts = np.concatenate((new_index_starts, temp_starts))
            j = k

            temp_counts = np.repeat(marker_per_line, count_per_class_array[class_position_array[i]])
            new_vertex_counts = np.concatenate((new_vertex_counts, temp_counts))

            new_marker_count += count_per_class_array[class_position_array[i]]

            new_marker_vertices = np.concatenate((new_marker_vertices, marker_dict[class_position_array[i]]))
            new_marker_colors = np.concatenate((new_marker_colors, marker_color_dict[class_position_array[i]]))

    new_marker_vertices = np.delete(new_marker_vertices, 0, axis=0)
    new_marker_vertices = new_marker_vertices.astype('float32')
    new_marker_colors = np.delete(new_marker_colors, 0, axis=0)
    new_marker_colors = new_marker_colors.astype('float32')

    return new_marker_vertices, new_marker_colors, new_marker_count, new_vertex_counts, new_index_starts


class showHideClassInfo:
    def __init__(self, class_dict, class_color_dict, marker_dict, marker_color_dict, class_to_plot, marker_to_plot, class_count, feature_count, sample_count, class_position_array,
                 count_per_class_array, plot_type):

        line_length = None
        marker_per_line = None
        self.new_class_vertices = None
        self.new_class_colors = None
        self.new_sample_count = None
        self.new_index_starts = None
        self.new_vertex_counts = None

        self.new_marker_vertices = None
        self.new_marker_colors = None
        self.new_marker_count = None
        self.new_marker_index_starts = None
        self.new_marker_vertex_counts = None

        if plot_type == 'SPCP' or plot_type == 'DICP':
            line_length = int(feature_count / 2)
            marker_per_line = int(feature_count / 2)
        elif plot_type == 'PCP':
            line_length = feature_count
            marker_per_line = feature_count
        elif plot_type == 'AP' or plot_type == 'ACP_OPT':
            line_length = feature_count + 1
            marker_per_line = feature_count
        elif plot_type == 'GLCSP':
            line_length = int(feature_count / 2)
            marker_per_line = int(feature_count / 2)

        self.new_class_vertices, self.new_class_colors, self.new_sample_count, self.new_vertex_counts, self.new_index_starts = new_class_vertex_info(
            line_length, class_count, class_to_plot, class_position_array, count_per_class_array, class_dict, class_color_dict)

        self.new_marker_vertices, self.new_marker_colors, self.new_marker_count, self.new_marker_vertex_counts, self.new_marker_index_starts = new_marker_vertex_info(
            marker_per_line, class_count, marker_to_plot, class_position_array, count_per_class_array, marker_dict, marker_color_dict)

