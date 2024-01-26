from attr import dataclass, field
from engine.objects.bbox import BBox


@dataclass(init=False, frozen=False, order=True)
class BBoxAnnotations:
    class_name: str = field(default=None, init=False)
    class_id: int = field(default=None, init=False)
    bbox: BBox = field(init=False)
    
    def __init__(self, x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 class_name: float,
                 class_id: int):

        object.__setattr__(self, 'bbox', BBox(x1, y1, x2, y2))

        if class_name is None and class_id is None:
            raise ValueError("Either class_name or class_id must be provided.")

        object.__setattr__(self, 'bbox', BBox(x1, y1, x2, y2))
        if class_name is not None:
            object.__setattr__(self, 'class_name', class_name)
            
        if class_id is not None:
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
    
    