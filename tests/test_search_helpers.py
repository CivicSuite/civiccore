from __future__ import annotations

import uuid

from civiccore.search import (
    normalize_search_query,
    normalize_search_text,
    reciprocal_rank_fusion,
    search_text_matches_query,
)


def test_normalize_search_text_collapses_case_and_whitespace() -> None:
    assert normalize_search_text("  Budget\tMeeting \n Packet  ") == "budget meeting packet"


def test_normalize_search_query_uses_same_rules_as_text() -> None:
    assert normalize_search_query("  Closed   Session ") == "closed session"


def test_search_text_matches_query_is_case_insensitive_and_whitespace_stable() -> None:
    assert search_text_matches_query(
        text="Closed   Cybersecurity Briefing",
        query="  cybersecurity   briefing ",
    )


def test_search_text_matches_query_treats_blank_query_as_match() -> None:
    assert search_text_matches_query(text="Anything", query="   ")


def test_reciprocal_rank_fusion_combines_both_result_sets() -> None:
    result_a, result_b, result_c = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()

    fused = reciprocal_rank_fusion(
        [(result_a, 0.1), (result_b, 0.2)],
        [(result_b, 0.9), (result_c, 0.8)],
    )

    fused_ids = [result_id for result_id, _ in fused]
    assert fused_ids == [result_b, result_a, result_c]
    assert all(score > 0 for _, score in fused)


def test_reciprocal_rank_fusion_allows_empty_inputs() -> None:
    assert reciprocal_rank_fusion([], []) == []
