import argparse
from datetime import date


def parse_args():
    parser = argparse.ArgumentParser(description="Rant Circle document generator")
    parser.add_argument(
        "--ranters",
        type=int,
        required=True,
        help="Number of students expected to rant (drives all page generation)",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Topic slug to look up in config/topics.yaml",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=date.today().isoformat(),
        help="Session date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="./output",
        help="Output directory (default: ./output)",
    )
    return parser.parse_args()


def validate(args):
    if args.ranters < 1:
        print(f"Error: --ranters must be >= 1, got {args.ranters}")
        raise SystemExit(1)


def main():
    args = parse_args()
    validate(args)

    print(f"Ranters: {args.ranters}")
    print(f"Topic: {args.topic}")
    print(f"Date: {args.date}")
    print(f"Output directory: {args.out}")


if __name__ == "__main__":
    main()
