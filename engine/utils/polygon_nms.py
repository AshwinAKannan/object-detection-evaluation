from engine.objects.polygon_detection import PolygonDetection
from engine.utils.nms import NMS


class PolygonNMS(NMS):
    
    def adjust_detections(self, detections, shift=True):
        """Adjust detections by shifting or unshifting based on the 'shift' parameter.
        
        Args:
            detections (list): List of detection objects.
            shift (bool): True to shift bounding boxes, False to unshift them.
        
        Returns:
            list: The adjusted list of detection objects.
        """
        
        if self.class_agnostic is False:
            # TODO
            raise NotImplementedError
            for detection in detections:
                pass
                
        return detections
    
    def check_detections_class(self, detections):
        for detection in detections:
            assert isinstance(detection, PolygonDetection)