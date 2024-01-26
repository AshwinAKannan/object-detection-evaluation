import os
import cv2
from abc import ABC, abstractmethod


class ImageGTHandler(ABC):
    def __init__(self, gt_file_path="", image_path="") -> None:
        self.gt_file_path: str = gt_file_path
        self.image_path: str = image_path
        
        print(self.gt_file_path, self.image_path)
        assert self.gt_file_path != ""
        
        self.__image = None
        self.__gt = None

    def __init_ground_truth(self, ) -> None:
        # Ensure annotations are loaded during initialization if preload is True.
        self.__gt = self.load_ground_truth_file()
    
    def is_valid_file(self, file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):  
            return True
        return False
    
    def is_image(self) -> bool:
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
        return os.path.splitext(self.image_path)[1].lower() in image_extensions

    def load_image(self,) -> None:
        assert self.is_valid_file(self.image_path) and self.is_image()
        image = cv2.imread(self.image_path)
        self.__image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # def __len__(self, ) -> int:
    #     return len(self.__gt)
    def __len__(self, ):
        raise TypeError("len() is disabled on purpose")
    
    # User Functions
    def add_annotation(self, new_annotation) -> None:
        self.__gt.append(new_annotation)   
    
    def get_ground_truth(self,):
        self.__init_ground_truth()

        return self.__gt, self.__image
    
    # Function(s) to be implemented in subclass   
    @abstractmethod
    def load_ground_truth_file(self,) -> None:
        """
        Load ground truth data from `self.gt_file_path`.
        
        This method must be implemented by subclasses and must load detection data
        from the file specified by `self.gt_file_path`. The method should
        append the loaded data in the appropriate format to `self.__gt` by using
        self.add_annotation(annotation_i).
        """
        raise NotImplementedError
    