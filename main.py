import argparse
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

import formatter

TOPICS_PATH = Path(__file__).resolve().parent / "config" / "topics.yaml"


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


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate(args):
    if args.ranters < 1:
        fail(f"--ranters must be >= 1, got {args.ranters}")
    d = args.date
    try:
        valid = len(d) == 10 and datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m-%d") == d
    except ValueError:
        valid = False
    if not valid:
        fail(f"--date must be a valid date in YYYY-MM-DD format (e.g. 2026-09-16), got '{d}'")


def resolve_topic(slug):
    """Return (display_name, slug) for a valid slug, or (None, None) when no topic."""
    if slug is None:
        return None, None
    with open(TOPICS_PATH, "r", encoding="utf-8") as f:
        topics = yaml.safe_load(f)["topics"]
    by_slug = {t["slug"]: t for t in topics}
    if slug not in by_slug:
        valid = "\n".join(f"  {s}" for s in sorted(by_slug))
        fail(f"unknown topic slug '{slug}'. Valid slugs:\n{valid}")
    return by_slug[slug]["display_name"], slug


def unique_path(out_dir, base):
    candidate = out_dir / f"{base}.docx"
    n = 2
    while candidate.exists():
        candidate = out_dir / f"{base}_{n}.docx"
        n += 1
    return candidate


def main():
    args = parse_args()
    validate(args)
    display_name, slug = resolve_topic(args.topic)

    document = formatter.create_document()
    formatter.add_footer(document)
    formatter.add_header(document, date=args.date, topic=display_name)
    formatter.add_page1_content(document, topic_slug=slug)
    formatter.add_speaker_prep_sheet(document)
    formatter.add_listener_notes(document, args.ranters)
    formatter.add_post_class_reflection(document, args.ranters, date=args.date)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    base = f"rant-circle_{slug or 'no-topic'}_{args.date.replace('-', '')}"
    while True:
        path = unique_path(out_dir, base)
        try:
            with open(path, "xb") as f:  # exclusive create: never overwrite
                document.save(f)
            break
        except FileExistsError:
            continue
    print(path)


if __name__ == "__main__":
    main()
