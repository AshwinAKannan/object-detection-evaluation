from abc import ABC, abstractmethod
from logging import raiseExceptions


class ImageDetectionHandler(ABC):
    def __init__(self, detection_file_path="", preload_data=False, apply_nms=False, nms_params=None) -> None:
        self.detection_file_path: str = detection_file_path
        self.preload_data: bool = preload_data
        self.__detections: list = []
        
        assert self.detection_file_path != ""
        assert self.preload_data==False, "data preloading not supported due to resource hog"
        
        self.apply_nms: bool = apply_nms
        if self.apply_nms:
            self.preload_data = True
            self.nms = nms_params["nms_class"]()
            self.nms_score_threshold = nms_params["score_threshold"]
            self.nms_iou_threshold = nms_params["iou_threshold"]
        
        if self.preload_data:
            self.__init_detections()
            
       
    def __init_detections(self,):
        # Ensure detections are loaded during initialization if preload is True.
        # This method could also handle post-loading processing if necessary.
        self.load_detection_file()
        
        if self.apply_nms:
            self.__detections = self.nms.apply_class_nms(self.__detections,
                                                         self.nms_score_threshold,
                                                         self.nms_iou_threshold)
    
    # Function(s) to be implemented in subclass
    @abstractmethod
    def load_detection_file(self,):
        """
        Load detection data from `self.detection_file_path`.
        
        This method must be implemented by subclasses and must load detection data
        from the file specified by `self.detection_file_path`. The method should
        append the loaded data in the appropriate format to `self.detections` by using
        self.add_detections(new_detection).
        """
        pass
    
    """
    Disabled __len__ since the len of 
    self.__detections can be 0 if self.preload_data is False
    This can lead to confusion
    """
    # def __len__(self, ) -> int:
    #     if self.preload_data:
    #         return len(self.__detections)
        
    #     self.__init_detections()
    #     self.preload_data = True
    #     return len(self.__detections)
    def __len__(self, ):
        raise TypeError("len() is disabled on purpose")
    
    # User Functions
    def add_detections(self, new_detection):
        self.__detections.append(new_detection)    
    
    def get_detections(self,):
        if self.preload_data == False:
            self.__init_detections()

        return self.__detections
