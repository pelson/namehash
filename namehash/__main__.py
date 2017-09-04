import argparse

from . import encode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("N",
                        help="Display the namehash for the given number",
                        type=int)
    args = parser.parse_args()
    print(encode(args.N))


if __name__ == '__main__':
    main()
