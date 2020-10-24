import sys
from . import bmpdata
from argparse import ArgumentParser

def setup_create(subparsers):
    parser = subparsers.add_parser("create", help="Create new sign")
    parser.add_argument("tag", type=str, help="Opc tag name")
    parser.add_argument("-width", "--width", type=int, default=64, help="pixel width")
    parser.add_argument("-height", "--height", type=int, default=64, help="pixel height")
    parser.set_defaults(func=bmpdata.create_bmp_data)

def main():
    global_parser = ArgumentParser(add_help=True)
    global_parser.set_defaults(func=None)
    subparsers = global_parser.add_subparsers(
        title="Commands", description="Additional help for commands: {command} --help"
    )

    for setup in [setup_create]:
        setup(subparsers)

    args = global_parser.parse_args()

    if args.func:
        kwargs = {k:v for k,v in args._get_kwargs() if not k == "func"}
        try:
            args.func(**kwargs)
        except KeyboardInterrupt:
            print("Aborted by user")
    else:
        global_parser.print_help()

if __name__ == "__main__":
    main()