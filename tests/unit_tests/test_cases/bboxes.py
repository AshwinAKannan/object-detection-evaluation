from engine.objects.bbox import BBox

BBOXES = [  
    BBox(10, 10, 50, 50), 
    BBox(0, 0, 60, 60),
    BBox(0, 0, 100, 100),
    BBox(0, 0, 0, 0)
]

BBOX_AREAS = [
    1600,
    3600,
    10000,
    0]

OVERLAPPING_BBOXES = [
    # no overlap
    [BBox(0, 0, 10, 10),  # area = 100
     BBox(50, 50, 60, 60)],  # area = 100
    
    # no overlap, corners touching
    [BBox(10, 10, 20, 20),  # area = 100
     BBox(20, 20, 35, 35)],  # area = 225
    
    # bbox within a bbox
    [BBox(10, 10, 50, 50),  # area = 1600
     BBox(0, 0, 60, 60)],  # area = 3600
    
    # 100% overlap
    [BBox(0, 0, 20, 20),  # area = 400
     BBox(0, 0, 20, 20)],  # area = 400
    
    # partial overlap
    [BBox(0, 0, 10, 10),  # area = 100
     BBox(5, 5, 20, 20)],  # area = 225
]

OVERLAPPING_BBOXES_INTERSECTION = [
    0,
    0,
    1600,
    400,
    25
]

OVERLAPPING_BBOXES_UNION = [
    200,
    325,
    3600,
    400,
    300
]

INVALID_BBOXES = [
    # (x1, y1, x2, y2)
    
    # 1. Negative coordinates
    (-10, 10, 10, 10),
    (-10, -10, -10, -10),
    (-10, -7, 0, 0),
    
    # 2. x1 > x2
    (10, 3, 5, 5),
    
    # 3. y1 > y2
    (3, 10, 5, 5),
    
    # x2 > x1 and y2 > y1
    (10, 10, 5, 5),
]

