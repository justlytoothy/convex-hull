from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25


#
# This is the class you have to complete.
#
def find_slope(a, b):
    return (a[1] - b[1]) / (a[0] - b[0])


def get_next_index(i, n, direction):
    if direction > 0:  # counter-clockwise
        if i == n - 1:
            return 0
        else:
            return i + 1
    else:  # clockwise
        if i == 0:
            return n - 1
        else:
            return i - 1


def merge_hulls(left_hull, right_hull):
    maxEl = left_hull[-1][0]
    maxIndex = len(left_hull) - 1
    for i in range(len(left_hull)):
        if left_hull[i][0] > maxEl:
            maxEl = left_hull[i][0]
            maxIndex = i
    minEl = right_hull[0][0]
    minIndex = 0
    for i in range(len(right_hull)):
        if right_hull[i][0] < minEl:
            minEl = right_hull[i][0]
            minIndex = i

    merged_hull = []
    left_point = left_hull[maxIndex]
    right_point = right_hull[minIndex]
    left_point_lower = left_hull[maxIndex]
    right_point_lower = right_hull[minIndex]
    left_index = maxIndex
    right_index = minIndex
    left_index_lower = maxIndex
    right_index_lower = minIndex
    curr_slope = find_slope(left_point, right_point)
    changed = True
    left_stopped = get_next_index(maxIndex, len(left_hull), 1)
    right_stopped = get_next_index(minIndex, len(right_hull), -1)
    while changed is True:
        changed = False
        i = left_stopped
        while find_slope(left_hull[i], right_point) < curr_slope:
            changed = True
            left_point = left_hull[i]
            curr_slope = find_slope(left_point, right_point)
            left_index = i
            i = get_next_index(i, len(left_hull), 1)
        left_stopped = i
        i = right_stopped
        while find_slope(left_point, right_hull[i]) > curr_slope:
            changed = True
            right_point = right_hull[i]
            curr_slope = find_slope(left_point, right_point)
            right_index = i
            i = get_next_index(i, len(right_hull), -1)
        right_stopped = i

    curr_slope = find_slope(left_point_lower, right_point_lower)

    changed = True
    left_stopped = get_next_index(maxIndex, len(left_hull), -1)
    right_stopped = get_next_index(minIndex, len(right_hull), 1)
    while changed is True:
        changed = False
        i = left_stopped
        while find_slope(left_hull[i], right_point_lower) > curr_slope:
            changed = True
            left_point_lower = left_hull[i]
            curr_slope = find_slope(left_point_lower, right_point_lower)
            left_index_lower = i
            i = get_next_index(i, len(left_hull), -1)
        left_stopped = i
        i = right_stopped
        while find_slope(left_point_lower, right_hull[i]) < curr_slope:
            changed = True
            right_point_lower = right_hull[i]
            curr_slope = find_slope(left_point_lower, right_point_lower)
            right_index_lower = i
            i = get_next_index(i, len(right_hull), 1)
        right_stopped = i
    i = left_index

    while i != left_index_lower:
        merged_hull.append(left_hull[i])
        i = get_next_index(i, len(left_hull), 1)
    merged_hull.append(left_hull[i])
    i = right_index_lower
    while i != right_index:
        merged_hull.append(right_hull[i])
        i = get_next_index(i, len(right_hull), 1)
    merged_hull.append(right_hull[i])
    return merged_hull


# O(logn)
def convex_solver(points):
    if len(points) <= 2:
        return points
    mid = len(points) // 2
    left_hull = convex_solver(points[:mid])
    right_hull = convex_solver(points[mid:])
    return merge_hulls(left_hull, right_hull)


class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)
        t1 = time.time()
        # TODO: SORT THE POINTS BY INCREASING X-VALUE
        points = sorted([(p.x(), p.y()) for p in points])
        t2 = time.time()

        t3 = time.time()
        hull = convex_solver(points)
        polygon = [QLineF(QPointF(hull[i][0], hull[i][1]),
                          QPointF(hull[(i + 1) % len(hull)][0],
                                  hull[(i + 1) % len(hull)][1])) for i in range(len(hull))]
        # TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
        # split array in half
        # build doubly linked list
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
