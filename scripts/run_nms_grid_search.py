import argparse

from engine.utils.polygon_nms import PolygonNMS
from engine.utils.bbox_nms import BBoxNMS


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Script to run object detection metrics"
    )

    parser.add_argument(
        "--annotations-dir", required=True, help="Directory with GT Annotations"
    )
    
    args: argparse.Namespace = parser.parse_args()
    print(args)
    
    pnms = PolygonNMS()
    pnms.apply_nms()
    
    bboxnms = BBoxNMS()
    bboxnms.apply_nms()