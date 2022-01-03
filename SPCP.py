import numpy as np
from sklearn.preprocessing import MinMaxScaler

import COLORS


class getSPCPInfo:
    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array):

        # dataset information
        self.dataframe = dataframe
        self.class_count = class_count
        self.feature_count = feature_count
        self.sample_count = sample_count
        self.count_per_class_array = count_per_class_array

    def getClassVertices(self):
        df = self.dataframe.copy()

        section_array = np.linspace(start=0, stop=1, num=int(self.feature_count / 2) + 1)

        # scale attributes to fit to graphic coordinate system -0.8 to 0.8

        j = 0
        for i in range(self.feature_count):
            if i % 2 != 0:
                scaler = MinMaxScaler((0, 1))
                df[df.columns[i]] = scaler.fit_transform(df[[df.columns[i]]])
            else:
                scaler = MinMaxScaler((section_array[j], section_array[j + 1]))
                df[df.columns[i]] = scaler.fit_transform(df[[df.columns[i]]])
                j += 1

        # get xy_coord
        xy_coord = df.to_numpy()
        xy_coord = xy_coord.ravel()
        xy_coord = np.reshape(xy_coord, (-1, 2))

        # how to randomly generate more colors?
        colors = COLORS.getColors()
        class_color_array = colors.colors_array

        color_array = np.tile(class_color_array[0], reps=(self.count_per_class_array[0] * int((self.feature_count / 2)), 1))
        for i in range(1, self.class_count):
            temp_array = np.tile(class_color_array[i], reps=(self.count_per_class_array[i] * int((self.feature_count / 2)), 1))
            color_array = np.concatenate((color_array, temp_array))

        data_plot_indices = np.arange(0, self.sample_count * int(self.feature_count / 2), int(self.feature_count / 2))
        data_vertices_per_line = np.repeat(int(self.feature_count / 2), self.sample_count)

        return xy_coord, color_array, data_plot_indices, data_vertices_per_line

    def getAxesVertices(self):
        # add x-axis
        axis_vertex_array = [[0, 0], [1, 0]]
        # add y-axes

        new_count = int(self.feature_count / 2) + 1

        x_coord_array = np.linspace(start=0, stop=1, num=new_count)
        y_coord_array_bottom = np.repeat(0, new_count)
        y_coord_array_top = np.repeat(1, new_count)

        for i in range(new_count - 1):
            axis_vertex_array.append([x_coord_array[i], y_coord_array_bottom[i]])
            axis_vertex_array.append([x_coord_array[i], y_coord_array_top[i]])

        axis_color_array = np.tile([0, 0, 0], reps=(new_count * 2 + 1, 1))

        axis_ind = np.arange(0, (self.feature_count + 1) * 2, 2)
        axis_per_line = np.repeat(2, self.feature_count + 1)

        axes_count = self.feature_count + 1

        return axis_vertex_array, axis_color_array, axis_ind, axis_per_line, axes_count

    def getMarkerVertices(self, scaffold_axis):
        point_array = scaffold_axis
        point_color_array = np.tile([0, 0, 0], reps=(point_array.shape[0], 1))

        index_starts = np.arange(0, self.sample_count * (self.feature_count/2), 1)
        vertex_count = np.repeat(1, self.sample_count * (self.feature_count/2))
        point_count = self.sample_count * int(self.feature_count/2)
        return point_array, point_color_array, index_starts, vertex_count, point_count


    def getLabelInformation(self):
        return None