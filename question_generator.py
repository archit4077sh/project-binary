"""
question_generator.py - Returns questions from the expanded 252-question bank.

Each theme has 28 questions pre-written in its snippets/q_<theme>.py file.
The generate() function picks a question by index from the correct list.
No LLM API required.
"""

from snippets.q_react       import Q_REACT
from snippets.q_performance  import Q_PERFORMANCE
from snippets.q_nextjs       import Q_NEXTJS
from snippets.q_typescript   import Q_TYPESCRIPT
from snippets.q_architecture import Q_ARCHITECTURE
from snippets.q_debugging    import Q_DEBUGGING
from snippets.q_state        import Q_STATE
from snippets.q_css          import Q_CSS
from snippets.q_testing      import Q_TESTING

# Map theme name → question list
_THEME_QUESTIONS: dict[str, list[str]] = {
    "react_internals":  Q_REACT,
    "performance":      Q_PERFORMANCE,
    "nextjs_advanced":  Q_NEXTJS,
    "typescript":       Q_TYPESCRIPT,
    "architecture":     Q_ARCHITECTURE,
    "debugging":        Q_DEBUGGING,
    "state_management": Q_STATE,
    "css_rendering":    Q_CSS,
    "testing":          Q_TESTING,
}


def generate(theme: str, subtopic: str) -> str:
    """
    Return the question identified by (theme, subtopic).

    subtopic is a zero-padded integer string ("00", "01", ...) representing
    the index into the theme's question list. This is produced by
    session_memory.py's THEME_REGISTRY which auto-generates index labels.

    Returns the question text, stripped of leading/trailing whitespace.
    """
    questions = _THEME_QUESTIONS.get(theme)
    if questions is None:
        raise ValueError(f"Unknown theme: {theme!r}")

    try:
        idx = int(subtopic)
    except (ValueError, TypeError):
        raise ValueError(f"subtopic must be a numeric index string, got: {subtopic!r}")

    if idx < 0 or idx >= len(questions):
        raise IndexError(
            f"Index {idx} out of range for theme {theme!r} "
            f"(has {len(questions)} questions)"
        )

    return questions[idx].strip()


def theme_size(theme: str) -> int:
    """Return the number of questions available for a given theme."""
    questions = _THEME_QUESTIONS.get(theme)
    if questions is None:
        raise ValueError(f"Unknown theme: {theme!r}")
    return len(questions)
