"""
Entry point for The 98% Career Platform CLI.

This module handles command-line arguments and interfaces with the core application logic
to help student-athletes translate their skills into corporate value.
"""

import argparse
from typing import Dict, Callable
from src.core.app import AthleteProfile, translate_skills, match_careers
from src.core.export import MarkdownResumeGenerator, validate_filename


def handle_translate(args: argparse.Namespace) -> None:
    """Handles the 'translate' command."""
    profile = AthleteProfile(sport=args.sport, role=args.role)
    result = translate_skills(profile)
    print(f"\n--- Resume Translation for {args.sport} {args.role} ---")
    for raw, corpo in result.items():
        print(f"Athletic Context: \"{raw}\"")
        print(f"Resume Bullet:    \"{corpo}\"\n")

    if args.output:
        if not validate_filename(args.output):
            print(
                f"Error: Invalid filename '{args.output}'. "
                "Cannot contain path traversal characters."
            )
            return

        generator = MarkdownResumeGenerator()
        content = generator.generate(profile, result)
        try:
            with open(args.output, "w") as f:
                f.write(content)
            print(f"Successfully exported resume to {args.output}")
        except IOError as e:
            print(f"Error writing to file: {e}")


def handle_match(args: argparse.Namespace) -> None:
    """Handles the 'match' command."""
    print(f"\n--- Finding Career Matches (Grit: {args.grit}, Teamwork: {args.teamwork}) ---")
    matches = match_careers(args.grit, args.teamwork)
    for job in matches:
        print(f"- {job}")
    print("\nStructure is gone. But your discipline remains.")


def main() -> None:
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="The 98%: Career Platform for Student-Athletes"
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0-mvp')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Command: translate
    translate_parser = subparsers.add_parser(
        'translate', help='Translate athletic skills to corporate resume terms'
    )
    translate_parser.add_argument(
        '--sport', type=str, required=True, help='Sport played (e.g., Football, Swimming)'
    )
    translate_parser.add_argument(
        '--role', type=str, default='Player', help='Role within the team (e.g., Captain, Starter)'
    )
    translate_parser.add_argument(
        '--output', type=str, help='Output filename for resume (e.g., resume.md)'
    )

    # Command: match
    match_parser = subparsers.add_parser(
        'match', help='Find potential career matches based on athletic traits'
    )
    match_parser.add_argument(
        '--grit', type=int, default=8, help='Grit level (1-10)'
    )
    match_parser.add_argument(
        '--teamwork', type=int, default=9, help='Teamwork level (1-10)'
    )

    args = parser.parse_args()

    command_handlers: Dict[str, Callable[[argparse.Namespace], None]] = {
        'translate': handle_translate,
        'match': handle_match,
    }

    if args.command in command_handlers:
        command_handlers[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
