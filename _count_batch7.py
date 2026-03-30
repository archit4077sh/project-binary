import re, os, hashlib

FILES = [
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

ARCHIVE_DIRS = [
    'snippets/archive/batch1',
    'snippets/archive/batch2',
    'snippets/archive/batch3',
    'snippets/archive/batch4',
    'snippets/archive/batch5',
    'snippets/archive/batch6',
]

def extract_questions(filepath):
    """Extract triple-quoted strings that begin with **Task** or **Debug**."""
    with open(filepath, encoding='utf-8') as f:
        src = f.read()
    # Find all triple-quoted string contents
    pattern = re.compile(r'"""(.*?)"""', re.DOTALL)
    questions = []
    for m in pattern.finditer(src):
        content = m.group(1).strip()
        if content.startswith('**Task') or content.startswith('**Debug'):
            questions.append(content)
    return questions

def fingerprint(text):
    # Remove code fences, strip whitespace, lowercase — then hash
    cleaned = re.sub(r'```[\w]*', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
    return hashlib.md5(cleaned.encode()).hexdigest()

# ── Count new questions ───────────────────────────────────────────────────────
new_questions = []
print("=== NEW BATCH 7 COUNTS ===")
for f in FILES:
    qs = extract_questions(f)
    print(f"  {os.path.basename(f):30s}: {len(qs)}")
    new_questions.extend(qs)
print(f"  {'TOTAL':30s}: {len(new_questions)}\n")

# ── Collect archive fingerprints ─────────────────────────────────────────────
archive_fps = set()
for adir in ARCHIVE_DIRS:
    if not os.path.isdir(adir):
        print(f"WARNING: archive dir not found: {adir}")
        continue
    for fname in os.listdir(adir):
        if fname.endswith('.py'):
            qs = extract_questions(os.path.join(adir, fname))
            for q in qs:
                archive_fps.add(fingerprint(q))

print(f"Archive fingerprints loaded: {len(archive_fps)}")

# ── Check for duplicates ──────────────────────────────────────────────────────
duplicates = []
seen_new = set()
internal_dups = []

for q in new_questions:
    fp = fingerprint(q)
    if fp in archive_fps:
        duplicates.append(q[:120])
    if fp in seen_new:
        internal_dups.append(q[:120])
    seen_new.add(fp)

print(f"\n=== DEDUPLICATION RESULTS ===")
print(f"  Duplicates vs archive: {len(duplicates)}")
print(f"  Internal duplicates:   {len(internal_dups)}")

if duplicates:
    print("\nARCHIVE DUPLICATES:")
    for d in duplicates:
        print(f"  - {d}")

if internal_dups:
    print("\nINTERNAL DUPLICATES:")
    for d in internal_dups:
        print(f"  - {d}")

if not duplicates and not internal_dups:
    print("\n✓ All questions are unique — zero duplicates found!")
