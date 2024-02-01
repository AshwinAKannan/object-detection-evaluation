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
from engine.custom.coco_sample.classes import CocoSampleClassMapping


class CocoSampleDetectionHandler(ImageDetectionHandler):
                    
    def load_detection_file(self,) -> None:
                
        tree: ET.ElementTree = ET.parse(self.detection_file_path)
        root = tree.getroot()
        
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            class_name = class_name.replace(" ", "_")
            class_id = CocoSampleClassMapping.get_class_id(class_name)
            detection_score = float(obj.find('score').text)
            bbox_elem = obj.find('bndbox')
            x1 = float(bbox_elem.find('xmin').text)
            y1 = float(bbox_elem.find('ymin').text)
            x2 = float(bbox_elem.find('xmax').text)
            y2 = float(bbox_elem.find('ymax').text)
            
            detection = BBoxDetection(x1=x1,
                                      y1=y1,
                                      x2=x2,
                                      y2=y2,
                                      objectness_score=detection_score,
                                      class_id=class_id)
            
            self.add_detections(detection)
            
               
class CocoSampleDatasetLoader(DatasetDetectionLoader):
    def get_detection_handler_class(self,):
        return CocoSampleDetectionHandler    


class CocoSampleImageGTHandler(ImageGTHandler):             
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
            class_name = class_name.replace(" ", "_")
            class_id = CocoSampleClassMapping.get_class_id(class_name)
            bbox_elem = obj.find('bndbox')
            x1 = float(bbox_elem.find('xmin').text)
            y1 = float(bbox_elem.find('ymin').text)
            x2 = float(bbox_elem.find('xmax').text)
            y2 = float(bbox_elem.find('ymax').text)

            ann = BBoxAnnotation(x1=x1,
                                 y1=y1,
                                 x2=x2,
                                 y2=y2,
                                 class_name=class_name,
                                 class_id=class_id)
            
            result['objects'].append(ann)
            
        return result


class CocoSampleAnnotationLoader(DatasetImageGTLoader):    
    def get_ground_truth_handler_class(self, ):
        return CocoSampleImageGTHandler