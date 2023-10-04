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
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else 2


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

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.next = None
            self.prev = None

    def convex_hull(self, points):
        if len(points) <= 3:
            return points
        points.sort(key=lambda p: (p.x, p.y))

        # Initialize the doubly linked list
        head = points[0]
        tail = points[-1]
        head.next = tail
        tail.prev = head

        upper_hull = [head, points[1]]

        for i in range(2, len(points)):
            while len(upper_hull) > 1 and orientation(upper_hull[-2], upper_hull[-1], points[i]) != 2:
                upper_hull.pop()
            upper_hull[-1].next = points[i]
            points[i].prev = upper_hull[-1]
            upper_hull.append(points[i])

        lower_hull = [tail, points[-2]]

        for i in range(len(points) - 3, -1, -1):
            while len(lower_hull) > 1 and orientation(lower_hull[-2], lower_hull[-1], points[i]) != 2:
                lower_hull.pop()
            lower_hull[-1].next = points[i]
            points[i].prev = lower_hull[-1]
            lower_hull.append(points[i])

        upper_hull[-1].next = lower_hull[0]
        lower_hull[0].prev = upper_hull[-1]

        return upper_hull + lower_hull

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
            converted_points.append(self.Point(point[0], point[1]))
        hull = self.convex_hull(converted_points)
        polygon = [QLineF(QPointF(hull[i].x, hull[i].y),
                          QPointF(hull[(i + 1) % len(hull)].x, hull[(i + 1) % len(hull)].y)) for i in range(len(hull))]
        # TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
        # split array in half
        # build doubly linked list
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
