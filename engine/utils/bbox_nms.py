
from engine.utils.nms import NMS
from engine.objects.bbox_detections import BBoxDetections
from engine.utils.iou import intersection_over_union


class BBoxNMS(NMS):

    def iou_calculator(self, a, b):
        assert type(a) == BBoxDetections and type(b) == BBoxDetections
        
        iou: float = intersection_over_union(a.bbox, b.bbox)
        
        return iou