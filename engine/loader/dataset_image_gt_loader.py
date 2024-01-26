
import os
from tqdm import tqdm
from abc import ABC, abstractmethod
from typing import Any, Iterator, List

from concurrent.futures import ThreadPoolExecutor, as_completed


class DatasetImageGTLoader(ABC):
    def __init__(self, annotations_dir=None, image_dir=None, preload_data=False) -> None:
        """
        'self.dataset_annotations' will hold detections from each image in the dataset
        indexing into self.dataset_annotations will return ImageGTHandler Object for that Image
        """
        self.annotations_dir = annotations_dir
        self.image_dir = image_dir
        self.preload_data = preload_data
        
        assert self.preload_data==False, "data preload not supported"
        
        assert self.annotations_dir!=""
        
        print(self.annotations_dir, self.image_dir, self.preload_data)
        self.dataset_annotations = []
        
        self.load_dataset_ground_truth()
        
    def __iter__(self) -> Iterator:
        # This makes the class iterable, using the list of detections as the iterable object.
        return iter(self.dataset_annotations)
    
    def __len__(self,) -> int:
        print(len(self.dataset_annotations))
        return len(self.dataset_annotations)

    def __getitem__(self, idx) -> Any:
        print(len(self.dataset_annotations))
        assert idx >= 0 and idx < len(self.dataset_annotations)
        return self.dataset_annotations[idx]
    
    def is_valid_file(self, file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):  
            return True
        return False
    
    def load_dataset_ground_truth(self,):
        self.find_ground_truth_image_files()
        
        print("Loading Annotation Files..." if self.preload_data else "Lazy Loading Annotation Files...")
        handler_class = self.get_ground_truth_handler_class()
        for i in tqdm(range(len(self.dataset_annotations))):
            annotation_info = self.dataset_annotations[i]
            self.dataset_annotations[i] = handler_class(
                annotation_info["ann_file_path"],
                annotation_info["image_path"],
                self.preload_data)
    
    def find_ground_truth_image_files(self, ):
        print(f"Populating Annotation Files...")
        ann_image_pairs_list = self.populate_ground_truth_image_files()
        
        assert ann_image_pairs_list != None, "Invalid list of files"
        assert isinstance(ann_image_pairs_list, list)
        
        for ann_image_pair_i in ann_image_pairs_list:
            assert len(ann_image_pair_i)==2
            ann_file_path = ann_image_pair_i[0]
            image_file_path = ann_image_pair_i[1]
            if self.is_valid_file(ann_file_path) and self.is_valid_file(image_file_path):
                self.dataset_annotations.append({"ann_file_path": ann_file_path, "image_path": image_file_path}) 
                     
        assert isinstance(self.dataset_annotations, list)
        if not self.dataset_annotations:
            print("No annotation files found or specified.")
    
    @abstractmethod
    def get_ground_truth_handler_class(self,):
        """
        Subclasses should return their specific ImageGTHandler class.
        This method enforces subclasses to specify their ImageGTHandler.
        """
        pass
    
    @abstractmethod
    def populate_ground_truth_image_files(self,):
        pass
