from enum import Enum


class BBoxFormat(Enum):
    """
    Class representing the format of a bounding box.
    """
    X1Y1X2Y2 = 1


class BBoxType(Enum):
    """
    Class representing if the bounding box is ground truth or not.
    """
    GROUND_TRUTH = 1
    DETECTION = 2


class PolygonFormat(Enum):
    """
    Class representing the format of a polygon
    """
    XYXYXY = 1    
    
    
class PolygonType(Enum):
    """
    Class representing if the polygon is ground truth or not.
    """
    GROUND_TRUTH = 1
    DETECTION = 2