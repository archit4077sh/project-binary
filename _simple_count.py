import re
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
expected = 0
for fpath, exp in files:
    with open(fpath, encoding='utf-8') as f:
        src = f.read()
    count = src.count('**Task') + src.count('**Debug')
    total += count
    expected += exp
    status = 'OK' if count == exp else f'MISMATCH (expected {exp})'
    print(f'{os.path.basename(fpath):30s}: {count} {status}')

print()
print(f'Total: {total} / Expected: {expected}')
if total == expected:
    print('COUNT CHECK PASSED')
else:
    print('COUNT CHECK FAILED')
