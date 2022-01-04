import numpy as np
from sklearn.preprocessing import MinMaxScaler

import COLORS


class getGLCSP_OPTInfo:
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

        space = 1 / (int(self.feature_count / 2) + 1)
        for i in range(self.feature_count):
            scaler = MinMaxScaler((0, space))
            df[df.columns[i]] = scaler.fit_transform(df[[df.columns[i]]])

        angle_array = [0, 45, 0, 0, 0, 0, 0, 0, 0]
        j = 0
        for i in range(0, self.feature_count, 2):
            xy_temp = np.asarray([df[df.columns[i]], df[df.columns[i + 1]]])
            theta = np.deg2rad(angle_array[j])
            j += 1
            rotation_matrix = np.array([[np.cos(theta), np.sin(theta)],
                                        [-np.sin(theta), np.cos(theta)]])

            xy_temp = np.matmul(rotation_matrix, xy_temp)
            df[df.columns[i]] = xy_temp[0]
            df[df.columns[i + 1]] = xy_temp[1]

        # get xy_coord [[0,0],[2,0]]
        xy_coord = df.to_numpy()
        xy_coord = xy_coord.ravel()
        xy_coord = np.reshape(xy_coord, (-1, 2))
        scaffold_axis = np.asarray([[0, 0]])
        j = 0
        for i in range(self.sample_count * int(self.feature_count / 2 + 1)):
            if i % int(self.feature_count / 2 + 1) == 0:
                if i == 0:
                    scaffold_axis = np.asarray([[0, 0]])
                else:
                    scaffold_axis = np.append(scaffold_axis, [[0, 0]], 0)
            else:
                scaffold_axis = np.append(scaffold_axis, [
                    [scaffold_axis[i - 1][0] + xy_coord[j][0], scaffold_axis[i - 1][1] + xy_coord[j][1]]], 0)
                j += 1

        # how to randomly generate more colors?
        colors = COLORS.getColors()
        class_color_array = colors.colors_array

        color_array = np.tile(class_color_array[0], reps=(self.count_per_class_array[0] * int((self.feature_count / 2) + 1), 1))
        for i in range(1, self.class_count):
            temp_array = np.tile(class_color_array[i],
                                 reps=(self.count_per_class_array[i] * int((self.feature_count / 2) + 1), 1))
            color_array = np.concatenate((color_array, temp_array))

        index_starts = np.arange(0, self.sample_count * (int(self.feature_count / 2) + 1), int(self.feature_count / 2) + 1)
        vertex_count = np.repeat(int(self.feature_count / 2) + 1, self.sample_count)

        return scaffold_axis, color_array, index_starts, vertex_count

    def getAxesVertices(self):
        axes_count = 2
        axes_vertices = [[0, 0], [0, 1], [0, 0], [1, 0]]
        axes_color = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        axes_index_starts = [0, 2]
        axes_vertex_count = [2, 2]
        return axes_vertices, axes_color, axes_index_starts, axes_vertex_count, axes_count

    def getMarkerVertices(self, scaffold_axis):
        arrowhead_size = 0.01
        arrowhead_angle = arrowhead_size * np.tan(np.radians(30) / 2)
        triangle_array = np.asarray([[0, 0]])
        for i in range(self.sample_count * int(self.feature_count / 2 + 1)):
            if i % int(self.feature_count / 2 + 1) == 0:
                continue
            else:
                triangle_array = np.append(triangle_array, [[scaffold_axis[i][0], scaffold_axis[i][1]]], 0)

                # find unit vector of line
                vX = scaffold_axis[i][0] - scaffold_axis[i - 1][0]
                vY = scaffold_axis[i][1] - scaffold_axis[i - 1][1]

                length = np.sqrt(vX ** 2 + vY ** 2)
                if length != 0:
                    unitvX = vX / length
                    unitvY = vY / length
                else:
                    unitvX = 0
                    unitvY = 0

                v_point_1 = [scaffold_axis[i][0] - unitvX * arrowhead_size - unitvY * arrowhead_angle,
                             scaffold_axis[i][1] - unitvY * arrowhead_size + unitvX * arrowhead_angle]

                triangle_array = np.append(triangle_array, [[v_point_1[0], v_point_1[1]]], 0)

                v_point_2 = [scaffold_axis[i][0] - unitvX * arrowhead_size + unitvY * arrowhead_angle,
                             scaffold_axis[i][1] - unitvY * arrowhead_size - unitvX * arrowhead_angle]
                triangle_array = np.append(triangle_array, [[v_point_2[0], v_point_2[1]]], 0)

        triangle_array = np.delete(triangle_array, 0, 0)
        # print(triangle_array)
        arrowhead_color_array = np.tile([0, 0, 0], reps=(triangle_array.shape[0], 1))

        index_starts = np.arange(0, self.sample_count * int(self.feature_count / 2) * 3, 3)
        vertex_count = np.repeat(3, self.sample_count * int(self.feature_count / 2))
        triangle_count = self.sample_count * int(self.feature_count / 2)

        return triangle_array, arrowhead_color_array, index_starts, vertex_count, triangle_count


    def getLabelInformation(self):
        title = 'Angled Coordinate Plot'
        return title