
from ast import Dict
import os
import psutil
from tqdm import tqdm
from abc import ABC, abstractmethod
from typing import Any, Iterator, List

from joblib import Parallel, delayed


class DatasetDetectionLoader(ABC):
    def __init__(self, root_dir=None,
                 detections_txt_list=None,
                 apply_nms=False,
                 nms_params=None) -> None:
        """
        'self.dataset_detections' will hold detections from each image in the dataset
        indexing into self.dataset_detections will return DetectionHandler Object for that Image
        """
    
        assert root_dir is not None, "Detection directory cannot be None"
        
        if detections_txt_list is not None:
            assert self.is_valid_file(detections_txt_list), f"Could not find file {detections_txt_list}"
        
        self.detections_dir = root_dir
        self.detections_txt_list = detections_txt_list
        
        if apply_nms is False and nms_params is not None:
            print(f"apply_nms: {apply_nms}... ignoring nms_params")
        
        if apply_nms is True:
            assert isinstance(nms_params, Dict)
            
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
    
    def load_dataset_detections(self):
        self.find_detection_files()
        print("Lazy Loading Detection Files...")

        if self.should_parallelize():
            num_workers = psutil.cpu_count(logical=True) 
            print(f"num_workers {num_workers}")
            results = Parallel(n_jobs=num_workers)(
                delayed(self.process_detection)(detection_file) for detection_file in tqdm(self.dataset_detections))
            self.dataset_detections = results
        else:
            for i in tqdm(range(len(self.dataset_detections))):
                detection_info = self.dataset_detections[i]
                self.dataset_detections[i] = self.process_detection(detection_info)
    
    def find_detection_files(self):
        print(f"Populating Detection Files...")
        
        self.populate_detection_file_paths()
        
        assert self.dataset_detections is not None, "Invalid list of files"
        assert isinstance(self.dataset_detections, list)
        
        # redundant check. can potentially do away with
        for file_path_i in self.dataset_detections:
            assert self.is_valid_file(file_path_i)
                         
    def process_detection(self, detection_file):
        handler_class = self.get_detection_handler_class()
        return handler_class(
            detection_file_path=detection_file,
            apply_nms=self.apply_nms, nms_params=self.nms_params)
       
    def populate_detection_file_paths(self, ):
        if self.detections_txt_list != "":
            assert self.is_valid_file(self.detections_txt_list)
        else:
            print("No detections_txt_list provided. Will find json files in root_detections_dir....")
            raise NotImplementedError
            
        with open(self.detections_txt_list, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                detection_file_path = os.path.join(self.detections_dir, line.strip())
                if not self.is_valid_file(detection_file_path):
                    raise FileNotFoundError(f"Invalid file path: {detection_file_path}")
                self.dataset_detections.append(detection_file_path)
        
    @abstractmethod
    def get_detection_handler_class(self):
        """
        Subclasses should return their specific DetectionHandler class.
        This method enforces subclasses to specify their DetectionHandler.
        """
        raise NotImplementedError