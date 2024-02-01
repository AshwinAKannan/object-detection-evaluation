
from engine.objects.bbox_detection import BBoxDetection
from engine.objects.polygon_detection import PolygonDetection


NMS_BBOXES1 = [
    
    # 100 % overlap
    BBoxDetection(0, 0, 10, 10, 0.9, 0), 
    BBoxDetection(0, 0, 10, 10, 0.99, 1), 
    BBoxDetection(0, 0, 10, 10, 0.6, 2), 
    BBoxDetection(0, 0, 10, 10, 0.2, 3), 
    BBoxDetection(0, 0, 10, 10, 0.8, 4), 
    
]


NMS_BBOXES2 = [

    BBoxDetection(0, 0, 10, 10, 0.9, 0), 
    BBoxDetection(5, 0, 15, 10, 0.9, 1), 
    
]


NMS_BBOXES3 = [

    BBoxDetection(0, 0, 10, 10, 0.51, 0), 
    BBoxDetection(2, 2, 8, 8, 0.9, 1), 
    
]


# 100% overlap
NMS_SCENARIO1 = {
    "detections": NMS_BBOXES1,
    "iou_thresh": 0.00001,
    "score_thresh": 0.0,
    "expected_detections": 1
}


# test score thresholding
NMS_SCENARIO2 = {
    "detections": NMS_BBOXES1,
    "iou_thresh": 0.1,
    "score_thresh": 1.0,
    "expected_detections": 0
}

# partial overlap
NMS_SCENARIO3 = {
    "detections": NMS_BBOXES2,
    "iou_thresh": 0.1,
    "score_thresh": 0.5,
    "expected_detections": 1
}


# partial overlap. high iou thresh
NMS_SCENARIO4 = {
    "detections": NMS_BBOXES2,
    "iou_thresh": 0.9,
    "score_thresh": 0.5,
    "expected_detections": 2
}


# box in a box
NMS_SCENARIO5 = {
    "detections": NMS_BBOXES3,
    "iou_thresh": 0.35,
    "score_thresh": 0.5,
    "expected_detections": 1
}

# box in a box
# iou thresh should be LESS THAN threshold
NMS_SCENARIO6 = {
    "detections": NMS_BBOXES3,
    "iou_thresh": 0.36,
    "score_thresh": 0.5,
    "expected_detections": 1
}

# box in a box
NMS_SCENARIO7 = {
    "detections": NMS_BBOXES3,
    "iou_thresh": 0.37,
    "score_thresh": 0.5,
    "expected_detections": 2
}


BBOX_NMS_SCENARIOS = [
    
    NMS_SCENARIO1,
    NMS_SCENARIO2,
    NMS_SCENARIO3,
    NMS_SCENARIO4,
    NMS_SCENARIO5,
    NMS_SCENARIO6,
    NMS_SCENARIO7
    
]


INVALID_BBOXES_NMS1 = [

    PolygonDetection(((0, 0), (10, 10), (10, 5)), 0.50, 0), 
    PolygonDetection(((0, 0), (2, 2), (10, 8)), 0.55, 0), 
    
]

INVALID_BBOX_NMS = [
    INVALID_BBOXES_NMS1
    
]