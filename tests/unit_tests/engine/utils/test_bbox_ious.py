import pytest
import logging
from numpy.testing import assert_allclose


from tests.unit_tests.test_cases.bboxes import (
    OVERLAPPING_BBOXES,
    OVERLAPPING_BBOXES_INTERSECTION,
    OVERLAPPING_BBOXES_UNION
)


@pytest.mark.parametrize(
    "bboxes, intersection, union",
    zip(OVERLAPPING_BBOXES, OVERLAPPING_BBOXES_INTERSECTION, OVERLAPPING_BBOXES_UNION))
def test_bbox_intersection_over_union(bboxes, intersection, union):
    bbox1, bbox2 = bboxes
    iou: float = bbox1.intersection_over_union(bbox2)
    
    expected_iou: float = intersection / union
    assert_allclose(iou, expected_iou, 1e-7)
