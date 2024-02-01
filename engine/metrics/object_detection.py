import os
import logging
from ast import List
from collections import defaultdict
from re import match

import numpy as np


class ObjectDetectionEvaluationEngine():
    def __init__(self, detections_list, annotations_list, iou_thresholds: List, ) -> None:
        assert isinstance(detections_list, list) and \
            isinstance(annotations_list, list) and \
            isinstance(iou_thresholds, list)
        
        self.__detections_list = detections_list
        self.__annotations_list = annotations_list
        self.__iou_thresholds = iou_thresholds
        
        self.__logger = logging.getLogger(__name__)

        # detection annotation (image x class)
        self.__dann_pairs = defaultdict(lambda: {"detections": [], "annotations": []})
        
        self.__group_detections_by_image_id_and_class()
        
    def __get_file_name_without_extension(self, file_path):
        base = os.path.basename(file_path)
        return os.path.splitext(base)[0]

    def __group_detections_by_image_id_and_class(self):
        """Group detections and annotations by image x class."""
        
        self.__logger.info(f"Grouping Detections & Annotations (image x class)")
        
        paired_data = defaultdict(lambda: {"image_detections": [], "image_annotations": []})
        annotation_data = {
            self.__get_file_name_without_extension(image_ann.ann_file_path): image_ann 
            for image_ann in self.__annotations_list
        }
        
        for image_detections in self.__detections_list:
            file_name = self.__get_file_name_without_extension(image_detections.detection_file_path)
            if file_name in annotation_data:
                paired_data[file_name]['image_detections'] = image_detections
                paired_data[file_name]['image_annotations'] = annotation_data[file_name]
            else:
                self.__logger.warning(f"Skipping \
                                      {image_detections.detection_file_path}. \
                                      Missing annotations file")
        
        for file_name, data in paired_data.items():
            image_detections = data["image_detections"].load_detections()
            image_annotations = data["image_annotations"].load_annotations(False)['objects']
            self.__logger.info(file_name)
            for detection in image_detections:
                self.__dann_pairs[file_name, detection.class_id]["detections"].append(detection)
            
            for annotation in image_annotations:
                self.__dann_pairs[file_name, annotation.class_id]["annotations"].append(annotation)
    
    def __get_ious(self, detections, annotations):
        ious = np.zeros((len(detections), len(annotations)))
        for det_idx, det in enumerate(detections):
            for ann_idx, ann in enumerate(annotations):
                ious[det_idx, ann_idx] = det.intersection_over_union(ann)
        
        return ious

    def __evaluate_dataset(self, iou_threshold, max_dets=None, area_range=None):
        self.__logger.info(f"Evaluating iou_threshold {iou_threshold}")
        _evals = defaultdict(lambda: {"detection_scores": [], "hit": [], "ann_count": []})
        
        # TODO: incorporate max_dets and area_range
        for image_id, class_id in self.__dann_pairs:
            dann_pair = self.__dann_pairs[(image_id, class_id)]
            eval_result = self.__evaluate_image(dann_pair["detections"],
                                                dann_pair["annotations"],
                                                iou_threshold)

            acc = _evals[class_id]
            acc["detection_scores"].append(eval_result["detection_scores"])
            acc["hit"].append(eval_result["hit"])
            acc["ann_count"].append(eval_result["ann_count"])
            
        # now reduce accumulations
        for class_id in _evals:
            acc = _evals[class_id]
            acc["detection_scores"] = np.concatenate(acc["detection_scores"])
            acc["hit"] = np.concatenate(acc["hit"]).astype(bool)
            acc["ann_count"] = np.sum(acc["ann_count"])
        
        res = {}
        # run ap calculation per-class
        for class_id in _evals:
            class_eval_results = _evals[class_id]
            res[class_id] = {
                "class_id": class_id,
                **self.compute_per_class_average_precision_recall(detection_scores=class_eval_results["detection_scores"],
                                                                  hit=class_eval_results["hit"],
                                                                  total_ann_count=class_eval_results["ann_count"])
                }
        return res
            
    def compute_per_class_average_precision_recall(self, detection_scores, hit, total_ann_count, recall_thresholds=None):
        if total_ann_count == 0:
            return {
                "precision": None,
                "recall": None,
                "AP": None,
                "interpolated precision": None,
                "interpolated recall": None,
                "total positives": total_ann_count,
                "TP": None,
                "FP": None
            }
            
        # by default evaluate on 101 recall levels
        if recall_thresholds is None:
            recall_thresholds = np.linspace(0.0,
                                            1.00,
                                            int(np.round((1.00 - 0.0) / 0.01)) + 1,
                                            endpoint=True)

        # sort in descending score order
        inds = np.argsort(-detection_scores, kind="stable")

        scores = detection_scores[inds]
        matched = hit[inds]
        
        tp = np.cumsum(matched)
        fp = np.cumsum(~matched)

        rc = tp / total_ann_count
        pr = tp / (tp + fp)

        # make precision monotonically decreasing
        i_pr = np.maximum.accumulate(pr[::-1])[::-1]

        rec_idx = np.searchsorted(rc, recall_thresholds, side="left")
        n_recalls = len(recall_thresholds)

        # get interpolated precision values at the evaluation thresholds
        i_pr = np.array([i_pr[r] if r < len(i_pr) else 0 for r in rec_idx])

        return {
            "precision": pr,
            "recall": rc,
            "AP": np.mean(i_pr),
            "interpolated precision": i_pr,
            "interpolated recall": recall_thresholds,
            "total positives": total_ann_count,
            "TP": tp[-1] if len(tp) != 0 else 0,
            "FP": fp[-1] if len(fp) != 0 else 0
        }   
        
    def __evaluate_image(self, detections, annotations, iou_threshold, max_dets=None):
        """
        __evaluate_image _summary_

        _extended_summary_

        Args:
            detections (_type_): list of detections
            annotations (_type_): list of annotations
            iou_threshold (_type_): _description_
            max_dets (_type_, optional): Pick max_dets number of detections. 
                                        Defaults to None - which means all detections will be used.
        """
        # calculate iou between all detections and annotations (__ious=(detections x annotations))
        __ious = self.__get_ious(detections, annotations)
        # sort in decending order
        detections_sort = np.argsort([-det.objectness_score for det in detections], kind="stable")

        detections = [detections[idx] for idx in detections_sort[:max_dets]]
        __ious = __ious[detections_sort[:max_dets]]
        
        annotation_hit_tracker = {}
        detection_hit_tracker = {}
        
        # find hit
        for det_idx, det in enumerate(detections):
            iou = iou_threshold
            annotation_hit_idx = -1  # -1 -> unmatched
            
            for ann_idx, ann in enumerate(annotations):
                
                # match annotation only once
                # if annotation was already counted towards a hit, don't match
                if ann_idx in annotation_hit_tracker:
                    continue
                
                if __ious[det_idx, ann_idx] < iou:
                    continue
                
                # detection hits annotation!!
                iou = __ious[det_idx, ann_idx]
                annotation_hit_idx = ann_idx
        
            # if no annotation matched -> iou less than thresh, or ann list was empty
            if annotation_hit_idx == -1:
                continue
        
            detection_hit_tracker[det_idx] = annotation_hit_idx
            annotation_hit_tracker[annotation_hit_idx] = det_idx
        
            # print(det, annotations[detection_hit_tracker[det_idx]], iou)
            
        scores = [detections[det_idx].objectness_score for det_idx in range(len(detections))]
        # print(f"scores len {len(scores)}")
        matched = [det_idx in detection_hit_tracker for det_idx in range(len(detections))]

        num_annotations = len([ann_idx for ann_idx in range(len(annotations))])
        return {"detection_scores": scores, "hit": matched, "ann_count": num_annotations}
        
    def evaluate(self, ):
        self.__logger.info(f"Evaluating Dataset")
        self.__logger.info(f"IOU Thresholds: {self.__iou_thresholds}")
        full = {
            iou: self.__evaluate_dataset(iou_threshold=iou) for iou in self.__iou_thresholds
        }

        AP50 = np.mean([v['AP'] for k, v in full[0.50].items() if v['AP'] is not None])
        AP75 = np.mean([v['AP'] for k, v in full[0.75].items() if v['AP'] is not None])
        AP = np.mean([v['AP'] for x in full for k, v in full[x].items() if v['AP'] is not None])
        
        # max recall for 100 dets can also be calculated here
        AR100 = np.mean(
            [v['TP'] / v['total positives'] for x in full for k, v in full[x].items() if v['TP'] is not None])
        # print(AP50, AP75, AP, AR100)
        # small = {
        #     i: _evaluate(iou_threshold=i, max_dets=100, area_range=(0, 32**2))
        #     for i in iou_thresholds
        # }
        # APsmall = [x['AP'] for k in small for x in small[k] if x['AP'] is not None]
        # APsmall = np.nan if APsmall == [] else np.mean(APsmall)
        # ARsmall = [
        #     x['TP'] / x['total positives'] for k in small for x in small[k] if x['TP'] is not None
        # ]
        # ARsmall = np.nan if ARsmall == [] else np.mean(ARsmall)

        # medium = {
        #     i: _evaluate(iou_threshold=i, max_dets=100, area_range=(32**2, 96**2))
        #     for i in iou_thresholds
        # }
        # APmedium = [x['AP'] for k in medium for x in medium[k] if x['AP'] is not None]
        # APmedium = np.nan if APmedium == [] else np.mean(APmedium)
        # ARmedium = [
        #     x['TP'] / x['total positives'] for k in medium for x in medium[k] if x['TP'] is not None
        # ]
        # ARmedium = np.nan if ARmedium == [] else np.mean(ARmedium)

        # large = {
        #     i: _evaluate(iou_threshold=i, max_dets=100, area_range=(96**2, np.inf))
        #     for i in iou_thresholds
        # }
        # APlarge = [x['AP'] for k in large for x in large[k] if x['AP'] is not None]
        # APlarge = np.nan if APlarge == [] else np.mean(APlarge)
        # ARlarge = [
        #     x['TP'] / x['total positives'] for k in large for x in large[k] if x['TP'] is not None
        # ]
        # ARlarge = np.nan if ARlarge == [] else np.mean(ARlarge)

        max_det1 = {
            i: self.__evaluate_dataset(iou_threshold=i, max_dets=1)  #  , area_range=(0, np.inf)
            for i in self.__iou_thresholds
        }
        AR1 = np.mean([
            v['TP'] / v['total positives'] for x in max_det1 for k, v in max_det1[x].items() if v['TP'] is not None
        ])

        max_det10 = {
            i: self.__evaluate_dataset(iou_threshold=i, max_dets=10)  #  , area_range=(0, np.inf)
            for i in self.__iou_thresholds
        }
        AR10 = np.mean([
            v['TP'] / v['total positives'] for x in max_det1 for k, v in max_det1[x].items() if v['TP'] is not None
        ])
        
        print({
            "AP": AP,
            "AP50": AP50,
            "AP75": AP75,
            # "APsmall": APsmall,
            # "APmedium": APmedium,
            # "APlarge": APlarge,
            "AR1": AR1,
            "AR10": AR10,
            "AR100": AR100,
            # "ARsmall": ARsmall,
            # "ARmedium": ARmedium,
            # "ARlarge": ARlarge
        })

        return {
            "AP": AP,
            "AP50": AP50,
            "AP75": AP75,
            # "APsmall": APsmall,
            # "APmedium": APmedium,
            # "APlarge": APlarge,
            "AR1": AR1,
            "AR10": AR10,
            "AR100": AR100,
            # "ARsmall": ARsmall,
            # "ARmedium": ARmedium,
            # "ARlarge": ARlarge
        }
