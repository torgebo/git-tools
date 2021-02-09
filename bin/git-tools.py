import argparse
import os.path

from pathlib import Path


GIT_TOOLS_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent


def main():
    parser = argparse.ArgumentParser(
            description="git-tools helper command",
    )
    subparsers = parser.add_subparsers(
            title='action', dest='action',
            description='available subcommands',
            help="Available subcommands", required=True)

    parser_aliases = subparsers.add_parser('aliases', help='inspect git-tools aliases')
    parser_aliases.set_defaults(func=aliases)

    parser_location = subparsers.add_parser('location', help='inspect git-tools location')
    parser_location.set_defaults(func=location)

    args = parser.parse_args()
    args.func(args)


def location(args):
    print(GIT_TOOLS_DIR)


def aliases(args):
    with open(GIT_TOOLS_DIR / "aliases.sh", "r") as f:
        print(f.read())


if __name__ == "__main__":
    main()
