import numpy as np
from sklearn.preprocessing import MinMaxScaler

import COLORS


class getAPInfo:
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
        scaler = MinMaxScaler((0, 90))
        df[:] = scaler.fit_transform(df[:])

        # get y_coord
        y_coord = df.to_numpy()
        y_coord = y_coord.ravel()

        space = 1.6 / self.feature_count
        scaffold_axis = np.asarray([[-0.8, -0.8]])

        j = 0
        for i in range(1, self.sample_count * (self.feature_count + 1)):
            if i % (self.feature_count + 1) == 0:
                scaffold_axis = np.append(scaffold_axis, [[-0.8, -0.8]], 0)
            else:
                new_x = np.cos(np.deg2rad(y_coord[j])) * space
                new_y = np.sin(np.deg2rad(y_coord[j])) * space
                scaffold_axis = np.append(scaffold_axis, [
                    [scaffold_axis[i - 1][0] + new_x, scaffold_axis[i - 1][1] + new_y]], 0)
                j += 1

        # how to randomly generate more colors?
        colors = COLORS.getColors()
        class_color_array = colors.colors_array

        color_array = np.tile(class_color_array[0], reps=(self.count_per_class_array[0] * (self.feature_count + 1), 1))
        for i in range(1, self.class_count):
            temp_array = np.tile(class_color_array[i], reps=(self.count_per_class_array[i] * (self.feature_count + 1), 1))
            color_array = np.concatenate((color_array, temp_array))

        index_starts = np.arange(0, self.sample_count * (self.feature_count + 1), self.feature_count + 1)
        vertex_count = np.repeat(self.feature_count + 1, self.sample_count * (self.feature_count + 1))

        return scaffold_axis, color_array, index_starts, vertex_count

    def getAxesVertices(self):
        axes_count = 2
        axes_vertices = [[-0.8, -0.8], [-0.8, 0.8], [-0.8, -0.8], [0.8, -0.8]]
        axes_color = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        axes_index_starts = [0, 2]
        axes_vertex_count = [2, 2]
        return axes_vertices, axes_color, axes_index_starts, axes_vertex_count, axes_count

    def getMarkerVertices(self):
        return None

    def getLabelInformation(self):
        title = 'Angled Coordinate Plot'
        return title
