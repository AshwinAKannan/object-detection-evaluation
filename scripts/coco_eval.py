import sys
import logging
import numpy as np
from collections import defaultdict

from engine.custom.coco_sample.loaders import CocoSampleDatasetLoader
from engine.custom.coco_sample.loaders import CocoSampleAnnotationLoader
from engine.lib.matcher.pair_danns import PairDetectionsWithAnnotations
from engine.metrics.object_detection import ObjectDetectionEvaluationEngine
from engine.configs import coco_config

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# list of detections of class <>
# TODO: Support a specific extension
detection_loader = CocoSampleDatasetLoader(
    root_dir=coco_config.DETECTIONS_ROOT_DIR,
    detections_txt_list=coco_config.DETECTIONS_TXT_LIST_PATH,
    apply_nms=coco_config.APPLY_NMS)

print(len(detection_loader))

# list of annotations of class <>    
annotation_loader = CocoSampleAnnotationLoader(
    root_dir=coco_config.ANNOTATIONS_ROOT_DIR,
    annotations_txt_list=coco_config.ANNOTATIONS_TXT_LIST_PATH,
    skip_loading_images=True)

print(len(annotation_loader))

IOU_THRESHOLDS = np.linspace(0.5, 0.95, int(np.round((0.95 - 0.5) / 0.05)) + 1, endpoint=True)
# IOU_THRESHOLDS = np.array([0.1, 0.3, 0.5, 0.75])
# input()
# print(IOU_THRESHOLDS)

eval_e = ObjectDetectionEvaluationEngine(detection_loader.dataset_detections,
                                         annotation_loader.dataset_annotations,
                                         IOU_THRESHOLDS.tolist())
eval_e.evaluate()
