from engine.objects.bbox_detection import BBoxDetection
from engine.utils.nms import NMS


class BBoxNMS(NMS):
    
    def adjust_detections(self, detections, shift=True):
        
        """Adjust detections by shifting or unshifting based on the 'shift' parameter.
        
        Args:
            detections (list): List of detection objects.
            shift (bool): True to shift bounding boxes, False to unshift them.
        
        Returns:
            list: The adjusted list of detection objects.
        """
        if self.class_agnostic is False:
            for detection in detections:
                offset = 4096 * detection.class_id if shift else -4096 * detection.class_id
                detection.bbox.x1 += offset
                detection.bbox.y1 += offset
                detection.bbox.x2 += offset
                detection.bbox.y2 += offset
                
        return detections
    
    def check_detections_class(self, detections) -> None:
        for detection in detections:
            assert isinstance(detection, BBoxDetection)