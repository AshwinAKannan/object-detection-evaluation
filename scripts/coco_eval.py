from engine.custom_loader.coco_sample.loaders import CocoSampleDatasetLoader
from engine.custom_loader.coco_sample.loaders import CocoSampleGTLoader

detection_loader = CocoSampleDatasetLoader(
    root_dir=".",
    detections_txt_list="datasets/coco_sample/tvt_split/test.dets.txt",
    apply_nms=False)

# for d in detection_loader:
#     print(d.detection_file_path)
#     print(d.get_detections())  
    
gt = CocoSampleGTLoader(
    root_dir=".",
    annotations_txt_list="datasets/coco_sample/tvt_split/test.ann.txt")

# for g in gt:
#     # print(g.)
#     print(g.get_ground_truth())
