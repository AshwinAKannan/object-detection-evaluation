import math
import shapely
import numpy as np


from engine.objects.bbox import BBox
from engine.objects.polygon import Polygon


def intersection_over_union(bbox1: BBox, bbox2: BBox) -> float:
    """
    intersection_over_union

    Computes Intersection of Union given 2 BBox

    Args:
        bbox1 (BBox): box 1 with bottom-left, top-right coordinates
        bbox2 (BBox): box 2 with bottom-left, top-right coordinates

    Returns:
        float: intersection of union of 2 bounding boxes
    """
    area_bbox1: float = bbox1.area()
    area_bbox2: float = bbox2.area()
    
    # find intersection of 2 bbox
    # bottom-left x, y & top-right x, y of intersection box
    bl_x: float = max(bbox1.x1, bbox2.x1) 
    bl_y: float = max(bbox1.y1, bbox2.y1)
    tr_x: float = min(bbox1.x2, bbox2.x2)
    tr_y: float = min(bbox1.y2, bbox2.y2)
    
    h_intersection: float = (tr_y - bl_y)
    w_intersection: float = (tr_x - bl_x)
    
    if h_intersection > 0 and w_intersection > 0:
        intersection_area: float = h_intersection * w_intersection
        union_area: float = area_bbox1 + area_bbox2 - intersection_area
        
        iou: float = intersection_area / union_area
        # print(f"intersection_area: {intersection_area}, union_area: {union_area}, iou: {iou}")
    
    else:
        # if either height or width of intersecting box is 0,
        # iou will be 0
        return 0.0
    
    assert iou > 0.0
    
    return iou


def intersection_over_union_polygon(polygon1: Polygon, polygon2: Polygon):
    
    polygon1 = shapely.geometry.Polygon(polygon1.vertices)

    polygon2 = shapely.geometry.Polygon(polygon2.vertices)
    
    print(polygon2)
    intersection_area = polygon1.intersection(polygon2).area
    print(intersection_area)
    union_area = polygon1.union(polygon2).area
    
    iou = intersection_area / union_area
    
    return iou

# def calculate_polygon_intersection(polygon1: Polygon, polygon2: Polygon):
#     # Find the intersection points of two polygons
#     intersection_points = []

#     for i in range(polygon1.num_vertices):
#         for j in range(polygon2.num_vertices):
#             x1, y1 = polygon1.vertices[i]
#             x2, y2 = polygon1.vertices[(i + 1) % polygon1.num_vertices]
#             x3, y3 = polygon2.vertices[j]
#             x4, y4 = polygon2.vertices[(j + 1) % polygon2.num_vertices]

#             # Check if line segments (x1, y1)-(x2, y2) and (x3, y3)-(x4, y4) intersect
#             den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
#             if den != 0:
#                 t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
#                 u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

#                 if 0 <= t <= 1 and 0 <= u <= 1:
#                     intersection_x = x1 + t * (x2 - x1)
#                     intersection_y = y1 + t * (y2 - y1)
#                     intersection_point = (intersection_x, intersection_y)

#                     # Check if the intersection point is not already in the list
#                     if intersection_point not in intersection_points:
#                         intersection_points.append(intersection_point)

#     # Calculate centroid of polygon1 to use as the reference point for sorting
#     centroid_x = sum(x for x, _ in polygon1.vertices) / polygon1.num_vertices
#     centroid_y = sum(y for _, y in polygon1.vertices) / polygon1.num_vertices

#     # Sort intersection points based on their angles relative to the centroid
#     intersection_points.sort(key=lambda point: math.atan2(point[1] - centroid_y, point[0] - centroid_x))

#     return intersection_points


# def polygon_intersection_over_union(polygon1: Polygon, polygon2: Polygon) -> float:
#     # WILL ACURATELY WORK ONLY FOR CONVEX POLYGONS
#     intersection_points: list = calculate_polygon_intersection(polygon1, polygon2)
#     print(intersection_points)
#     intersection_area: float = Polygon(intersection_points).area()
#     print(f"intersection_area: {intersection_area}")
#     union_area: float = polygon1.area() + polygon2.area() - intersection_area

