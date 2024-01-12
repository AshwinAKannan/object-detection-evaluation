import argparse

from engine.utils.polygon_nms import PolygonNMS


if __name__ == "__main__":

    pnms = PolygonNMS()
    pnms.non_maximum_supression()
    
    parser = argparse.ArgumentParser(
        description="Script to run object detection metrics"
    )

    parser.add_argument(
        "--annotations-dir", required=True, help="Directory with GT Annotations"
    )
    
    args: argparse.Namespace = parser.parse_args()
    print(args)