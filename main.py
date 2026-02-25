"""
main.py - Orchestration loop for the Frontend Question Automation System.

Usage:
    python main.py                        # default: 20 questions, 10s countdown
    python main.py --questions 5          # send only 5 questions
    python main.py --dry-run              # print questions, no keyboard actions
    python main.py --countdown 15         # 15 second countdown before typing starts
    python main.py --difficulty 5         # question intensity (1-5, cosmetic label)
    python main.py --reset                # wipe saved state and start a fresh cycle
    python main.py --dry-run --questions 3 --difficulty 4
"""

import argparse
import sys

from config import DEFAULT_MAX_QUESTIONS, DEFAULT_COUNTDOWN_SECONDS, DEFAULT_DIFFICULTY
from session_memory import SessionMemory
import question_generator as qgen

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Frontend Engineering Question Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python main.py --dry-run --questions 5
  python main.py --questions 10 --countdown 15 --difficulty 3
        """
    )
    parser.add_argument(
        "--questions", "-q",
        type=int, default=DEFAULT_MAX_QUESTIONS,
        help=f"Number of questions to send (default: {DEFAULT_MAX_QUESTIONS})"
    )
    parser.add_argument(
        "--countdown", "-c",
        type=int, default=DEFAULT_COUNTDOWN_SECONDS,
        help=f"Seconds to wait before first keystroke (default: {DEFAULT_COUNTDOWN_SECONDS})"
    )
    parser.add_argument(
        "--difficulty", "-d",
        type=int, choices=[1, 2, 3, 4, 5], default=DEFAULT_DIFFICULTY,
        help="Question difficulty label 1-5 (1=senior debug, 5=principal design)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print questions to console only -- no keyboard actions fired"
    )
    parser.add_argument(
        "--reset", "-r", action="store_true",
        help="Delete saved session state and start a fresh question cycle"
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Difficulty label
# ---------------------------------------------------------------------------

DIFFICULTY_LABELS = {
    1: "Senior Debugging",
    2: "Senior Architecture",
    3: "Staff-Level Design",
    4: "Principal Tradeoffs",
    5: "Principal + Scale",
}


# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # Handle --reset before creating SessionMemory (which loads state)
    if args.reset:
        from session_memory import _STATE_FILE
        if _STATE_FILE.exists():
            _STATE_FILE.unlink()
            print("[*] Session state wiped. Starting a fresh question cycle.\n")
        else:
            print("[*] No saved state found — already starting fresh.\n")

    memory = SessionMemory()

    SEP = "=" * 60
    DIV = "-" * 60

    print(SEP)
    print("  [*] Frontend Question Automation System")
    print(f"  Mode      : {'DRY RUN (no typing)' if args.dry_run else 'LIVE (keyboard control)'}")
    print(f"  Questions : {args.questions}")
    print(f"  Difficulty: {args.difficulty} - {DIFFICULTY_LABELS[args.difficulty]}")
    print(f"  Countdown : {args.countdown}s")
    print(SEP)

    if not args.dry_run:
        # Import here so dry-run works even if pyautogui is missing
        import human_simulator as hs
        hs.countdown(args.countdown)
    else:
        print("\n[DRY RUN] No keyboard actions will be taken.\n")

    for q_num in range(1, args.questions + 1):
        theme, subtopic = memory.pick_next_theme()

        print(DIV)
        print(f"  Q{q_num:02d}/{args.questions:02d} | Theme: {theme} > {subtopic}")
        print(f"  {memory.stats()}")
        print(DIV)

        try:
            question = qgen.generate(theme, subtopic)
        except Exception as e:
            print(f"  [ERROR] Failed to generate question: {e}")
            memory.mark_used(theme, subtopic)
            continue

        memory.mark_used(theme, subtopic)

        if args.dry_run:
            print()
            print(question)
            print()
        else:
            import human_simulator as hs
            print("  [Clicking input to re-focus...]")
            hs.click_input()
            print("  [Typing...]")
            hs.type_humanly(question)
            hs.press_enter()
            print("  [Enter pressed OK]")

            if q_num < args.questions:
                hs.random_idle()

    print("\n" + SEP)
    print(f"  [DONE] Session complete - {args.questions} question(s) sent.")
    print(SEP + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user. Exiting.")
        sys.exit(0)
