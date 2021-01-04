import sys
from collections import namedtuple

Point = namedtuple("Point", ["X", "Y"])


class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def find_contours(image):
    gp_paths = []

    for y in range(len(image) - 1):
        for x in range(len(image[y]) - 1):
            if image[y][x] == sys.maxsize:
                continue

            if not (image[y][x] > 0 and image[y][x + 1] <= 0):
                continue

            image[y][x] = sys.maxsize
            start = Point(x, y)
            gp_path = [start]

            dr = Direction.UP
            p = Point(start.X, start.Y - 1)

            while True:
                if dr == Direction.UP:
                    if image[p.Y][p.X] > 0:
                        image[p.Y][p.X] = sys.maxsize

                        if image[p.Y][p.X + 1] <= 0:
                            p = Point(p.X, p.Y - 1)
                        else:
                            gp_path.append(p)
                            dr = Direction.RIGHT
                            p = Point(p.X + 1, p.Y)
                    else:
                        p = Point(p.X, p.Y + 1)
                        gp_path.append(p)
                        dr = Direction.LEFT
                        p = Point(p.X - 1, p.Y)

                elif dr == Direction.DOWN:
                    if image[p.Y][p.X] > 0:
                        image[p.Y][p.X] = sys.maxsize

                        if image[p.Y][p.X - 1] <= 0:
                            p = Point(p.X, p.Y + 1)
                        else:
                            gp_path.append(p)
                            dr = Direction.LEFT
                            p = Point(p.X - 1, p.Y)
                    else:
                        p = Point(p.X, p.Y - 1)
                        gp_path.append(p)
                        dr = Direction.RIGHT
                        p = Point(p.X + 1, p.Y)

                elif dr == Direction.LEFT:
                    if image[p.Y][p.X] > 0:
                        image[p.Y][p.X] = sys.maxsize

                        if image[p.Y - 1][p.X] <= 0:
                            p = Point(p.X - 1, p.Y)
                        else:
                            gp_path.append(p)
                            dr = Direction.UP
                            p = Point(p.X, p.Y - 1)
                    else:
                        p = Point(p.X + 1, p.Y)
                        gp_path.append(p)
                        dr = Direction.DOWN
                        p = Point(p.X, p.Y + 1)

                elif dr == Direction.RIGHT:
                    if image[p.Y][p.X] > 0:
                        image[p.Y][p.X] = sys.maxsize

                        if image[p.Y + 1][p.X] <= 0:
                            p = Point(p.X + 1, p.Y)
                        else:
                            gp_path.append(p)
                            dr = Direction.DOWN
                            p = Point(p.X, p.Y + 1)
                    else:
                        p = Point(p.X - 1, p.Y)
                        gp_path.append(p)
                        dr = Direction.UP
                        p = Point(p.X, p.Y - 1)
                else:
                    raise RuntimeError()

                if p == start:
                    break

            gp_paths.append(gp_path)

    return gp_paths
