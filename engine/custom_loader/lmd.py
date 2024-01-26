import imp
import os
import json
import glob as glob
from tqdm import tqdm
from PIL import Image

from concurrent.futures import ThreadPoolExecutor


from engine.loader.handler.image_detection_handler import ImageDetectionHandler
from engine.loader.handler.image_gt_handler import ImageGTHandler
from engine.loader.dataset_detection_loader import DatasetDetectionLoader
from engine.loader.dataset_image_gt_loader import DatasetImageGTLoader
from engine.objects.bbox_detections import BBoxDetections


class LMDDetectionHandler(ImageDetectionHandler):
    def load_detection_file(self) -> None:
        try:
            with open(self.detection_file_path, 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise Exception(f"File not found: {self.detection_file_path}")
        
        for det_i in json_data["lldet"]:
            if "bbox" in det_i and "conf_score" in det_i and "pred_class" in det_i:
                bboxd_i = BBoxDetections(x1=max(0, det_i["bbox"][0]),
                                         y1=max(0, det_i["bbox"][1]),
                                         x2=max(0, det_i["bbox"][2]),
                                         y2=max(0, det_i["bbox"][3]),
                                         objectness_score=float(det_i["conf_score"]),
                                         class_id=int(float(det_i["pred_class"]))
                                         )
            
                self.add_detections(new_detection=bboxd_i)


class LMDImageGTHandler(ImageGTHandler):      
    def load_image(self, ) -> None:
        image: Image = Image.open(self.image_path)
        return image
        
    def load_ground_truth_file(self, ):
        with open(self.gt_file_path, 'r') as file:
            data = json.load(file)
        return data
     

class LMDDetectionLoader(DatasetDetectionLoader):              
    def get_detection_handler_class(self, ):
        return LMDDetectionHandler

    def populate_detection_file_paths(self,):
        "return a list of file paths'"''
        file_list: list = glob.glob(self.detections_dir + "/*.json")
        return file_list


class LMDImageGTLoader(DatasetImageGTLoader):    
    def get_ground_truth_handler_class(self, ):
        return LMDImageGTHandler

    def populate_ground_truth_image_files(self, ):
        """return a list of tuple (annotation file path, image_path)"""
        
        ann_dir = os.path.join(self.annotations_dir, "det_gt", "val_dataset_Scale21Jan23_vert640x400_2023-02-04-06-49")
        image_dir = os.path.join(self.image_dir, "images", "val_dataset_Scale21Jan23_vert640x400_2023-02-04-06-49")

        matched_files = []
        
        # List all files in the directories
        gt_files = {os.path.splitext(f)[0]: os.path.join(ann_dir, f) for f in os.listdir(ann_dir) if os.path.isfile(os.path.join(ann_dir, f))}
        image_files = {os.path.splitext(f)[0]: os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))}
        
        # Match files based on basename
        for gt_basename, gt_path in gt_files.items():
            if gt_basename in image_files:
                # print(gt_basename, image_files[gt_basename])
                if self.is_valid_file(gt_path) and self.is_valid_file(image_files[gt_basename]):
                    matched_files.append((gt_path, image_files[gt_basename]))
        
        return matched_files
        