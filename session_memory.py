"""
session_memory.py — Tracks used questions across sessions (persistent).

State is saved to `session_state.json` in the project root after every question
is marked used. On the next run the remaining pool is restored, so no question
repeats until all 252 have been asked, even across restarts.

When the pool is exhausted it resets automatically and starts a new cycle.
"""

import json
import os
import random
from pathlib import Path
from typing import Tuple, Dict, Set

# ─── State file ───────────────────────────────────────────────────────────────
_STATE_FILE = Path(__file__).parent / "session_state.json"


def _build_registry() -> Dict[str, list[str]]:
    """
    Build a registry where each theme maps to index strings for its questions.
    Imports each snippet file to discover the actual question count.
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

    mapping = {
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
    return {theme: [str(i) for i in range(len(qs))] for theme, qs in mapping.items()}


# Build at module load time once
THEME_REGISTRY: Dict[str, list[str]] = _build_registry()


class SessionMemory:
    def __init__(self) -> None:
        self._all_pairs: list[Tuple[str, str]] = [
            (theme, subtopic)
            for theme, subtopics in THEME_REGISTRY.items()
            for subtopic in subtopics
        ]
        self._used: Set[Tuple[str, str]] = set()
        self._last_theme: str | None = None

        # Try to restore from disk; fall back to a fresh shuffled pool
        self._available = self._load_state()

    # ── Persistence ──────────────────────────────────────────────────────────

    def _load_state(self) -> list[Tuple[str, str]]:
        """
        Load the remaining question pool from disk.

        If the file doesn't exist, is corrupted, or contains an empty pool,
        return a freshly shuffled full pool (starts a new cycle).
        """
        if _STATE_FILE.exists():
            try:
                data = json.loads(_STATE_FILE.read_text(encoding="utf-8"))
                available = [tuple(pair) for pair in data.get("available", [])]
                used = {tuple(pair) for pair in data.get("used", [])}
                self._last_theme = data.get("last_theme")

                # Validate: all pairs must be known
                all_set = set(map(tuple, self._all_pairs))
                available = [p for p in available if p in all_set]
                used = {p for p in used if p in all_set}

                if available:
                    self._used = used
                    print(
                        f"[Memory] Restored state — "
                        f"{len(used)}/{len(self._all_pairs)} questions already asked "
                        f"({len(available)} remaining)"
                    )
                    return list(available)
                else:
                    print(
                        "[Memory] All questions have been asked — "
                        "resetting for a new cycle."
                    )
            except Exception as exc:
                print(f"[Memory] Could not read state file ({exc}), starting fresh.")

        # Fresh start
        pool = list(self._all_pairs)
        random.shuffle(pool)
        print(f"[Memory] Starting fresh — {len(pool)} questions available.")
        return pool

    def _save_state(self) -> None:
        """Persist the current pool and used set to disk."""
        data = {
            "available": [list(p) for p in self._available],
            "used":      [list(p) for p in self._used],
            "last_theme": self._last_theme,
        }
        _STATE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ── Public API ───────────────────────────────────────────────────────────

    def pick_next_theme(self) -> Tuple[str, str]:
        """Pick the next (theme, subtopic) pair, avoiding the last used theme."""
        if not self._available:
            # All 252 questions exhausted — reset for a new cycle
            self._available = list(self._all_pairs)
            random.shuffle(self._available)
            self._used.clear()
            self._save_state()
            print("[Memory] Full cycle complete — starting a new cycle.")

        # Avoid two questions from the same theme back-to-back
        candidates = [p for p in self._available if p[0] != self._last_theme]
        if not candidates:
            candidates = self._available  # fallback if only one theme left

        return random.choice(candidates)

    def mark_used(self, theme: str, subtopic: str) -> None:
        """Record that this question was sent, then persist to disk."""
        pair = (theme, subtopic)
        self._used.add(pair)
        self._last_theme = theme
        if pair in self._available:
            self._available.remove(pair)
        self._save_state()

    def stats(self) -> str:
        total = len(self._all_pairs)
        used = len(self._used)
        remaining = len(self._available)
        return f"[Memory] {used}/{total} questions asked this cycle  ({remaining} remaining)"
