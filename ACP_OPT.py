import numpy as np
from sklearn.preprocessing import MinMaxScaler

import COLORS


class getCC2Info:
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
        class_positions = {}
        class_colors = {}

        # scale attributes to fit to graphic coordinate system -0.8 to 0.8
        scaler = MinMaxScaler((0, 1))
        df[:] = scaler.fit_transform(df[:])
        #tmp = df.to_numpy().reshape(-1, 1)
        #scaled = scaler.fit_transform(tmp).reshape(len(df), self.feature_count)
        #df.loc[:] = scaled

        # get y_coord
        y_coord = df.to_numpy()
        y_coord = y_coord.ravel()

        space = 1 / self.feature_count

        scaffold_axis = np.asarray([[0, 0]])

        angle_array = [80, 55, 25, 10, 20, 20, 20, 20, 20, 20, 45, 45]
        j = 0
        k = 0
        for i in range(1, self.sample_count * (self.feature_count + 1)):
            if i % (self.feature_count + 1) == 0:
                scaffold_axis = np.append(scaffold_axis, [[0, 0]], 0)
                j = 0
            else:
                new_x = np.cos(np.deg2rad(angle_array[j])) * y_coord[k] * space
                new_y = np.sin(np.deg2rad(angle_array[j])) * y_coord[k] * space
                scaffold_axis = np.append(scaffold_axis, [
                    [scaffold_axis[i - 1][0] + new_x, scaffold_axis[i - 1][1] + new_y]], 0)
                j += 1
                k += 1

        # how to randomly generate more colors?
        colors = COLORS.getColors()
        class_color_array = colors.colors_array

        color_array = np.tile(class_color_array[0], reps=(self.count_per_class_array[0] * (self.feature_count + 1), 1))
        for i in range(1, self.class_count):
            temp_array = np.tile(class_color_array[i], reps=(self.count_per_class_array[i] * (self.feature_count + 1), 1))
            color_array = np.concatenate((color_array, temp_array))

        j = 0
        for i in range(self.class_count):
            k = j + (self.count_per_class_array[i] * (self.feature_count + 1))
            class_positions[i] = scaffold_axis[j:k]
            class_colors[i] = color_array[j:k]
            j = k

        index_starts = np.arange(0, self.sample_count * (self.feature_count + 1), self.feature_count + 1)
        vertex_count = np.repeat(self.feature_count + 1, self.sample_count)

        return class_positions, class_colors, index_starts, vertex_count

    def getAxesVertices(self):
        axes_count = 2
        axes_vertices = [[0, 0], [0, 1], [0, 0], [1, 0]]
        axes_color = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        axes_index_starts = [0, 2]
        axes_vertex_count = [2, 2]
        return axes_vertices, axes_color, axes_index_starts, axes_vertex_count, axes_count

    def getMarkerVertices(self, scaffold_axis):
        marker_positions = {}
        marker_colors = {}

        for i in range(len(scaffold_axis)):
            marker_positions[i] = np.delete(scaffold_axis[i],
                                            np.arange(0, np.shape(scaffold_axis[i])[0], int(self.feature_count + 1)), axis=0)
        #print(marker_positions)

        colors = COLORS.getColors()
        class_color_array = colors.colors_array

        point_color_array = np.tile(class_color_array[0],
                                    reps=(self.count_per_class_array[0] * int(self.feature_count), 1))
        for i in range(1, self.class_count):
            temp_array = np.tile(class_color_array[i],
                                 reps=(self.count_per_class_array[i] * int(self.feature_count), 1))
            point_color_array = np.concatenate((point_color_array, temp_array))

        j = 0
        for i in range(self.class_count):
            k = j + (self.count_per_class_array[i] * int(self.feature_count))
            marker_colors[i] = point_color_array[j:k]
            j = k

        index_starts = np.arange(0, self.sample_count * int(self.feature_count), 1)
        vertex_count = np.repeat(1, self.sample_count * int(self.feature_count))
        point_count = self.sample_count * int(self.feature_count)

        return marker_positions, marker_colors, index_starts, vertex_count, point_count


    def getLabelInformation(self):
        title = 'Angled Coordinate Plot'
        return title
