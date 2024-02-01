
from attr import dataclass


@dataclass(init=False, frozen=False, order=True)
class BBox:
     
    x1: float
    y1: float
    x2: float
    y2: float
        
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
        
        object.__setattr__(self, 'x1', x1)
        object.__setattr__(self, 'y1', y1)
        object.__setattr__(self, 'x2', x2)
        object.__setattr__(self, 'y2', y2)
        
        # all coordinates should be +ve
        assert self.x1 >= 0 and \
            self.y1 >= 0 and \
            self.x2 >= 0 and \
            self.y2 >= 0, f"negative bounding box coordinates. Found \
                    ({self.x1}, {self.y1}), ({self.x2}, {self.y2})"
        
        # bottom left x should be <= top right x
        # bottom left y should be <= top right y      
        assert self.x1 <= self.x2 and self.y1 <= self.y2
    
    @property
    def area(self) -> float:
        """Computes  area of the bounding box."""
        area: float = (self.y2 - self.y1) * (self.x2 - self.x1)
        assert area >= 0, "Negative bounding box area"
        return area
    
    @property
    def height(self) -> float:
        """Computes height of the bounding box."""
        return self.y2 - self.y1

    @property
    def width(self) -> float:
        """Computes width of the bounding box."""
        return self.x2 - self.x1
    
    def intersection_over_union(self, another_bbox: 'BBox') -> float:
        """
        intersection_over_union

        Computes Intersection of Union with given BBox

        Args:
            another_bbox (BBox): bbox with bottom-left, top-right coordinates
        Returns:
            float: intersection of union of 2 bounding boxes
        """
        assert type(another_bbox) == BBox
        
        area_bbox1: float = self.area
        area_bbox2: float = another_bbox.area
        
        # find intersection of 2 bbox
        # bottom-left x, y & top-right x, y of intersection box
        bl_x: float = max(self.x1, another_bbox.x1) 
        bl_y: float = max(self.y1, another_bbox.y1)
        tr_x: float = min(self.x2, another_bbox.x2)
        tr_y: float = min(self.y2, another_bbox.y2)
        
        h_intersection: float = (tr_y - bl_y)
        w_intersection: float = (tr_x - bl_x)
        
        if h_intersection > 0 and w_intersection > 0:
            intersection_area: float = h_intersection * w_intersection
            union_area: float = area_bbox1 + area_bbox2 - intersection_area
            
            iou: float = intersection_area / union_area
            # print(f"intersection_area: {intersection_area}, union_area: {union_area}, iou: {iou}"
        else:
            # if either height or width of intersecting box is 0,
            # iou will be 0
            return 0.0
        
        # iou cannot be 0 at the point
        assert iou > 0.0
        return iou
    