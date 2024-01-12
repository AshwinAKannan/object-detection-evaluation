
class BBox:
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """
        __init__ _summary_

        _extended_summary_

        Args:
            x1 (float): bottom left x
            y1 (float): bottom left y
            x2 (float): top right x
            y2 (float): top right y
        """
        self.x1: float = x1
        self.y1: float = y1
        self.x2: float = x2
        self.y2: float = y2
        
        # all coordinates should be +ve
        assert self.x1 >= 0 and \
            self.y1 >= 0 and \
            self.x2 >= 0 and \
            self.y2 >= 0, f"Bounding Boxes cannot have negative coordinates. Found \
                    ({self.x1}, {self.y1}), ({self.x2}, {self.y2})"
        
        # bottom left x should be <= top right x
        # bottom left y should be <= top right y      
        assert self.x1 <= self.x2 and self.y1 <= self.y2
    
    def area(self) -> float:
        area: float = (self.y2 - self.y1) * (self.x2 - self.x1)
        assert area >= 0, "Negative bbox area"
        return area
    