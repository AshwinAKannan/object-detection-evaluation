from attr import dataclass, field

from engine.objects.bbox import BBox
from engine.utils.enums import BBoxFormat, BBoxType


@dataclass(init=False, frozen=True, order=True)
class BBoxAnnotation:
    
    class_name: str = field(default=None, init=False)
    class_id: int = field(default=None, init=False)
    bbox: BBox = field(init=False)
    bbox_format = BBoxFormat.X1Y1X2Y2
    bbox_type = BBoxType.GROUND_TRUTH
    
    def __init__(self, x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 class_name: str,
                 class_id: int):

        object.__setattr__(self, 'bbox', BBox(x1, y1, x2, y2))
        object.__setattr__(self, 'class_name', class_name)
        object.__setattr__(self, 'class_id', class_id)
    
    @property
    def area(self) -> float:
        return self.bbox.area
    
    @property
    def height(self) -> float:
        return self.bbox.height

    @property
    def width(self) -> float:
        return self.bbox.width
    
    def intersection_over_union(self, another_bbox: BBox) -> float:
        return self.bbox.intersection_over_union(another_bbox=another_bbox)
    
    