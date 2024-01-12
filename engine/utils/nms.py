from engine.utils.iou import intersection_over_union
from engine.objects.bbox_detections import BBoxDetections

from typing import List


class NMS:
    # TODO [Ashwin]: Check if it's worth speeding this up with MT
    # TODO [Ashwin]: Unit test this class
    
    # Notes to self [Ashwin]
    # 1. Write a separate class agnostic NMS that uses this class
    # do not try to update this class
    
    # 2. torchvision.ops.nms performs class-agnostic nms
    # So, this implement should largely match torchvision.ops.nms
    # leaving aside minor differences, if any
    
    def __init__(self, multi_thread: bool = False, ) -> None:
        self.multi_thread: bool = multi_thread  # not implemented
    
    def apply_nms(self,
                  detections: List[BBoxDetections],
                  score_threshold: float,
                  iou_threshold: float) -> List[BBoxDetections]:
        
        if len(detections) == 0:
            return []
        
        detections = [detection
                      for detection in detections
                      if detection.objectness_score >= score_threshold]
    
        if len(detections) == 0:
            return []
        
        # If class_agnostic is True, consider all detections as one class
        if self.class_agnostic:
            
            # Sort detections by objectness score in descending order
            detections.sort(key=lambda x: x.objectness_score, reverse=True)
            
            selected_detections: list = []
            
            # until the pool runs out of detections...
            while len(detections) > 0:
                
                # always retain the detection with the highest score
                current_detection: BBoxDetections = detections.pop()
                selected_detections.append(current_detection)
                
                # check IOU of current detection with all other detections in the pool
                # discard detections from which have high overlap
                # retain detections with smaller overlap (< iou_threshold) in the pool
                remaining_detections: list = []
                for detection in detections:
                    iou: float = intersection_over_union(
                        current_detection.bbox,
                        detection.bbox)
                    
                    if iou < iou_threshold:
                        remaining_detections.append(detection)
                
                detections = remaining_detections
        else:
            pass
        
        return selected_detections
