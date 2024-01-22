from engine.objects.bbox import BBox


class BBoxDetections:
    def __init__(self, x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 objectness_score: float,
                 class_id: int) -> None:
        
        self.bbox: BBox = BBox(x1, y1, x2, y2)
        self.objectness_score: float = objectness_score
        self.class_id: int = class_id
        
        # assert self.objectness_score >= 0 and self.objectness_score <= 1.0
    
    def area(self) -> float:
        return self.bbox.area()
    