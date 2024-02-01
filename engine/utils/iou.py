import math
import shapely
import numpy as np


from engine.objects.bbox import BBox
from engine.objects.polygon import Polygon


# def intersection_over_union(bbox1: BBox, bbox2: BBox) -> float:
#     """
#     intersection_over_union

#     Computes Intersection of Union given 2 BBox

#     Args:
#         bbox1 (BBox): box 1 with bottom-left, top-right coordinates
#         bbox2 (BBox): box 2 with bottom-left, top-right coordinates

#     Returns:
#         float: intersection of union of 2 bounding boxes
#     """
    
#     assert type(bbox1) == BBox and type(bbox2) == BBox
    
#     area_bbox1: float = bbox1.area
#     area_bbox2: float = bbox2.area
    
#     # find intersection of 2 bbox
#     # bottom-left x, y & top-right x, y of intersection box
#     bl_x: float = max(bbox1.x1, bbox2.x1) 
#     bl_y: float = max(bbox1.y1, bbox2.y1)
#     tr_x: float = min(bbox1.x2, bbox2.x2)
#     tr_y: float = min(bbox1.y2, bbox2.y2)
    
#     h_intersection: float = (tr_y - bl_y)
#     w_intersection: float = (tr_x - bl_x)
    
#     if h_intersection > 0 and w_intersection > 0:
#         intersection_area: float = h_intersection * w_intersection
#         union_area: float = area_bbox1 + area_bbox2 - intersection_area
        
#         iou: float = intersection_area / union_area
#         # print(f"intersection_area: {intersection_area}, union_area: {union_area}, iou: {iou}")
    
#     else:
#         # if either height or width of intersecting box is 0,
#         # iou will be 0
#         return 0.0
    
#     assert iou > 0.0
    
#     return iou


# def intersection_over_union_polygon(polygon1: Polygon, polygon2: Polygon):
    
#     assert type(polygon1) == Polygon and type(polygon2) == Polygon
    
#     polygon1 = shapely.geometry.Polygon(polygon1.vertices)
#     polygon2 = shapely.geometry.Polygon(polygon2.vertices)
    
#     # print(polygon2)
#     intersection_area: float = polygon1.intersection(polygon2).area
#     # print(intersection_area)
#     union_area: float = polygon1.union(polygon2).area
    
#     iou: float = intersection_area / union_area
    
#     return iou