#     if union_area == 0:
#         return 0.0

#     iou_value: float = intersection_area / union_area
#     return iou_value


# class PolygonIoU:

    # @staticmethod
    # def on_segment(p, q, r) -> bool:
    #     """Check if point q lies on line segment 'pr'"""
    #     if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and 
    #         q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
    #         return True
    #     return False

    # @staticmethod
    # def orientation(p, q, r):
    #     """Find orientation of ordered triplet (p, q, r).
    #     Returns 0 if p, q and r are collinear, 1 if Clockwise, 2 if Counterclockwise"""
    #     val = ((q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]))
    #     if val == 0:
    #         return 0
    #     return 1 if val > 0 else 2

    # @staticmethod
    # def do_intersect(p1, q1, p2, q2) -> bool:
    #     """Check if line segments 'p1q1' and 'p2q2' intersect."""
    #     o1 = PolygonIoU.orientation(p1, q1, p2)
    #     o2 = PolygonIoU.orientation(p1, q1, q2)
    #     o3 = PolygonIoU.orientation(p2, q2, p1)
    #     o4 = PolygonIoU.orientation(p2, q2, q1)

    #     # General case
    #     if o1 != o2 and o3 != o4:
    #         return True

    #     # Special Cases
    #     if o1 == 0 and PolygonIoU.on_segment(p1, p2, q1):
    #         return True
    #     if o2 == 0 and PolygonIoU.on_segment(p1, q2, q1):
    #         return True
    #     if o3 == 0 and PolygonIoU.on_segment(p2, p1, q2):
    #         return True
    #     if o4 == 0 and PolygonIoU.on_segment(p2, q1, q2):
    #         return True

    #     return False

    # # @staticmethod
    # # def clockwise_angle_and_distance(point, origin):
    # #     """Compute the clockwise angle and distance from a given origin to the point."""
    # #     refvec = [1, 1]
    # #     vector = [point[0] - origin[0], point[1] - origin[1]]
    # #     lenvector = math.hypot(*vector)
    # #     if lenvector == 0:
    # #         return -math.pi, 0

    # #     normalized = [vector[0] / lenvector, vector[1] / lenvector]
    # #     dotprod = normalized[0] * refvec[0] + normalized[1] * refvec[1]
    # #     diffprod = refvec[1] * normalized[0] - refvec[0] * normalized[1]
    # #     angle = math.atan2(diffprod, dotprod)
    # #     if angle < 0:
    # # #         return 2 * math.pi + angle, lenvector
    # # #     return angle, lenvector

    # # @staticmethod
    # # def clockwise_angle_and_distance(point, origin):
    # #     """Compute the clockwise angle and distance from a given origin to the point."""
    # #     refvec = [0, 1]  # Upward-pointing reference vector

    # #     # Compute vector from origin to point
    # #     vector = [point[0] - origin[0], point[1] - origin[1]]
    # #     lenvector = math.hypot(*vector)
    # #     normalized = [vector[0] / lenvector, vector[1] / lenvector] if lenvector != 0 else [0, 0]

    # #     # Compute the dot product and determinant for angle calculation
    # #     dotprod = normalized[0] * refvec[0] + normalized[1] * refvec[1]
    # #     det = normalized[0] * refvec[1] - normalized[1] * refvec[0]
    # #     angle = math.atan2(det, dotprod)

    # #     # Adjust the angle for sorting
    # #     if angle < 0:
    # #         angle += 2 * math.pi

    # #     # Sort primarily by angle, then by y-coordinate for same angle
    # #     return (angle, -point[1] if normalized[0] == 0 else lenvector)
    
    # @staticmethod
    # def sort_coordinates(list_of_xy_coords):
    #     np_coords = np.array(list_of_xy_coords)
    #     cx, cy = np_coords.mean(axis=0)
    #     x, y = np_coords[:, 0], np_coords[:, 1]
    #     angles = np.arctan2(x - cx, y - cy)
    #     indices = np.argsort(angles)
    #     sorted_coords = np_coords[indices]
    #     return sorted_coords.tolist()

    # @staticmethod
    # def line_intersection(p1, q1, p2, q2):
    #     """Find the intersection point of two line segments p1q1 and p2q2, if they intersect."""
    #     A1 = q1[1] - p1[1]
    #     B1 = p1[0] - q1[0]
    #     C1 = A1 * p1[0] + B1 * p1[1]
    #     A2 = q2[1] - p2[1]
    #     B2 = p2[0] - q2[0]
    #     C2 = A2 * p2[0] + B2 * p2[1]
    #     determinant = A1 * B2 - A2 * B1

    #     if determinant == 0:
    #         return None  # parallel lines
    #     else:
    #         x = (B2 * C1 - B1 * C2) / determinant
    #         y = (A1 * C2 - A2 * C1) / determinant
    #         return (x, y)

    # @staticmethod
    # def centroid(points):
    #     """Compute the centroid of a polygon defined by points."""
    #     x = [p[0] for p in points]
    #     y = [p[1] for p in points]
    #     length = len(points)
    #     centroid_x = sum(x) / length
    #     centroid_y = sum(y) / length
    #     return (centroid_x, centroid_y)
    
    # @staticmethod
    # def point_inside_polygon(point, polygon) -> bool:
    #     """Check if a point is inside a polygon."""
    #     # A big value
    #     INF = 10000

    #     # Count intersections of the above line with sides of polygon
    #     count = 0
    #     n = len(polygon)
    #     for i in range(n):
    #         next = (i + 1) % n
    #         if PolygonIoU.do_intersect(polygon[i], polygon[next], point, (INF, point[1])):
    #             if PolygonIoU.orientation(polygon[i], point, polygon[next]) == 0:
    #                 return PolygonIoU.on_segment(polygon[i], point, polygon[next])
    #             count += 1

    #     return count % 2 == 1
    
    # @staticmethod
    # def order_points_clockwise(points):
    #     """Order points in a clockwise manner."""
    #     center = PolygonIoU.centroid(points)
    #     return PolygonIoU.clockwise_angle_and_distance(points, center)
    
    # @staticmethod
    # def remove_duplicates(points):
    #     """Remove duplicate points from the list."""
    #     unique_points = []
    #     for point in points:
    #         if point not in unique_points:
    #             unique_points.append(point)
    #     return unique_points

    # @staticmethod
    # def polygon_intersection_over_union(polygon1: Polygon, polygon2: Polygon) -> list:
    #     # Step 1: Find Intersection Points
    #     intersection_points = []
    #     for i in range(polygon1.num_vertices):
    #         p1 = polygon1.vertices[i]
    #         q1 = polygon1.vertices[(i + 1) % polygon1.num_vertices]
    #         for j in range(polygon2.num_vertices):
    #             p2 = polygon2.vertices[j]
    #             q2 = polygon2.vertices[(j + 1) % polygon2.num_vertices]
    #             print(p1, q1, p2, q2)
    #             if PolygonIoU.do_intersect(p1, q1, p2, q2):
    #                 intersection = PolygonIoU.line_intersection(p1, q1, p2, q2)
    #                 if intersection and intersection not in intersection_points:
    #                     print(intersection)
    #                     intersection_points.append(intersection)
    #     print("################################")
    #     print(intersection_points)
    #     print("################################")
    #     # a=b
    #     # Step 2: Include Vertices Inside the Other Polygon
    #     for point in polygon1.vertices:
    #         if PolygonIoU.point_inside_polygon(point, polygon2.vertices):
    #             intersection_points.append(point)
    #     for point in polygon2.vertices:
    #         if PolygonIoU.point_inside_polygon(point, polygon1.vertices):
    #             intersection_points.append(point)
    #     # print(intersection_points)
    #     # Step 3: Remove Duplicates
    #     intersection_points = PolygonIoU.remove_duplicates(intersection_points)
        
    #     # # Step 4: Order the Points Clockwise
    #     # intersection_points = PolygonIoU.order_points_clockwise(intersection_points)
    #     intersection_points = PolygonIoU.sort_coordinates(intersection_points)
    #     print("2....################################")
    #     print(intersection_points)
    #     print("################################")
        
    #     return True
    