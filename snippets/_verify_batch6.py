"""
Count and dedup verification for Batch 6 (500 new questions).
Run: python _verify_batch6.py  (from snippets/ directory)
"""
import ast, hashlib, os, sys, re

BASE = os.path.dirname(__file__)
BATCH6_DIR = BASE
ARCHIVE_DIRS = [
    os.path.join(BASE, "archive"),
    os.path.join(BASE, "archive", "batch2"),
    os.path.join(BASE, "archive", "batch3"),
    os.path.join(BASE, "archive", "batch4"),
    os.path.join(BASE, "archive", "batch5"),
]
BATCH6_FILES = {
    "q_react.py":        "Q_REACT",
    "q_performance.py":  "Q_PERFORMANCE",
    "q_nextjs.py":       "Q_NEXTJS",
    "q_typescript.py":   "Q_TYPESCRIPT",
    "q_architecture.py": "Q_ARCHITECTURE",
    "q_debugging.py":    "Q_DEBUGGING",
    "q_state.py":        "Q_STATE",
    "q_css.py":          "Q_CSS",
    "q_testing.py":      "Q_TESTING",
}

def fingerprint(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r'```[\s\S]*?```', '', t)
    t = re.sub(r'\s+', ' ', t)
    return hashlib.md5(t.encode()).hexdigest()

def load_questions(filepath: str, varname: str) -> list:
    try:
        with open(filepath, encoding='utf-8') as f:
            src = f.read()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == varname:
                        if isinstance(node.value, ast.List):
                            return [ast.literal_eval(e) for e in node.value.elts]
    except Exception as e:
        print(f"  [WARN] Could not parse {filepath}: {e}")
    return []

# ── Archive fingerprints ───────────────────────────────────────────────────
archive_fps: set = set()
archive_total = 0
for adir in ARCHIVE_DIRS:
    if not os.path.isdir(adir):
        print(f"  [WARN] Archive dir not found: {adir}")
        continue
    for fname in sorted(os.listdir(adir)):
        if not fname.endswith('.py') or fname.startswith('_'):
            continue
        fpath = os.path.join(adir, fname)
        # Try common variable name patterns
        stem = os.path.splitext(fname)[0]   # e.g. "q_react"
        varname = stem.upper()              # "Q_REACT"
        qs = load_questions(fpath, varname)
        if qs:
            archive_fps.update(fingerprint(q) for q in qs)
            archive_total += len(qs)

print(f"Archive: {archive_total} questions ({len(archive_fps)} unique fingerprints)\n")

# ── Batch 6 count & fingerprints ───────────────────────────────────────────
all_fps: list = []
batch6_total = 0

for fname, varname in BATCH6_FILES.items():
    fpath = os.path.join(BATCH6_DIR, fname)
    qs = load_questions(fpath, varname)
    fps = [fingerprint(q) for q in qs]
    all_fps.extend(fps)
    batch6_total += len(qs)
    print(f"  {fname:25s}: {len(qs):3d} questions")

batch6_unique = len(set(all_fps))
print(f"\nBatch 6 TOTAL    : {batch6_total}")
print(f"Batch 6 UNIQUE   : {batch6_unique}")

# Internal duplicates
seen: set = set()
internal_dups = 0
for fp in all_fps:
    if fp in seen:
        internal_dups += 1
    seen.add(fp)
print(f"Internal dups    : {internal_dups}")

# Archive overlaps
overlaps = archive_fps & set(all_fps)
print(f"Archive overlaps : {len(overlaps)}")

print("\n" + "=" * 52)
ok = batch6_total == 500 and internal_dups == 0 and len(overlaps) == 0
if ok:
    print("✅  PASS — 500 questions, 0 internal dups, 0 archive overlaps")
else:
    if batch6_total != 500:
        print(f"❌  Total: expected 500, got {batch6_total}")
    if internal_dups:
        print(f"❌  Internal duplicates: {internal_dups}")
    if overlaps:
        print(f"❌  Archive overlaps: {len(overlaps)}")
    sys.exit(1)
