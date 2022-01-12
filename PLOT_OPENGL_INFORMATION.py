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


class getPlotInfo:
    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array, plot_type):

        # dataset information
        self.class_vertices = None
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

        # label information
        self.title = None

        if not plot_type:
            print('choose_plot')
        elif plot_type == 'PCP':
            pcp_info = PCP.getPCPInfo(dataframe, class_count, feature_count, sample_count,
                                      count_per_class_array)
            self.class_vertices, self.class_colors, self.class_index_starts, self.class_vertex_count = pcp_info.getDatasetVertices()
            self.axes_vertices, self.axes_colors, self.axes_index_starts, self.axes_vertex_count, self.axes_count = pcp_info.getAxesVertices()

        elif plot_type == 'AP':
            ap_info = ACP.getAPInfo(dataframe, class_count, feature_count, sample_count,
                                    count_per_class_array)
            self.class_vertices, self.class_colors, self.class_index_starts, self.class_vertex_count = ap_info.getClassVertices()
            self.axes_vertices, self.axes_colors, self.axes_index_starts, self.axes_vertex_count, self.axes_count = ap_info.getAxesVertices()
            self.title = ap_info.getLabelInformation()
            self.marker_vertices, self.marker_colors, self.marker_index_starts, self.marker_vertex_count, self.marker_count = ap_info.getMarkerVertices(
                self.class_vertices)

        elif plot_type == 'SPCP':
            spcp_info = SPCP.getSPCPInfo(dataframe, class_count, feature_count, sample_count,
                                         count_per_class_array)
            self.class_vertices, self.class_colors, self.class_index_starts, self.class_vertex_count = spcp_info.getClassVertices()
            self.axes_vertices, self.axes_colors, self.axes_index_starts, self.axes_vertex_count, self.axes_count = spcp_info.getAxesVertices()
            self.marker_vertices, self.marker_colors, self.marker_index_starts, self.marker_vertex_count, self.marker_count = spcp_info.getMarkerVertices(
                self.class_vertices)

        elif plot_type == 'DICP':
            dicp_info = DICP.getDICPInfo(dataframe, class_count, feature_count, sample_count,
                                         count_per_class_array)
            self.class_vertices, self.class_colors, self.class_index_starts, self.class_vertex_count = dicp_info.getClassVertices()
            self.axes_vertices, self.axes_colors, self.axes_index_starts, self.axes_vertex_count, self.axes_count = dicp_info.getAxesVertices()
            self.marker_vertices, self.marker_colors, self.marker_index_starts, self.marker_vertex_count, self.marker_count = dicp_info.getMarkerVertices(
                self.class_vertices)

        elif plot_type == 'GLCSP':
            glcsp_info = GLCSP.getGLCSPInfo(dataframe, class_count, feature_count, sample_count,
                                            count_per_class_array)
            self.class_vertices, self.class_colors, self.class_index_starts, self.class_vertex_count = glcsp_info.getClassVertices()
            self.axes_vertices, self.axes_colors, self.axes_index_starts, self.axes_vertex_count, self.axes_count = glcsp_info.getAxesVertices()
            self.marker_vertices, self.marker_colors, self.marker_index_starts, self.marker_vertex_count, self.marker_count = glcsp_info.getMarkerVertices(self.class_vertices)

        elif plot_type == 'GLCSP_OPT':
            glcsp_opt_info = GLCSP_OPT.getGLCSP_OPTInfo(dataframe, class_count, feature_count, sample_count,
                                         count_per_class_array)
            self.class_vertices, self.class_colors, self.class_index_starts, self.class_vertex_count = glcsp_opt_info.getClassVertices()
            self.axes_vertices, self.axes_colors, self.axes_index_starts, self.axes_vertex_count, self.axes_count = glcsp_opt_info.getAxesVertices()
            self.marker_vertices, self.marker_colors, self.marker_index_starts, self.marker_vertex_count, self.marker_count = glcsp_opt_info.getMarkerVertices(
                self.class_vertices)