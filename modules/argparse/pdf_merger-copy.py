import argparse

parser = argparse.ArgumentParser(description="Add some integers.")
# Note: argparse: nargs='*' positional argument doesn't accept any items
# if preceded by an option and another positional
parser.add_argument("integers", metavar="N", type=int, nargs="+", help="interger list")

args = parser.parse_args()
print(args.integers)