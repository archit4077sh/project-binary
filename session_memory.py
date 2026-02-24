"""
session_memory.py — Tracks used themes/subtopics across a session.
Ensures no topic is repeated until all have been exhausted (then resets).
"""

import random
from typing import Tuple, Dict, Set


# ─── Theme → Subtopic registry ────────────────────────────────────────────────
# Each theme maps to a list of specific subtopics.
THEME_REGISTRY: Dict[str, list[str]] = {
    "react_internals": [
        "re-render_debugging",
        "memoization_misuse",
        "reconciliation_key_issue",
        "suspense_edge_case",
        "strict_mode_double_invoke",
        "concurrent_rendering_teardown",
    ],
    "performance": [
        "bundle_splitting_strategy",
        "tree_shaking_failure",
        "react_profiler_bottleneck",
        "memory_leak_listeners",
        "virtualized_list_overscan",
        "layout_thrashing",
    ],
    "nextjs_advanced": [
        "ssr_hydration_mismatch",
        "streaming_rsc",
        "server_vs_client_components",
        "edge_runtime_limitation",
        "caching_stale_data",
        "middleware_redirect_loop",
    ],
    "typescript": [
        "complex_generic_inference",
        "mapped_type_pitfall",
        "discriminated_union_narrowing",
        "deep_readonly_mutation",
        "conditional_type_distribution",
        "infer_keyword_usage",
    ],
    "architecture": [
        "monorepo_package_boundary",
        "microfrontend_state_sharing",
        "design_system_versioning",
        "feature_flag_architecture",
        "code_splitting_boundary",
        "component_library_breaking_change",
    ],
    "debugging": [
        "race_condition_in_hook",
        "stale_closure_trap",
        "infinite_render_loop",
        "event_delegation_leak",
        "useeffect_dependency_bug",
        "ref_callback_timing",
    ],
    "state_management": [
        "zustand_vs_redux_tradeoff",
        "server_vs_client_state",
        "optimistic_update_rollback",
        "react_query_cache_invalidation",
        "normalization_strategy",
        "derived_state_antipattern",
    ],
    "css_rendering": [
        "layout_shift_cls",
        "repaint_from_animation",
        "css_containment",
        "style_recalculation_cost",
        "css_in_js_runtime_perf",
        "font_loading_foit_fout",
    ],
    "testing": [
        "flaky_e2e_timing",
        "jest_slow_suite",
        "async_race_in_test",
        "msw_vs_fetch_mock",
        "snapshot_anti_pattern",
        "testing_library_role_query",
    ],
}


class SessionMemory:
    def __init__(self) -> None:
        self._used: Set[Tuple[str, str]] = set()
        self._all_pairs: list[Tuple[str, str]] = [
            (theme, subtopic)
            for theme, subtopics in THEME_REGISTRY.items()
            for subtopic in subtopics
        ]
        self._available: list[Tuple[str, str]] = list(self._all_pairs)
        random.shuffle(self._available)
        self._last_theme: str | None = None

    def pick_next_theme(self) -> Tuple[str, str]:
        """Pick the next (theme, subtopic) pair, avoiding the last used theme."""
        if not self._available:
            # All topics exhausted — reset pool
            self._available = list(self._all_pairs)
            random.shuffle(self._available)
            self._used.clear()

        # Try to avoid repeating the same theme consecutively
        candidates = [
            p for p in self._available if p[0] != self._last_theme
        ]
        if not candidates:
            candidates = self._available  # fall back if only one theme left

        chosen = random.choice(candidates)
        return chosen

    def mark_used(self, theme: str, subtopic: str) -> None:
        """Record that this pair was sent."""
        pair = (theme, subtopic)
        self._used.add(pair)
        self._last_theme = theme
        if pair in self._available:
            self._available.remove(pair)

    def stats(self) -> str:
        total = len(self._all_pairs)
        used = len(self._used)
        return f"[Memory] {used}/{total} topics used this session"
