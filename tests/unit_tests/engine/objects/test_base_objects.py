import pytest
import logging

from numpy.testing import assert_equal, assert_allclose

from engine.objects.bbox import BBox
from engine.objects.polygon import Polygon

from tests.unit_tests.test_cases.bboxes import (
    BBOXES,
    BBOX_AREAS,
    INVALID_BBOXES)
from tests.unit_tests.test_cases.polygons import (
    POLYGONS,
    NUM_VERTICES,
    POLYGON_AREAS,
    INVALID_POLYGON_VERTICES)


@pytest.fixture(autouse=True)
def set_logging_level(caplog) -> None:
    caplog.set_level(logging.INFO)


@pytest.mark.parametrize(
    "bbox, expected_area",
    zip(BBOXES, BBOX_AREAS))
def test_bbox_area(bbox: BBox,
                   expected_area: float,) -> None:
    assert_equal(actual=bbox.area(), desired=expected_area)


@pytest.mark.parametrize("invalid_bbox", INVALID_BBOXES)
def test_invalid_bbox(invalid_bbox) -> None:
    # print(invalid_bbox)
    assert len(invalid_bbox) == 4
    with pytest.raises(expected_exception=AssertionError):
        BBox(x1=invalid_bbox[0],
             y1=invalid_bbox[1],
             x2=invalid_bbox[2],
             y2=invalid_bbox[3])


@pytest.mark.parametrize(
    "polygon, expected_num_vertices",
    zip(POLYGONS, NUM_VERTICES))
def test_polygon_vertices_len(polygon: Polygon,
                              expected_num_vertices: float,
                              ) -> None:
    # print(f"polygon.num_vertices: {polygon.num_vertices}, \
    #       expected_num_vertices: {expected_num_vertices}")
    assert_equal(actual=polygon.num_vertices, desired=expected_num_vertices)


@pytest.mark.parametrize(
    "polygon, expected_area",
    zip(POLYGONS, POLYGON_AREAS))
def test_polygon_area(polygon: Polygon,
                      expected_area: float,
                      ) -> None:
    # print(f"polygon.area(): {polygon.area()}, \
    #       expected_area: {expected_area}")
    assert_allclose(actual=polygon.area(), desired=expected_area)


@pytest.mark.parametrize("invalid_polygon_vertices", INVALID_POLYGON_VERTICES)
def test_invalid_polygons(invalid_polygon_vertices) -> None:
    # print(invalid_polygon_vertices)
    with pytest.raises(expected_exception=AssertionError):
        Polygon(points=invalid_polygon_vertices)
