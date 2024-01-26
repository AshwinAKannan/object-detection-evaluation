import os
import glob
from PIL import Image
import xml.etree.ElementTree as ET

from engine.loader.dataset_detection_loader import DatasetDetectionLoader
from engine.loader.dataset_image_gt_loader import DatasetImageGTLoader
from engine.loader.handler.image_detection_handler import ImageDetectionHandler
from engine.loader.handler.image_gt_handler import ImageGTHandler
from engine.objects.bbox_detections import BBoxDetections


class CocoSampleDetectionHandler(ImageDetectionHandler):
    def load_detection_file(self, ) -> None:
        with open(self.detection_file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 6:
                    class_id = int(parts[0])
                    score: float = float(parts[1])
                    x1: float = float(parts[2])
                    y1: float = float(parts[3])
                    x2: float = float(parts[4])
                    y2: float = float(parts[5])
                    detection = BBoxDetections(x1=x1,
                                               y1=y1,
                                               x2=x2,
                                               y2=y2,
                                               objectness_score=score,
                                               class_id=class_id)
                    self.add_detections(new_detection=detection)
        
        
class CocoSampleDatasetLoader(DatasetDetectionLoader):
    def get_detection_handler_class(self,):
        return CocoSampleDetectionHandler    


class CocoSampleImageGTHandler(ImageGTHandler):             
    def load_ground_truth_file(self, ):
        
        print(self.gt_file_path)
        tree: ET.ElementTree = ET.parse(self.gt_file_path)
        root = tree.getroot()
        
        size = root.find('size')
        image_w = int(size.find('width').text)
        image_h = int(size.find('height').text)
        c = int(size.find('depth').text)
        
        result = {'image_h': image_h,
                  'image_w': image_w,
                  'c': c,
                  'objects': []}
        
        # Extract object information
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            bbox_elem = obj.find('bndbox')
            xmin = int(bbox_elem.find('xmin').text)
            ymin = int(bbox_elem.find('ymin').text)
            xmax = int(bbox_elem.find('xmax').text)
            ymax = int(bbox_elem.find('ymax').text)
            bbox = [xmin, ymin, xmax, ymax]
            
            # Append object information to the objects list
            result['objects'].append({'class_name': class_name, 'bbox': bbox})
        
        # print(result)
        return result


class CocoSampleGTLoader(DatasetImageGTLoader):    
    def get_ground_truth_handler_class(self, ):
        return CocoSampleImageGTHandler