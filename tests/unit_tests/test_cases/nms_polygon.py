import numpy as np
from engine.objects.polygon import Polygon
from engine.objects.bbox_detections import BBoxDetections
from engine.objects.polygon_detections import PolygonDetections

# regular convex polygons
# 1. square as a polygon. 8 points.  area = 50
POLYGON1 = Polygon(points=((0, 0), (0, 5), (0, 10), (5, 10),
                           (10, 10), (10, 5), (10, 0), (5, 0)))
    
# 2. rectangle as a polygon. 4 points. area = 500
POLYGON2 = Polygon(points=((0, 0), (0, 10), (50, 10), (50, 0)))
    
# 3. equilateral triangle as polygon. 3 points. area =
POLYGON3 = Polygon(points=((0, 0), (3, np.sqrt(27)), (6, 0))),
    
# irregular polygons
# 4. rectangle as a polygon. non-uniform sampling. 9 points. area = 500
POLYGON4 = Polygon(points=((0, 0), (0, 5), (0, 10), (10, 10), (40, 10),
                           (50, 10), (50, 0), (25, 0), (13, 0)))
    
# 5. right angle triangle as polygon. 3 points
POLYGON5 = Polygon(points=((0, 3), (4, 0), (0, 0)))
    
# non-convex polygons
# 6. arrow <===>
# area = area(rect) + 2 * area(traingle)
#      = 6 + 2 * 4 = 14    
POLYGON6 = Polygon(points=((0, 2), (2, 4), (2, 3), (5, 3), (5, 4),
                           (7, 2), (5, 0), (5, 1), (2, 1), (2, 0)))


POLYGON7 = Polygon(points=((3, 0), (3, 2), (3, 2), (3, 4), (3, 4),
                           (4, 4), (4, 4), (4, 2), (4, 2), (4, 0)))
    

POLYGON8 = Polygon(points=((2, 1.5), (2, 2.5), (3, 2.5), (4, 2.5),
                           (5, 2.5), (5, 1.5), (4, 1.5), (3, 1.5)))
    

# 100 % overlap  
NMS_POLYGON1 = [
    PolygonDetections(POLYGON1.vertices, 0.1, 0),
    PolygonDetections(POLYGON1.vertices, 0.2, 1),
    PolygonDetections(POLYGON1.vertices, 0.3, 10),
    PolygonDetections(POLYGON1.vertices, 0.4, 3),
    PolygonDetections(POLYGON1.vertices, 0.5, 2),
]

# 100 % overlap
NMS_POLYGON2 = [
    PolygonDetections(POLYGON2.vertices, 0.1, 0),
    PolygonDetections(POLYGON2.vertices, 0.1, 1),
    PolygonDetections(POLYGON2.vertices, 0.1, 10),
    PolygonDetections(POLYGON2.vertices, 0.1, 3),
    PolygonDetections(POLYGON2.vertices, 0.1, 2),
]


# 100 % overlap
NMS_POLYGON3 = [
    PolygonDetections(POLYGON4.vertices, 0.1, 0),
    PolygonDetections(POLYGON4.vertices, 0.9, 1),
    PolygonDetections(POLYGON4.vertices, 0.3, 10),
    PolygonDetections(POLYGON4.vertices, 0.4, 3),
    PolygonDetections(POLYGON4.vertices, 0.5, 2),
]

# 100 % overlap
NMS_POLYGON4 = [
    PolygonDetections(POLYGON6.vertices, 0.1, 0),
    PolygonDetections(POLYGON6.vertices, 0.9, 10),
    PolygonDetections(POLYGON6.vertices, 0.4, 3),
]


# overlapping polygon (< 100%)
# iou: 2/16
NMS_POLYGON5 = [
    PolygonDetections(POLYGON6.vertices, 0.1, 0),
    PolygonDetections(POLYGON7.vertices, 0.9, 10),
]


# polygon in a polygon
# iou: 3/14
NMS_POLYGON6 = [
    PolygonDetections(POLYGON6.vertices, 0.1, 0),
    PolygonDetections(POLYGON8.vertices, 0.9, 10),

]


# 100% overlap
NMS_SCENARIO1 = {
    "detections": NMS_POLYGON1,
    "iou_thresh": 0.00001,
    "score_thresh": 0.0,
    "expected_detections": 1
}

NMS_SCENARIO2 = {
    "detections": NMS_POLYGON2,
    "iou_thresh": 0.00001,
    "score_thresh": 0.0,
    "expected_detections": 1
}

NMS_SCENARIO3 = {
    "detections": NMS_POLYGON3,
    "iou_thresh": 0.00001,
    "score_thresh": 0.0,
    "expected_detections": 1
}

NMS_SCENARIO4 = {
    "detections": NMS_POLYGON4,
    "iou_thresh": 0.00001,
    "score_thresh": 0.0,
    "expected_detections": 1
}

# score thresholding
NMS_SCENARIO5 = {
    "detections": NMS_POLYGON3,
    "iou_thresh": 0.00001,
    "score_thresh": 0.900001,
    "expected_detections": 0
}


# iou thresholding
NMS_SCENARIO6 = {
    "detections": NMS_POLYGON3,
    "iou_thresh": 0.0,
    "score_thresh": 0.0,
    "expected_detections": 1
}


NMS_SCENARIO7 = {
    "detections": NMS_POLYGON5,
    "iou_thresh": 0.124,
    "score_thresh": 0.0,
    "expected_detections": 1
}


NMS_SCENARIO8 = {
    "detections": NMS_POLYGON5,
    "iou_thresh": 0.125,
    "score_thresh": 0.0,
    "expected_detections": 1
}

NMS_SCENARIO9 = {
    "detections": NMS_POLYGON5,
    "iou_thresh": 0.126,
    "score_thresh": 0.0,
    "expected_detections": 2
}


NMS_SCENARIO10 = {
    "detections": NMS_POLYGON6,
    "iou_thresh": 0.1,
    "score_thresh": 0.05,
    "expected_detections": 1
}


POLYGON_NMS_SCENARIOS = [
    
    NMS_SCENARIO1,
    NMS_SCENARIO2,
    NMS_SCENARIO3,
    NMS_SCENARIO4,
    NMS_SCENARIO5,
    # NMS_SCENARIO6,
    # NMS_SCENARIO7,
    # NMS_SCENARIO8,
    # NMS_SCENARIO9,
    # NMS_SCENARIO10,
    
]


INVALID_POLYGON_NMS1 = [

    BBoxDetections(0, 0, 10, 10, 0.50, 0),
    BBoxDetections(0, 0, 2, 2, 0.55, 0),

]

INVALID_POLYGON_NMS = [
    INVALID_POLYGON_NMS1
    
]