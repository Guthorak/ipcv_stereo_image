"""Script to produce surface mesh from two stereo images"""
import argparse
from src.stereo_params import get_stereo_params
from src.calibration import calibrate


ARGPARSER = argparse.ArgumentParser()

ARGPARSER.add_argument(
    "--data",
    "-d",
    help="Path to camera calibration data",
    dest="data")

ARGPARSER.add_argument(
    "--calibrate",
    "-c",
    dest="calibrate",
    help="Path to calibration images and path to save calibration data",
    nargs="+")


if __name__ == "__main__":
    ARGS = ARGPARSER.parse_args()
    if ARGS.calibrate:
        IN_DIR, OUT_DIR = ARGS.calibrate
        calibrate(IN_DIR, OUT_DIR)
    if ARGS.data:
        STEREO_PARAMETERS = get_stereo_params(ARGS.data)
