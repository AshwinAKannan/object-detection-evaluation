import numpy as np

from engine.objects.polygon import Polygon

from typing import List

POLYGONS: List = [
    
    # regular convex polygons
    # 1. square as a polygon. 8 points
    Polygon(points=((0, 0), (0, 5), (0, 10), (5, 10),
                    (10, 10), (10, 5), (10, 0), (5, 0))),  # area = 50
    
    # 2. rectangle as a polygon. 4 points
    Polygon(points=((0, 0), (0, 10), (50, 10), (50, 0))),  # area = 500
    
    # 3. equilateral triangle as polygon. 3 points
    Polygon(points=((0, 0), (3, np.sqrt(27)), (6, 0))),  # area =
    
    # irregular polygons
    # 4. rectangle as a polygon. non-uniform sampling. 9 points
    Polygon(points=((0, 0), (0, 5), (0, 10),
            (10, 10), (40, 10), (50, 10),
            (50, 0), (25, 0), (13, 0))),  # area = 500
    
    # 5. right angle triangle as polygon. 3 points
    Polygon(points=((0, 3), (4, 0), (0, 0))),
    
    # non-convex polygons
    # 6. arrow <===>
    # area = area(rect) + 2 * area(traingle)
    #      = 6 + 2 * 4 = 14    
    Polygon(points=((0, 2), (2, 4), (2, 3), (5, 3), (5, 4),
                    (7, 2), (5, 0), (5, 1), (2, 1), (2, 0))),
    
]

NUM_VERTICES: List[int] = [
    8,
    4,
    3,
    9,
    3,
    10,
]

POLYGON_AREAS: List[float] = [
    100.0,
    500.0,
    np.sqrt(3) * 9,
    500.0,
    6.0,
    14,
]

INVALID_POLYGON_VERTICES: List = [
    # 1. Negative coordinates
    ((0, -3), (4, 0), (0, 0)),
    ((-1, -1), (-2, -2), (-3, -3)),
]

OVERLAPPING_POLYGONS = [
    
    # 100% overlap
    [Polygon(points=((0, 2), (2, 4), (2, 3), (5, 3), (5, 4),
                     (7, 2), (5, 0), (5, 1), (2, 1), (2, 0))),
     Polygon(points=((0, 2), (2, 4), (2, 3), (5, 3), (5, 4),
                     (7, 2), (5, 0), (5, 1), (2, 1), (2, 0)))],
    
    
    
    # # partial intersection
    # non-convex (arrow), convex (rectangle)
    [Polygon(points=((0, 2), (2, 4), (2, 3), (5, 3), (5, 4),
                     (7, 2), (5, 0), (5, 1), (2, 1), (2, 0))),
     Polygon(points=((3, 0), (3, 2), (3, 2), (3, 4), (3, 4),
                     (4, 4), (4, 4), (4, 2), (4, 2), (4, 0)))],
    
    # polygon inside a polygon
    # non-convex (arrow), convex (rectangle)
    [Polygon(points=((0, 2), (2, 4), (2, 3), (5, 3), (5, 4),
                     (7, 2), (5, 0), (5, 1), (2, 1), (2, 0))),
     Polygon(points=((2, 1.5), (2, 2.5), (3, 2.5), (4, 2.5),
                     (5, 2.5), (5, 1.5), (4, 1.5), (3, 1.5)))],
    

]
OVERLAPPING_POLYGON_INTERSECTION = [
    14.0,
    2.0,
    3.0
]
OVERLAPPING_POLYGON_UNION = [
    14,
    14 + 4 - 2,
    14 + 3 - 3
]