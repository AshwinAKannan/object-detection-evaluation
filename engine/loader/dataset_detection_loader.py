
import os
import psutil
from tqdm import tqdm
from abc import ABC, abstractmethod
from typing import Any, Iterator, List

from joblib import Parallel, delayed


class DatasetDetectionLoader(ABC):
    def __init__(self, detections_dir=None, preload_data=False, apply_nms=False, nms_params=None) -> None:
        """
        'self.dataset_detections' will hold detections from each image in the dataset
        indexing into self.dataset_detections will return DetectionHandler Object for that Image
        """
        assert detections_dir is not None, "Detection directory cannot be None"
        assert isinstance(preload_data, bool), "preload_data must be a boolean value"
 
        self.detections_dir = detections_dir
        self.preload_data: bool = preload_data
        
        assert self.preload_data==False, "data preloading not supported due to resource hog"
        
        if apply_nms==False and nms_params!=None:
            print(f"apply_nms: {apply_nms}... ignoring nms_params")
            
        assert "nms_class" in nms_params and \
        "score_threshold" in nms_params and \
        "iou_threshold" in nms_params, "missing keys for nms_params: nms_class, score_threshold, iou_threshold"
        
        self.apply_nms: bool = apply_nms
        self.nms_params = nms_params
        self.dataset_detections = []
        
        self.load_dataset_detections()
        
    def __iter__(self) -> Iterator:
        # This makes the class iterable, using the list of detections as the iterable object.
        return iter(self.dataset_detections)
    
    def __len__(self,) -> int:
        print(len(self.dataset_detections))
        return len(self.dataset_detections)

    def __getitem__(self, idx) -> Any:
        print(len(self.dataset_detections))
        assert idx >= 0 and idx < len(self.dataset_detections)
        return self.dataset_detections[idx]
    
    def should_parallelize(self, threshold=0.7):
        load1, _, _ = os.getloadavg()
        cpu_cores = psutil.cpu_count(logical=False)
        load_per_core = load1 / cpu_cores
        return load_per_core < threshold
    
    def is_valid_file(self, file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):  
            return True
        return False    
    
    def find_detection_files(self):
        print(f"Populating Detection Files...")
        
        file_path_list: List = self.populate_detection_file_paths()
        
        assert file_path_list != None, "Invalid list of files"
        assert isinstance(file_path_list, list)
        
        for file_path_i in file_path_list:
            if self.is_valid_file(file_path_i):
                self.dataset_detections.append({"detection_file_path": file_path_i}) 
                     
        assert isinstance(self.dataset_detections, list)
        if not self.dataset_detections:
            print("No detection files found or specified.")
    
    def load_dataset_detections(self):
        self.find_detection_files()
        print("Loading Detection Files..." if self.preload_data else "Lazy Loading Detection Files...")

        if self.should_parallelize():
            num_workers = psutil.cpu_count(logical=True) 
            print(f"num_workers {num_workers}")
            results = Parallel(n_jobs=num_workers)(
                delayed(self.process_detection)(info) for info in tqdm(self.dataset_detections))
            self.dataset_detections = results
        else:
            for i in tqdm(range(len(self.dataset_detections))):
                detection_info = self.dataset_detections[i]
                self.dataset_detections[i] = self.process_detection(detection_info)
    
    def process_detection(self, detection_info):
        handler_class = self.get_detection_handler_class()
        return handler_class(
            detection_file_path=detection_info["detection_file_path"],
            preload_data=self.preload_data, apply_nms=self.apply_nms, nms_params=self.nms_params)
       
    @abstractmethod
    def get_detection_handler_class(self):
        """
        Subclasses should return their specific DetectionHandler class.
        This method enforces subclasses to specify their DetectionHandler.
        """
        pass

    @abstractmethod
    def populate_detection_file_paths(self):
        """
        Subclasses should implement this method to return a list of file paths'.
        """
        pass
