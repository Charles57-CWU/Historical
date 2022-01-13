import numpy as np
from sklearn.preprocessing import MinMaxScaler

import COLORS


class getPCPInfo:
    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array):

        # dataset information
        self.dataframe = dataframe
        self.class_count = class_count
        self.feature_count = feature_count
        self.sample_count = sample_count
        self.count_per_class_array = count_per_class_array

    def getDatasetVertices(self):
        df = self.dataframe.copy()
        class_positions = {}
        class_colors = {}

        # scale attributes to fit to graphic coordinate system -0.8 to 0.8
        scaler = MinMaxScaler((0, 1))
        # df[:] = scaler.fit_transform(df[:])
        tmp = df.to_numpy().reshape(-1, 1)
        scaled = scaler.fit_transform(tmp).reshape(len(df), self.feature_count)
        df.loc[:] = scaled

        # change into 3 coordinate numpy vertex array ie: [[0, 0, 0], [1, 1, 1]]
        # get x_coord
        x_coord_array = np.linspace(start=0, stop=1, num=self.feature_count)
        x_coord = np.tile(x_coord_array, reps=self.sample_count)

        # get y_coord
        y_coord = df.to_numpy()
        y_coord = y_coord.ravel()

        # combine into x,y,z elements
        vertex_array = np.column_stack((x_coord, y_coord))

        # how to randomly generate more colors?
        colors = COLORS.getColors()
        class_color_array = colors.colors_array

        color_array = np.tile(class_color_array[0], reps=(self.count_per_class_array[0] * self.feature_count, 1))
        for i in range(1, self.class_count):
            temp_array = np.tile(class_color_array[i], reps=(self.count_per_class_array[i] * self.feature_count, 1))
            color_array = np.concatenate((color_array, temp_array))

        j = 0
        for i in range(self.class_count):
            k = j + (self.count_per_class_array[i] * self.feature_count)
            class_positions[i] = vertex_array[j:k]
            class_colors[i] = color_array[j:k]
            j = k

        data_plot_indices = np.arange(0, self.sample_count * self.feature_count, self.feature_count)
        data_vertices_per_line = np.repeat(self.feature_count, self.sample_count * self.feature_count)

        return class_positions, class_colors, data_plot_indices, data_vertices_per_line

    def getAxesVertices(self):
        # add x-axis
        axis_vertex_array = [[0, 0]]
        # add y-axes

        x_coord_array = np.linspace(start=0, stop=1, num=self.feature_count)
        y_coord_array_bottom = np.repeat(0, self.feature_count)
        y_coord_array_top = np.repeat(1, self.feature_count)

        for i in range(self.feature_count):
            axis_vertex_array.append([x_coord_array[i], y_coord_array_bottom[i]])
            axis_vertex_array.append([x_coord_array[i], y_coord_array_top[i]])

        axis_color_array = np.tile([0, 0, 0], reps=(self.feature_count * 2 + 1, 1))
        axis_vertex_array = np.delete(axis_vertex_array, 0, 0)

        axis_ind = np.arange(0, self.feature_count * 2, 2)
        axis_per_line = np.repeat(2, self.feature_count)
        axes_count = self.feature_count
        return axis_vertex_array, axis_color_array, axis_ind, axis_per_line, axes_count

    def getMarkerVertices(self, scaffold_axis):
        marker_positions = scaffold_axis
        marker_colors = {}

        colors = COLORS.getColors()
        class_color_array = colors.colors_array

        point_color_array = np.tile(class_color_array[0],
                                    reps=(self.count_per_class_array[0] * self.feature_count, 1))
        for i in range(1, self.class_count):
            temp_array = np.tile(class_color_array[i],
                                 reps=(self.count_per_class_array[i] * self.feature_count, 1))
            point_color_array = np.concatenate((point_color_array, temp_array))

        j = 0
        for i in range(self.class_count):
            k = j + (self.count_per_class_array[i] * self.feature_count)
            marker_colors[i] = point_color_array[j:k]
            j = k

        index_starts = np.arange(0, self.sample_count * self.feature_count, 1)
        vertex_count = np.repeat(1, self.sample_count * self.feature_count)
        point_count = self.sample_count * self.feature_count

        return marker_positions, marker_colors, index_starts, vertex_count, point_count

    def getLabelInformation(self):
        return None
