import PLOT_OPENGL_INFORMATION

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def Left_index(points):
    '''
    Finding the left most point
    '''
    minn = 0
    for i in range(1, len(points)):
        if points[i].x < points[minn].x:
            minn = i
        elif points[i].x == points[minn].x:
            if points[i].y > points[minn].y:
                minn = i
    return minn


def orientation(p, q, r):
    '''
    To find orientation of ordered triplet (p, q, r).
    The function returns following values
    0 --> p, q and r are collinear
    1 --> Clockwise
    2 --> Counterclockwise
    '''
    val = (q.y - p.y) * (r.x - q.x) - \
          (q.x - p.x) * (r.y - q.y)

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def convexHull(points, n):
    # There must be at least 3 points
    if n < 3:
        return

    # Find the leftmost point
    l = Left_index(points)

    hull = []

    '''
    Start from leftmost point, keep moving counterclockwise
    until reach the start point again. This loop runs O(h)
    times where h is number of points in result or output.
    '''
    p = l
    q = 0
    while (True):

        # Add current point to result
        hull.append(p)

        '''
        Search for a point 'q' such that orientation(p, q,
        x) is counterclockwise for all points 'x'. The idea
        is to keep track of last visited most counterclock-
        wise point in q. If any point 'i' is more counterclock-
        wise than q, then update q.
        '''
        q = (p + 1) % n

        for i in range(n):

            # If i is more counterclockwise
            # than current q, then update q
            if (orientation(points[p],
                            points[i], points[q]) == 2):
                q = i

        '''
        Now q is the most counterclockwise with respect to p
        Set p as q for next iteration, so that q is added to
        result 'hull'
        '''
        p = q

        # While we don't come to first point
        if (p == l):
            break

    # Print Result
    for each in hull:
        print(points[each].x, points[each].y)
    return(hull)


class convexhull:
    def __init__(self, class_dict, feature_count, class_count, class_count_array):
        self.points_dict = {}
        conv_p = []
        points = []

        for i in range(class_count):
            arr = class_dict[i]
            for j in range(0, class_count_array[i] * (feature_count + 1)):
                if j % (feature_count+1) == 2 or j % (feature_count+1) == 3 or j % (feature_count+1) == 4 or j % (feature_count+1) == 5 or j % (feature_count+1) == 6 or j % (feature_count+1) == 7 or j % (feature_count+1) == 8 or j % (feature_count+1) == 9:
                    points.append(Point(arr[j][0], arr[j][1]))

            hull_points = convexHull(points, len(points))
            for p in hull_points:
                conv_p.append([points[p].x, points[p].y])
            self.points_dict[i] = conv_p
            points = []
            conv_p = []
            print('hi6')
            print(self.points_dict[i])
        #print(self.points_dict[i])
