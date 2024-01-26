from abc import ABC, abstractmethod

# Should this be named ObjectDetectionImageGTHandler
# or can this be used for any Generic GT Handling?
class ImageGTHandler(ABC):
    def __init__(self, gt_file_path="", image_path="", preload_annotations=True) -> None:
        self.gt_file_path: str = gt_file_path
        self.image_path: str = image_path
        self.preload_annotations: bool = preload_annotations
        
        assert self.gt_file_path != ""
        assert self.preload_annotations == True or self.preload_annotations == False
        
        # print(self.gt_file_path, self.image_path, self.preload_annotations)
        
        self.__image = None
        self.__gt = None
        if self.preload_annotations:
            self.__init_ground_truth()

    def __init_ground_truth(self, ) -> None:
        # Ensure annotations are loaded during initialization if preload is True.
        self.__gt = self.load_ground_truth_file()
        if self.image_path != "":
            self.__image = self.load_image()

    # 
    # Function(s) to be implemented in subclass
    #     
    @abstractmethod
    def load_ground_truth_file(self,) -> None:
        """
        Load ground truth data from `self.gt_file_path`.
        
        This method must be implemented by subclasses and must load detection data
        from the file specified by `self.gt_file_path`. The method should
        append the loaded data in the appropriate format to `self.__gt` by using
        self.add_annotation(annotation_i).
        """
        pass

    @abstractmethod
    def load_image(self,) -> None:
        """
        Load Image from `self.image_path`.

        This method must be implemented by subclasses and must load image 
        from the file specified by `self.__image`.
        """
        pass
    
    """
    Disabled __len__ since the len of self.__gt
    can be 0 if self.preload_annotations is False
    This can lead to confusion
    """
    # def __len__(self, ) -> int:
    #     if self.preload_annotations:
    #         return len(self.__gt)
        
    #     self.__init_ground_truth()
    #     self.preload_annotations = True
    #     return len(self.__gt)
    def __len__(self, ):
        raise TypeError("len() is disabled on purpose")
    
    #
    # User Functions
    # 
    def add_annotation(self, new_annotation) -> None:
        self.__gt.append(new_annotation)   
    
    def get_ground_truth(self,):
        if self.preload_annotations == False:
            self.__init_ground_truth()

        return self.__gt, self.__image