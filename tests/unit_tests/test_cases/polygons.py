import numpy as np

from engine.objects.polygon import Polygon

from typing import List

POLYGONS: List = [
    
    # regular polygons
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
]

NUM_VERTICES: List[int] = [
    8,
    4,
    3,
    9,
    3,
]

POLYGON_AREAS: List[float] = [
    100.0,
    500.0,
    np.sqrt(3) * 9,
    500.0,
    6.0,
]

INVALID_POLYGON_VERTICES: List = [
    # 1. Negative coordinates
    ((0, -3), (4, 0), (0, 0)),
    ((-1, -1), (-2, -2), (-3, -3)),
]
