import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument(
    "images",
    help="List of paths to input images, left to right", 
    nargs="+",
    default=[])


if __name__ == "__main__":
    args = argparser.parse_args()
    images = args.images