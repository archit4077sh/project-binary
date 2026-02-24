# Frontend Engineering Question Automation System

A Python script that **generates realistic senior/staff-level frontend engineering questions** and **types them into any AI chat interface** using OS-level keyboard simulation — no browser automation, no API key required.

---

## How It Works

1. You open your preferred AI tool (ChatGPT, Claude, Gemini, etc.) and click into the chat input
2. Run the script — it counts down from 10 seconds
3. You switch to the browser before the countdown ends
4. The script types questions character-by-character with human-like timing and presses Enter
5. It waits 3–7 minutes, then types the next question
6. Each question comes from a different theme (React, Next.js, TypeScript, Architecture, etc.)

---

## Setup

### 1. Create a virtual environment

```powershell
cd c:\Users\archi\Desktop\projects\project-binary
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

> Only one dependency: `pyautogui` — for OS-level keyboard simulation.

---

## Usage

### Dry-run (no keyboard actions — just preview questions)

```powershell
python main.py --dry-run --questions 5
```

### Live run (types into your active window)

```powershell
python main.py --questions 10 --countdown 10
```

1. Run the command
2. Click into the chat input box within 10 seconds
3. The script takes over and types

### All options

```
--questions   -q   Number of questions to send   (default: 20)
--countdown   -c   Seconds before typing starts  (default: 10)
--difficulty  -d   Label 1–5 (cosmetic)          (default: 3)
--dry-run          Print questions, no typing
```

### Examples

```powershell
python main.py --dry-run --questions 3 --difficulty 5
python main.py --questions 5 --countdown 15
python main.py -q 20 -c 10 -d 3
```

---

## Project Structure

```
project-binary/
├── main.py                  # Orchestration + CLI
├── config.py                # Timing constants, session defaults
├── session_memory.py        # Theme rotation — no topic repeats
├── question_generator.py    # Template-based question generation
├── human_simulator.py       # pyautogui keyboard automation
├── requirements.txt
├── snippets/
│   ├── react.py             # React/TypeScript code snippets
│   ├── nextjs.py            # Next.js 14 code snippets
│   └── typescript.py        # Advanced TS code snippets
└── README.md
```

---

## Question Themes

The script rotates across 9 categories, never repeating a subtopic until all are exhausted:

| Theme | Example subtopics |
|---|---|
| React Internals | re-render debugging, stale closure, Suspense edge cases |
| Performance | bundle splitting, tree shaking, memory leaks, layout thrashing |
| Next.js Advanced | SSR hydration mismatch, RSC streaming, middleware bugs |
| TypeScript | conditional types, mapped types, discriminated unions |
| Architecture | monorepo boundaries, microfrontend state, feature flags |
| Debugging | race conditions, infinite render loops, event listener leaks |
| State Management | Zustand vs Redux, optimistic updates, React Query cache |
| CSS & Rendering | CLS debugging, CSS-in-JS perf, style recalculation |
| Testing | flaky E2E, MSW patterns, Jest suite performance |

---

## Timing Behavior

| Event | Range |
|---|---|
| Keystroke delay | 30–120ms per character |
| After `,` `.` `;` | 200–600ms pause |
| Random "thinking" pause | 500–1500ms (~4% of spaces) |
| Between questions | 3–7 minutes (randomized) |

---

## Notes

- **pyautogui FAILSAFE**: moving your mouse to the top-left corner of the screen will abort the script
- Questions contain realistic code snippets, observed production issues, and expert-level asks
- All questions are grounded in a fictional Next.js 14 SaaS dashboard with 200k daily users
