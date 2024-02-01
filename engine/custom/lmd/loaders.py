import imp
import os
import json
import glob as glob
from tqdm import tqdm
from PIL import Image

from concurrent.futures import ThreadPoolExecutor


from engine.lib.handler.image_detection_handler import ImageDetectionHandler
from engine.lib.handler.image_gt_handler import ImageGTHandler
from engine.lib.dataset_detection_loader import DatasetDetectionLoader
from engine.lib.dataset_image_gt_loader import DatasetImageGTLoader
from engine.objects.bbox_detection import BBoxDetection


class LMDDetectionHandler(ImageDetectionHandler):
    def load_detection_file(self) -> None:
        try:
            with open(self.detection_file_path, 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise Exception(f"File not found: {self.detection_file_path}")
        
        for det_i in json_data["lldet"]:
            if "bbox" in det_i and "conf_score" in det_i and "pred_class" in det_i:
                bboxd_i = BBoxDetection(x1=max(0, det_i["bbox"][0]),
                                        y1=max(0, det_i["bbox"][1]),
                                        x2=max(0, det_i["bbox"][2]),
                                        y2=max(0, det_i["bbox"][3]),
                                        objectness_score=float(det_i["conf_score"]),
                                        class_id=int(float(det_i["pred_class"]))
                                        )
            
                self.add_detections(new_detection=bboxd_i)


class LMDImageGTHandler(ImageGTHandler):      
    def load_ground_truth_file(self, ):
        with open(self.gt_file_path, 'r') as file:
            data = json.load(file)
        return data
     

class LMDDetectionLoader(DatasetDetectionLoader):              
    def get_detection_handler_class(self, ):
        return LMDDetectionHandler


class LMDImageGTLoader(DatasetImageGTLoader):    
    def get_ground_truth_handler_class(self, ):
        return LMDImageGTHandler