from engine.objects.polygon import Polygon


class PolygonDetections:
    def __init__(self,
                 points,
                 objectness_score: float,
                 class_id: float) -> None:
        
        self.vertices: Polygon = Polygon(points=points)
        self.num_vertices: int = len(self.vertices)
        self.objectness_score: float = objectness_score
        self.class_id: int = class_id
        
        assert self.objectness_score >= 0 and self.objectness_score <= 1.0
    
    def area(self) -> float:
        return self.vertices.area()
    