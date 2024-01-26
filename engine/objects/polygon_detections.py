from attr import dataclass, field
from engine.objects.polygon import Polygon


@dataclass(init=False, frozen=True, order=False)
class PolygonDetections:

    polygon: Polygon = field(init=False)
    num_vertices: int = field(init=False)
    objectness_score: int
    class_id: int

    def __init__(self,
                 points,
                 objectness_score: float,
                 class_id: float) -> None:

        polygon_instance = Polygon(points=points) 
        object.__setattr__(self, 'polygon', polygon_instance)
        object.__setattr__(self, 'num_vertices', polygon_instance.num_vertices) 
        object.__setattr__(self, 'objectness_score', objectness_score)
        object.__setattr__(self, 'class_id', class_id)

        assert self.objectness_score >= 0 and self.objectness_score <= 1.0
    
    def area(self) -> float:
        return self.vertices.area()