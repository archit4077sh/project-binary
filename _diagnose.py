"""
Diagnose: count triple-quotes in each file to find issues.
"""
import os

files = [
    'snippets/q_react.py',
    'snippets/q_performance.py',
    'snippets/q_nextjs.py',
    'snippets/q_typescript.py',
    'snippets/q_architecture.py',
    'snippets/q_debugging.py',
    'snippets/q_state.py',
    'snippets/q_css.py',
    'snippets/q_testing.py',
]

for fpath in files:
    with open(fpath, encoding='utf-8') as f:
        src = f.read()
    dq = src.count('"""')
    sq = src.count("'''")
    # Each question: 2 triple-quotes. Module docstring: 2 triple-quotes.
    # If dq is odd, there's a broken string.
    odd = 'BROKEN (odd count!)' if dq % 2 != 0 else ''
    # Expected list count = (dq - 2) / 2
    expected_from_dq = (dq - 2) // 2
    print(f"{os.path.basename(fpath):30s}: dq={dq:4d}  sq={sq:2d}  list_items_guess={expected_from_dq:3d}  {odd}")
