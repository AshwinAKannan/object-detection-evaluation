
import os
from tqdm import tqdm
from abc import ABC, abstractmethod
from typing import Any, Iterator, List


class DatasetImageGTLoader(ABC):
    def __init__(self,
                 root_dir=None,
                 annotations_txt_list=None
                 ) -> None:
        """
        'self.dataset_annotations' will hold detections from each image in the dataset
        indexing into self.dataset_annotations will return ImageGTHandler Object for that Image
        """
                
        assert root_dir != "" and root_dir is not None
        assert self.is_valid_file(annotations_txt_list), f"Could not find file {annotations_txt_list}"

        self.root_dir = root_dir
        self.annotations_txt_list = annotations_txt_list
        
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
        
        print("Lazy Loading Annotation Files...")
        handler_class = self.get_ground_truth_handler_class()
        for i in range(len(self.dataset_annotations)):
            annotation_info = self.dataset_annotations[i]
            self.dataset_annotations[i] = handler_class(
                annotation_info["ann_file_path"],
                annotation_info["image_path"])
    
    def find_ground_truth_image_files(self, ):
        print(f"Populating Annotation Files...")
        self.populate_ground_truth_image_files()
        
        assert self.dataset_annotations is not None, "Invalid list of files"
        assert isinstance(self.dataset_annotations, list)
        
        for ann_image_pair_i in self.dataset_annotations:
            assert len(ann_image_pair_i) == 2
            ann_file_path = ann_image_pair_i["ann_file_path"]
            image_file_path = ann_image_pair_i["image_path"]
            assert self.is_valid_file(ann_file_path) and \
                self.is_valid_file(image_file_path)
                                               
    def populate_ground_truth_image_files(self,):
        
        with open(self.annotations_txt_list, 'r') as file:
            lines = file.readlines()

            for line in tqdm(lines):
                paths = line.strip().split(';')
                if len(paths) != 2:
                    print(f"Invalid line format: {line}")
                    continue

                annotation_file_path, image_file_path = paths
                annotation_file_path = os.path.join(self.root_dir, annotation_file_path)
                image_file_path = os.path.join(self.root_dir, image_file_path)

                if not self.is_valid_file(annotation_file_path):
                    raise FileNotFoundError(f"Invalid file path: {annotation_file_path}")
                                            
                if not self.is_valid_file(image_file_path):
                    raise FileNotFoundError(f"Invalid file path: {image_file_path}")
                
                self.dataset_annotations.append({
                    'ann_file_path': annotation_file_path,
                    'image_path': image_file_path})

    @abstractmethod
    def get_ground_truth_handler_class(self,):
        """
        Subclasses should return their specific ImageGTHandler class.
        This method enforces subclasses to specify their ImageGTHandler.
        """
        raise NotImplementedError

