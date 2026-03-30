"""
Counts questions per file by counting list-separator triple-quotes.
Each question element in the list is bounded by triple-quotes.
The module docstring also has 2 triple-quotes (one open, one close).
Formula: (total_triplequote_count - 2_for_docstring) / 2 = number of questions
"""
import os

files = [
    ('snippets/q_react.py', 56),
    ('snippets/q_performance.py', 56),
    ('snippets/q_nextjs.py', 56),
    ('snippets/q_typescript.py', 56),
    ('snippets/q_architecture.py', 55),
    ('snippets/q_debugging.py', 56),
    ('snippets/q_state.py', 55),
    ('snippets/q_css.py', 55),
    ('snippets/q_testing.py', 55),
]

total = 0
expected_total = 0
all_ok = True

for fpath, exp in files:
    with open(fpath, encoding='utf-8') as f:
        src = f.read()
    # Count all occurrences of """
    tq_count = src.count('"""')
    # Subtract 2 for the module docstring (open + close), divide by 2
    count = (tq_count - 2) // 2
    total += count
    expected_total += exp
    status = 'OK' if count == exp else f'MISMATCH (expected {exp})'
    if count != exp:
        all_ok = False
    print(f'{os.path.basename(fpath):30s}: {count:3d}  {status}')

print()
print(f'Total: {total} / Expected: {expected_total}')
if all_ok and total == expected_total:
    print('COUNT CHECK PASSED ✓')
else:
    print('COUNT CHECK FAILED ✗')
