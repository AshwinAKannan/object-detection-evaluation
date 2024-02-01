from attr import dataclass, field

from engine.objects.bbox import BBox
from engine.utils.enums import BBoxFormat, BBoxType


@dataclass(init=False, frozen=False, order=True)
class BBoxDetection:
    
    objectness_score: float
    class_id: int
    bbox: BBox = field(init=False)
    bbox_format = BBoxFormat.X1Y1X2Y2
    bbox_type = BBoxType.DETECTION
    
    def __init__(self, x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 objectness_score: float,
                 class_id: int):

        object.__setattr__(self, 'bbox', BBox(x1, y1, x2, y2))
        object.__setattr__(self, 'objectness_score', objectness_score)
        object.__setattr__(self, 'class_id', class_id)

        assert 0.0 <= self.objectness_score <= 1.0, "objectness_score must be between 0.0 and 1.0"

    @property
    def area(self) -> float:
        return self.bbox.area
        
    def intersection_over_union(self, another_bbox) -> float:
        assert isinstance(another_bbox.bbox, BBox)
        return self.bbox.intersection_over_union(another_bbox=another_bbox.bbox)

