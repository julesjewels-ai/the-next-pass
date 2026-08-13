"""
Entry point for The 98% Career Platform CLI.

This module handles command-line arguments and interfaces with the
core application logic to help student-athletes translate their
skills into corporate value.
"""

import argparse
from typing import Dict, Callable
from src.core.models import AthleteProfile
from src.core.services import (
    translate_skills,
    match_careers,
    match_employers,
    match_opportunities,
    get_skill_demand_report,
    get_skill_gap_analysis
)


def handle_translate(args: argparse.Namespace) -> None:
    """Handles the 'translate' command."""
    profile = AthleteProfile(sport=args.sport, role=args.role)
    result = translate_skills(profile)
    print(f"\n--- Resume Translation for {args.sport} {args.role} ---")
    for raw, corpo in result.items():
        print(f"Athletic Context: \"{raw}\"")
        print(f"Resume Bullet:    \"{corpo}\"\n")


def handle_match(args: argparse.Namespace) -> None:
    """Handles the 'match' command."""
    print(
        f"\n--- Career Matches (Grit: {args.grit}, "
        f"Teamwork: {args.teamwork}) ---"
    )
    matches = match_careers(args.grit, args.teamwork)
    for job in matches:
        print(f"- {job.title}")
    print("\nStructure is gone. But your discipline remains.")


def handle_employers(args: argparse.Namespace) -> None:
    """Handles the 'employers' command."""
    profile = AthleteProfile(sport=args.sport, role=args.role)
    matches = match_employers(profile)
    print(f"\n--- Employer Matches for {args.sport} {args.role} ---")
    if not matches:
        print("No direct matches found. Keep training.")
    for employer in matches:
        print(f"- {employer.name} ({employer.industry})")
        print(f"  Required Skills: {', '.join(employer.required_skills)}")
    print("\nNetwork is net worth.")


def handle_opportunities(args: argparse.Namespace) -> None:
    """Handles the 'opportunities' command."""
    profile = AthleteProfile(sport=args.sport, role=args.role)
    print(f"\n--- Opportunity Matches for {args.sport} {args.role} ---")
    print(f"--- (Grit: {args.grit}, Teamwork: {args.teamwork}) ---\n")

    matches = match_opportunities(profile, args.grit, args.teamwork)

    if not matches:
        print("No direct matches found. Expand your skillset.")
        return

    for job in matches:
        print(f"- {job.title} ({job.employer})")

    print("\nPreparation meets opportunity.")


def handle_demand(args: argparse.Namespace) -> None:
    """Handles the 'demand' command."""
    print("\n--- Skill Demand Analytics ---")
    demand = get_skill_demand_report()
    if not demand:
        print("No job data available to calculate demand.")
        return

    for skill, count in demand.items():
        print(f"- {skill}: Required by {count} role(s)")

    print("\nTrain for what the market demands.")


def handle_gap(args: argparse.Namespace) -> None:
    """Handles the 'gap' command."""
    profile = AthleteProfile(sport=args.sport, role=args.role)
    print(f"\n--- Skill Gap Analysis for {args.sport} {args.role} ---")

    gaps = get_skill_gap_analysis(profile)

    if not gaps:
        print("You possess all currently demanded skills. Stay sharp.")
        return

    print("Missing Skills (Ranked by Market Demand):")
    for skill, count in gaps.items():
        print(f"- {skill} (Demanded by {count} role(s))")

    print("\nIdentify the gap. Bridge it.")


def main() -> None:
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="The 98%: Career Platform for Student-Athletes"
    )
    parser.add_argument(
        '--version', action='version', version='%(prog)s 0.1.0-mvp'
    )

    subparsers = parser.add_subparsers(
        dest='command', help='Available commands'
    )

    # Command: translate
    translate_parser = subparsers.add_parser(
        'translate',
        help='Translate athletic skills to corporate resume terms'
    )
    translate_parser.add_argument(
        '--sport',
        type=str,
        required=True,
        help='Sport played (e.g., Football, Swimming)'
    )
    translate_parser.add_argument(
        '--role',
        type=str,
        default='Player',
        help='Role within the team (e.g., Captain, Starter)'
    )

    # Command: match
    match_parser = subparsers.add_parser(
        'match',
        help='Find potential career matches based on athletic traits'
    )
    match_parser.add_argument(
        '--grit', type=int, default=8, help='Grit level (1-10)'
    )
    match_parser.add_argument(
        '--teamwork', type=int, default=9, help='Teamwork level (1-10)'
    )

    # Command: employers
    employers_parser = subparsers.add_parser(
        'employers',
        help='Find employers looking for your specific skills'
    )
    employers_parser.add_argument(
        '--sport',
        type=str,
        required=True,
        help='Sport played (e.g., Football, Swimming)'
    )
    employers_parser.add_argument(
        '--role',
        type=str,
        default='Player',
        help='Role within the team (e.g., Captain, Starter)'
    )

    # Command: opportunities
    opportunities_parser = subparsers.add_parser(
        'opportunities',
        help='Find specific job opportunities based on skills and traits'
    )
    opportunities_parser.add_argument(
        '--sport',
        type=str,
        required=True,
        help='Sport played (e.g., Football, Swimming)'
    )
    opportunities_parser.add_argument(
        '--role',
        type=str,
        default='Player',
        help='Role within the team (e.g., Captain, Starter)'
    )
    opportunities_parser.add_argument(
        '--grit', type=int, default=8, help='Grit level (1-10)'
    )
    opportunities_parser.add_argument(
        '--teamwork', type=int, default=9, help='Teamwork level (1-10)'
    )

    # Command: demand
    subparsers.add_parser(
        'demand',
        help='View market demand for specific skills'
    )

    # Command: gap
    gap_parser = subparsers.add_parser(
        'gap',
        help='Identify skills you are missing based on market demand'
    )
    gap_parser.add_argument(
        '--sport',
        type=str,
        required=True,
        help='Sport played (e.g., Football, Swimming)'
    )
    gap_parser.add_argument(
        '--role',
        type=str,
        default='Player',
        help='Role within the team (e.g., Captain, Starter)'
    )

    args = parser.parse_args()

    command_handlers: Dict[str, Callable[[argparse.Namespace], None]] = {
        'translate': handle_translate,
        'match': handle_match,
        'employers': handle_employers,
        'opportunities': handle_opportunities,
        'demand': handle_demand,
        'gap': handle_gap,
    }

    if args.command in command_handlers:
        command_handlers[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
