import sys

from . import cli, main2

__project_name__ = "hisaction"


def main() -> int:
    parser = cli.get_args_parser(__project_name__)
    args = parser.parse_args()

    if not args.command:
        out = main2.render_template("extended.j2")
        sys.stdout.write(out)

    if args.command == "config":
        if args.subcommand:
            args.func(args)
        else:
            print("Config command")
            if args.verbose:
                print("Verbose mode enabled")

    return 0


if __name__ == "__main__":
    main()
