import pytest
import logging
from numpy.testing import assert_allclose

from engine.objects.polygon import Polygon
from engine.utils.iou import intersection_over_union_polygon

from tests.unit_tests.test_cases.polygons import (
    OVERLAPPING_POLYGONS,
    OVERLAPPING_POLYGON_INTERSECTION,
    OVERLAPPING_POLYGON_UNION
)


@pytest.mark.parametrize(
    "polygons, intersection, union",
    zip(OVERLAPPING_POLYGONS, OVERLAPPING_POLYGON_INTERSECTION, OVERLAPPING_POLYGON_UNION))
def test_polygon_intersection_over_union(polygons: Polygon,
                                         intersection: float,
                                         union: float) -> float:
    polygon1, polygon2 = polygons
    # print(polygon1.vertices)
    # print(polygon2.vertices)
    iou: float = intersection_over_union_polygon(polygon1, polygon2)
    
    expected_iou: float = intersection / union
    # print(f"iou: {iou}, expected_iou: {expected_iou}")
    assert_allclose(iou, expected_iou, 1e-7)
    # assert iou == True
