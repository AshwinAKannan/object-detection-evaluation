import sys
import logging
import numpy as np
from collections import defaultdict

from engine.custom.pascalvoc_sample.loaders import PascalVocSampleDatasetLoader
from engine.custom.pascalvoc_sample.loaders import PascalVocSampleAnnotationLoader
from engine.lib.matcher.pair_danns import PairDetectionsWithAnnotations
from engine.metrics.object_detection import ObjectDetectionEvaluationEngine
from engine.configs import pascalvoc_config

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# list of detections of class <>
# TODO: Support a specific extension
detection_loader = PascalVocSampleDatasetLoader(
    root_dir=pascalvoc_config.DETECTIONS_ROOT_DIR,
    detections_txt_list=pascalvoc_config.DETECTIONS_TXT_LIST_PATH,
    apply_nms=pascalvoc_config.APPLY_NMS)


# list of annotations of class <>    
annotation_loader = PascalVocSampleAnnotationLoader(
    root_dir=pascalvoc_config.ANNOTATIONS_ROOT_DIR,
    annotations_txt_list=pascalvoc_config.ANNOTATIONS_TXT_LIST_PATH)


# IOU_THRESHOLDS = np.linspace(0.5, 0.95, int(np.round((0.95 - 0.5) / 0.05)) + 1, endpoint=True)
IOU_THRESHOLDS = np.array([0.1, 0.3, 0.5, 0.75])

eval_e = ObjectDetectionEvaluationEngine(detection_loader.dataset_detections,
                                         annotation_loader.dataset_annotations,
                                         IOU_THRESHOLDS.tolist())
eval_e.evaluate()