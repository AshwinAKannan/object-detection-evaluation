from attr import dataclass, field
from engine.objects.bbox import BBox


@dataclass(init=False, frozen=False, order=True)
class BBoxDetections:
    
    objectness_score: float
    class_id: int
    bbox: BBox = field(init=False)
    
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

    def area(self) -> float:
        return self.bbox.area()
    