import os
import glob
from PIL import Image
import xml.etree.ElementTree as ET

from engine.lib.dataset_detection_loader import DatasetDetectionLoader
from engine.lib.dataset_image_gt_loader import DatasetImageGTLoader
from engine.lib.handler.image_detection_handler import ImageDetectionHandler
from engine.lib.handler.image_gt_handler import ImageGTHandler
from engine.objects.bbox_detection import BBoxDetection
from engine.objects.bbox_annotation import BBoxAnnotation


class PascalVocSampleDetectionHandler(ImageDetectionHandler):
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
                    detection = BBoxDetection(x1=x1,
                                              y1=y1,
                                              x2=x2,
                                              y2=y2,
                                              objectness_score=score,
                                              class_id=class_id)
                    self.add_detections(new_detection=detection)
        
        
class PascalVocSampleDatasetLoader(DatasetDetectionLoader):
    def get_detection_handler_class(self,):
        return PascalVocSampleDetectionHandler    


class PascalVocSampleImageGTHandler(ImageGTHandler):             
    def load_ground_truth_file(self, ):
        
        tree: ET.ElementTree = ET.parse(self.ann_file_path)
        root = tree.getroot()
        
        size = root.find('size')
        image_w = int(size.find('width').text)
        image_h = int(size.find('height').text)
        c = int(size.find('depth').text)
        
        result = {'image_h': image_h,
                  'image_w': image_w,
                  'image_channels': c,
                  'objects': []}
        
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            class_id = int(obj.find('class_id').text)
            bbox_elem = obj.find('bndbox')
            x1 = int(bbox_elem.find('xmin').text)
            y1 = int(bbox_elem.find('ymin').text)
            x2 = int(bbox_elem.find('xmax').text)
            y2 = int(bbox_elem.find('ymax').text)
            # bbox = [xmin, ymin, xmax, ymax]
            
            ann = BBoxAnnotation(x1=x1,
                                 y1=y1,
                                 x2=x2,
                                 y2=y2,
                                 class_name=class_name,
                                 class_id=class_id)
            
            result['objects'].append(ann)
            
        return result


class PascalVocSampleAnnotationLoader(DatasetImageGTLoader):    
    def get_ground_truth_handler_class(self, ):
        return PascalVocSampleImageGTHandler