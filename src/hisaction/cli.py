import argparse

from . import config


def get_args_parser(project_name):
    parser = argparse.ArgumentParser(prog=project_name)
    subparsers = parser.add_subparsers(dest="command")
    config_parser = subparsers.add_parser("config")
    config_parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose mode"
    )
    config_subparsers = config_parser.add_subparsers(dest="subcommand")
    adddirs_parser = config_subparsers.add_parser("adddirs")
    adddirs_parser.set_defaults(func=config_adddirs)
    show_parser = config_subparsers.add_parser("show")
    show_parser.set_defaults(func=lambda args: config_show(args, project_name))
    return parser


def config_adddirs(args):
    print("Config adddirs")
    if args.verbose:
        print("Verbose mode enabled")


def config_show(args, project_name):
    print(config.config_path(project_name))
    if args.verbose:
        print("Verbose mode enabled")
