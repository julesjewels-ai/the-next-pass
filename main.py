"""
Entry point for The 98% Career Platform CLI.

This module handles command-line arguments and interfaces with the core application logic
to help student-athletes translate their skills into corporate value.
"""

import argparse
from src.core.app import CareerPlatform, AthleteProfile

def main() -> None:
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="The 98%: Career Platform for Student-Athletes"
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0-mvp')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Command: translate
    translate_parser = subparsers.add_parser('translate', help='Translate athletic skills to corporate resume terms')
    translate_parser.add_argument('--sport', type=str, required=True, help='Sport played (e.g., Football, Swimming)')
    translate_parser.add_argument('--role', type=str, default='Player', help='Role within the team (e.g., Captain, Starter)')

    # Command: match
    match_parser = subparsers.add_parser('match', help='Find potential career matches based on athletic traits')
    match_parser.add_argument('--grit', type=int, default=8, help='Grit level (1-10)')
    match_parser.add_argument('--teamwork', type=int, default=9, help='Teamwork level (1-10)')

    args = parser.parse_args()

    platform = CareerPlatform()

    if args.command == 'translate':
        profile = AthleteProfile(sport=args.sport, role=args.role)
        result = platform.translate_skills(profile)
        print(f"\n--- Resume Translation for {args.sport} {args.role} ---")
        for raw, corpo in result.items():
            print(f"Athletic Context: \"{raw}\"")
            print(f"Resume Bullet:    \"{corpo}\"\n")
            
    elif args.command == 'match':
        print(f"\n--- Finding Career Matches (Grit: {args.grit}, Teamwork: {args.teamwork}) ---")
        matches = platform.match_careers(args.grit, args.teamwork)
        for job in matches:
            print(f"- {job}")
        print("\nStructure is gone. But your discipline remains.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()