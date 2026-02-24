"""
config.py — Central constants for the Frontend Question Automation System.
All values can be overridden via CLI args in main.py.
"""

# ─── Typing Simulation ────────────────────────────────────────────────────────
# Per-character keystroke delay bounds (seconds)
TYPING_DELAY_MIN = 0.03   # 30ms
TYPING_DELAY_MAX = 0.12   # 120ms

# Pause after punctuation (,  .  ;  :  !) in seconds
PUNCTUATION_PAUSE_MIN = 0.20
PUNCTUATION_PAUSE_MAX = 0.60

# Mid-paragraph "thinking" pause — inserted randomly at whitespace
THINKING_PAUSE_MIN = 0.50
THINKING_PAUSE_MAX = 1.50

# Probability (0.0–1.0) that any given whitespace triggers a thinking pause
THINKING_PAUSE_PROBABILITY = 0.04   # ~4% of spaces get a long pause

# ─── Session Config ───────────────────────────────────────────────────────────
# How many questions to send per session (overridable via --questions)
DEFAULT_MAX_QUESTIONS = 20

# Inter-question wait: (min seconds, max seconds)
WAIT_MIN_SECONDS = 180   # 3 minutes
WAIT_MAX_SECONDS = 300   # 5 minutes

# Countdown before first question (seconds) — time for user to click into input
DEFAULT_COUNTDOWN_SECONDS = 10

# ─── Question Quality ─────────────────────────────────────────────────────────
# Difficulty level: 1 = senior debugging, 3 = staff architecture, 5 = principal
DEFAULT_DIFFICULTY = 3

# ─── Fictional Product Context ────────────────────────────────────────────────
PRODUCT_CONTEXT = {
    "product": "Next.js 14 SaaS dashboard",
    "daily_users": "200k",
    "stack": ["React 18", "Next.js 14", "TypeScript 5", "Zustand", "React Query v5", "Tailwind CSS"],
    "features": [
        "large dynamic data table (10k+ rows, virtual scroll)",
        "role-based permission system (RBAC)",
        "real-time WebSocket updates via a custom useWebSocket hook",
        "microfrontend experiment using Module Federation",
        "a design system with ~80 shared components",
        "a CI pipeline running Jest + Playwright on every PR",
    ],
    "team_size": "12 engineers, 3 frontend-focused",
}
