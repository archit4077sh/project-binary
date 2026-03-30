"""
Convert all batch7 question files from broken triple-double-quote strings
to working triple-single-quote strings.

Run: python _fix_quotes.py
"""
import re
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

    # Check if file uses triple single quotes already (already converted)
    if "'''" in src and '"""' not in src[src.find("'''"):]:
        print(f"SKIP (already uses '''): {fpath}")
        continue

    # Strategy: replace the outer """ delimiters with '''
    # The module docstring starts the file: """..."""
    # The list items each start and end with """
    # We need to:
    # 1) Keep module docstring as """ (it won't have internal """)
    # 2) Replace list item """ with '''
    # The module docstring ends at the first """ after the opening """
    # Find module docstring:
    doc_start = src.index('"""')
    doc_end   = src.index('"""', doc_start + 3) + 3
    module_doc = src[doc_start:doc_end]

    # The rest of the file content after the module docstring:
    rest = src[doc_end:]

    # In rest: each question is delimited by """..."""
    # Replace these with '''...'''
    # Simple approach: replace all """ in rest with '''
    rest_converted = rest.replace('"""', "'''")

    new_src = src[:doc_end] + rest_converted

    # Also fix the variable assignment line if it has """
    # (module_doc uses """, rest now uses ''')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_src)

    print(f"CONVERTED: {fpath}")

# Now count to verify
print("\n=== COUNTS AFTER FIX ===")
total = 0
for fpath in files:
    with open(fpath, encoding='utf-8') as f:
        src = f.read()
    # Count ''' occurrences
    tq = src.count("'''")
    # All ''' in the file are list item delimiters (module doc still uses """)
    count = tq // 2
    total += count
    print(f"  {os.path.basename(fpath):30s}: {count}")
print(f"  {'TOTAL':30s}: {total}")
