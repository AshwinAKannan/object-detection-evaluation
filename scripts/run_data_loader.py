import cv2
import numpy as np
from engine.custom_loader.lmd import LMDDetectionLoader, LMDImageGTLoader
from engine.utils.bbox_nms import BBoxNMS


bboxnms = BBoxNMS()

lmd_detection = LMDDetectionLoader(
    detections_dir="/work/projects/Stellantis_LMD/model_outputs/2023-02-15-14-41/model_outputs",
    apply_nms = True,
    nms_params = {"nms_class": BBoxNMS, "score_threshold": 0.01, "iou_threshold": 0.2})
# print(len(lmd_detection))

lmd_gt = LMDImageGTLoader(
    "/work/projects/Stellantis_LMD/prepared_datasets/SLMD_Birdseye_Dataset_V0.8.1",
    "/work/projects/Stellantis_LMD/prepared_datasets/SLMD_Birdseye_Dataset_V0.8.1")

# for gt_i in lmd_gt:
#     ann_i, img_i = gt_i.get_ground_truth()
    
#     open_cv_image = np.array(img_i)


for a in lmd_detection:
    print(type(a))
    # print(f"len(a): {len(a)}")
    print(a.detection_file_path)
    dets = a.get_detections()
    print(dets)
    print(len(dets))
    
# print("")
# for i in range(len(lmd)):
#     print(len(lmd[i]))
#     print(lmd[i].detection_file_path)



# # Run through the data
# for idx, handler in enumerate(lmd):
#     print(f"Handler {idx} has {len(handler._detections)} detections")
#     for detection in handler.detections:
#         print(f"Detection: BBox={detection.x_min, detection.y_min, detection.x_max, detection.y_max}, Conf={detection.conf_score}, Class={detection.pred_class}")

# # lmd_gt = LMDImageGTLoader()