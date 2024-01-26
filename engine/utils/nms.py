from abc import ABC, abstractmethod

from typing import List


class NMS(ABC):
    # TODO [Ashwin]: Check if it's worth speeding this up with MT
    # TODO [Ashwin]: Unit test this class
    
    # Notes to self [Ashwin]
    # 1. Write a separate class agnostic NMS that uses this class
    # do not try to update this class
    
    # 2. torchvision.ops.nms performs class-agnostic nms
    # So, this implementation should largely match torchvision.ops.nms
    # leaving aside minor differences, if any
    
    def __init__(self, multi_thread: bool = False) -> None:
        self.multi_thread: bool = multi_thread  # not implemented
        
        # this implementation is meant to handle only class agnostic NMS
        self.class_agnostic: bool = True
    
    def apply_nms(self,
                  detections: List,
                  score_threshold: float,
                  iou_threshold: float) -> List:
        
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
            
            # for d in detections:
            #     print(d.objectness_score)
            
            selected_detections: list = []
            
            # until the pool runs out of detections...
            while len(detections) > 0:
                
                # always retain the detection with the highest score
                current_detection = detections.pop(0)

                selected_detections.append(current_detection)
                
                # check IOU of current detection with all other detections in the pool
                # discard detections from which have high overlap
                # retain detections with smaller overlap (< iou_threshold) in the pool
                remaining_detections: list = []
                for detection in detections:
                    iou: float = self.iou_calculator(current_detection, detection)
                    
                    if iou < iou_threshold:
                        remaining_detections.append(detection)
                
                detections = remaining_detections
        else:
            pass
        
        return selected_detections
    
    def apply_class_nms(self,
                        detections: List,
                        score_threshold: float,
                        iou_threshold: float) -> List:
        
        if len(detections) == 0:
            return []
        
        detections = [detection
                      for detection in detections
                      if detection.objectness_score >= score_threshold]
        
        for detection in detections:
            detection.bbox.x1 = detection.bbox.x1 + 4096 * detection.class_id
            detection.bbox.y1 = detection.bbox.y1 + 4096 * detection.class_id
            detection.bbox.x2 = detection.bbox.x2 + 4096 * detection.class_id
            detection.bbox.y2 = detection.bbox.y2 + 4096 * detection.class_id

        if len(detections) == 0:
            return []
        
        # If class_agnostic is True, consider all detections as one class
        if self.class_agnostic:
            
            # Sort detections by objectness score in descending order
            detections.sort(key=lambda x: x.objectness_score, reverse=True)
            
            # for d in detections:
            #     print(d.objectness_score)
            
            selected_detections: list = []
            
            # until the pool runs out of detections...
            while len(detections) > 0:
                
                # always retain the detection with the highest score
                current_detection = detections.pop(0)

                selected_detections.append(current_detection)
                
                # check IOU of current detection with all other detections in the pool
                # discard detections from which have high overlap
                # retain detections with smaller overlap (< iou_threshold) in the pool
                remaining_detections: list = []
                for detection in detections:
                    iou: float = self.iou_calculator(current_detection, detection)
                    
                    if iou < iou_threshold:
                        remaining_detections.append(detection)
                
                detections = remaining_detections
        else:
            pass
        
        for detection in selected_detections:
            detection.bbox.x1 = detection.bbox.x1 - 4096 * detection.class_id
            detection.bbox.y1 = detection.bbox.y1 - 4096 * detection.class_id
            detection.bbox.x2 = detection.bbox.x2 - 4096 * detection.class_id
            detection.bbox.y2 = detection.bbox.y2 - 4096 * detection.class_id
        return selected_detections
    
    @abstractmethod
    def iou_calculator(self, a, b):
        return
