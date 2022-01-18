import argparse

parser = argparse.ArgumentParser()
parser.add_argument("amount", type=int, nargs="+", help="The amount of money you gain")


def get_args():
    return parser.parse_args()
