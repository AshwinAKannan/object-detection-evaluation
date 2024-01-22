
from engine.utils.nms import NMS
from engine.objects.polygon_detections import PolygonDetections
from engine.utils.iou import intersection_over_union_polygon


class PolygonNMS(NMS):

    def iou_calculator(self, a, b):
        assert type(a) == PolygonDetections and type(b) == PolygonDetections
        
        iou: float = intersection_over_union_polygon(a.polygon, b.polygon)
        
        return iou