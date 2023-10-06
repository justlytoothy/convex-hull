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
    return (a.y - b.y) / (a.x - b.x)


# Use point object to contain both the point coords and the linked list structure
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, point):
        if not self.head:
            self.head = point
            point.next = point
            point.prev = point
        else:
            tail = self.head.prev
            tail.next = point
            point.prev = tail
            point.next = self.head
            self.head.prev = point

    def get_rightmost(self):
        return self.head.prev

    def get_leftmost(self):
        return self.head


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise


def merge_hulls(left_hull, right_hull):
    pass


def convex_solver(points):
    if len(points) <= 2:
        dub_list = DoublyLinkedList()
        for point in points:
            dub_list.append(point)
        return dub_list
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
        # this is a dummy polygon of the first 3 unsorted points
        converted_points = []
        for point in points:
            converted_points.append(Point(point[0], point[1]))
        # hull = self.convex_hull(converted_points)
        hull = convex_solver(converted_points)
        curr = hull.head
        hull_list = []
        while True:
            hull_list.append(curr)
            curr = curr.next
            if curr == hull.head:
                break
        polygon = [QLineF(QPointF(hull_list[i].x, hull_list[i].y),
                          QPointF(hull_list[(i + 1) % len(hull_list)].x,
                                  hull_list[(i + 1) % len(hull_list)].y)) for i in range(len(hull_list))]
        # TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
        # split array in half
        # build doubly linked list
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
