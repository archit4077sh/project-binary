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
all_ok = True

for fpath, exp in files:
    with open(fpath, encoding='utf-8') as f:
        src = f.read()
    dq = src.count('"""')
    sq = src.count("'''")
    # Each question is delimited by either ''' or """
    # module docstring: 2 triple-double-quotes
    # If file was converted to single quotes:
    #   all list items use '''  -> count = sq // 2
    # If file still uses double quotes:
    #   module docstring = 2 triple-double-quotes
    #   list items = the rest -> count = (dq - 2) // 2
    if sq > 0 and dq == 2:
        # Converted: module doc uses """, list items use '''
        count = sq // 2
    elif sq == 0:
        # Unconverted: all use """
        count = (dq - 2) // 2
    else:
        # Mixed - something went wrong
        count = (dq - 2) // 2 + sq // 2

    total += count
    expected += exp
    ok = 'OK' if count == exp else f'MISMATCH (expected {exp})'
    if count != exp:
        all_ok = False
    print(f'{os.path.basename(fpath):30s}: {count:3d}  dq={dq}  sq={sq}  {ok}')

print()
print(f'Total: {total} / Expected: {expected}')
print('PASS' if (all_ok and total == expected) else 'FAIL')
