def inc(n: int) -> int:
    return n + 1

from tasks3.cli import build_parser

def main(argv=None) -> None:
    p = build_parser()
    # parse provided argv (or sys.argv by default)
    args = p.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        p.print_help()