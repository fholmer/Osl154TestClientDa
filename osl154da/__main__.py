import sys
from . import signdata, opcdata
from argparse import ArgumentParser

class register():
    subparsers = []
    @classmethod
    def subparser(cls, w):
        cls.subparsers.append(w)
        return w

@register.subparser
def setup_add_sign(subparsers):
    parser = subparsers.add_parser("add-sign", help="Add a new sign")
    parser.add_argument("name", type=str, default="default", help="A short name for this sign")
    parser.add_argument("-server", required=True, type=str, help="name of opc-server")
    parser.add_argument("-tag", required=True, type=str, help="Opc tag prefix")
    parser.add_argument("-width", required=True, type=int, default=64, help="pixel width")
    parser.add_argument("-height", required=True, type=int, default=64, help="pixel height")
    parser.set_defaults(func=signdata.add_sign_data)

@register.subparser
def setup_discover_sign(subparsers):
    parser = subparsers.add_parser("discover-sign", help="Search for sign in server")
    parser.add_argument("server", type=str, help="opc-server")
    parser.add_argument("-add-tag", type=str, default="", help="add sign with matching prefix")
    parser.add_argument("-name", type=str, default="default", help="A short name for this sign")
    parser.set_defaults(func=opcdata.discover_sign_data)

@register.subparser
def setup_list_servers(subparsers):
    parser = subparsers.add_parser("list-servers", help="Print a list of available OPC servers")
    parser.set_defaults(func=opcdata.list_servers)

@register.subparser
def setup_list_signs(subparsers):
    parser = subparsers.add_parser("list-signs", help="Print a list of signs in signs-dir")
    parser.set_defaults(func=signdata.list_signs)

@register.subparser
def setup_rgb_on(subparsers):
    parser = subparsers.add_parser("rgb-on", help="Write 1.bmp to opc-server")
    parser.add_argument("-name", type=str, default="default", help="A short name for this sign")
    parser.add_argument("-image", type=str, default="1.bmp", help="name of bmp image")
    parser.set_defaults(func=opcdata.rgb_on)

@register.subparser
def setup_read(subparsers):
    parser = subparsers.add_parser("read", help="read sign tags from opc-server")
    parser.add_argument("-name", type=str, default="default", help="A short name for this sign")
    parser.set_defaults(func=opcdata.sign_read)

def main():
    global_parser = ArgumentParser(add_help=True)
    global_parser.set_defaults(func=None)
    subparsers = global_parser.add_subparsers(
        title="Commands", description="Additional help for commands: {command} --help"
    )

    for setup in register.subparsers:
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