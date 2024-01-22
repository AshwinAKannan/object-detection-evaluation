import pytest
import logging
from numpy.testing import assert_allclose

from engine.utils.bbox_nms import BBoxNMS
from engine.utils.polygon_nms import PolygonNMS

from tests.unit_tests.test_cases.nms_bboxes import (
    BBOX_NMS_SCENARIOS,
    INVALID_BBOX_NMS
)

from tests.unit_tests.test_cases.nms_polygon import (
    POLYGON_NMS_SCENARIOS,
    INVALID_POLYGON_NMS
)


bbox_nms = BBoxNMS()
polygon_nms = PolygonNMS()

@pytest.mark.parametrize(
    "nms_scenarios", BBOX_NMS_SCENARIOS)
def test_bbox_nms(nms_scenarios):
    
    detections = nms_scenarios["detections"]
    iou_thresh = nms_scenarios["iou_thresh"]
    score_thresh = nms_scenarios["score_thresh"]
    expected_num_detections = nms_scenarios["expected_detections"]
    
    # print(detections, iou_thresh, score_thresh, expected_num_detections)
    
    output_detections = bbox_nms.apply_nms(detections, score_thresh, iou_thresh)
    
    # print(f"output_detections: {output_detections}, expected_num_detections: {expected_num_detections}")
    
    # for output_detections_i in output_detections:
    #     print(f"x1: {output_detections_i.bbox.x1}\
    #         y1: {output_detections_i.bbox.y1}\
    #             x2: {output_detections_i.bbox.x2}\
    #                 y2: {output_detections_i.bbox.y2}\
    #                     objectness_score: {output_detections_i.objectness_score}\
    #                         class: {output_detections_i.class_id}")
    
    assert len(output_detections) == expected_num_detections
    

@pytest.mark.parametrize("invalid_bbox_nms_scenario", INVALID_BBOX_NMS)
def test_invalid_bbox_nms_args(invalid_bbox_nms_scenario) -> None:
    with pytest.raises(expected_exception=AssertionError):
        bbox_nms.apply_nms(invalid_bbox_nms_scenario, 0.1, 0.5)
 

@pytest.mark.parametrize(
    "nms_scenarios", POLYGON_NMS_SCENARIOS)
def test_polygon_nms(nms_scenarios):
    # print(f".....................test_polygon_nms.....................")
    detections = nms_scenarios["detections"]
    iou_thresh = nms_scenarios["iou_thresh"]
    score_thresh = nms_scenarios["score_thresh"]
    expected_num_detections = nms_scenarios["expected_detections"]
    
    # print(detections, iou_thresh, score_thresh, expected_num_detections)
    
    output_detections = polygon_nms.apply_nms(detections, score_thresh, iou_thresh)
     
    # for output_detections_i in output_detections:
    #     print(f"objectness_score: {output_detections_i.objectness_score}\
    #                         class: {output_detections_i.class_id}")
    
    assert len(output_detections) == expected_num_detections


@pytest.mark.parametrize("invalid_polygon_nms_scenario", INVALID_POLYGON_NMS)
def test_invalid_polygon_nms_args(invalid_polygon_nms_scenario) -> None:
    with pytest.raises(expected_exception=AssertionError):
        polygon_nms.apply_nms(invalid_polygon_nms_scenario, 0.1, 0.5)
 