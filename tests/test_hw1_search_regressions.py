"""Regression coverage for product-name search precision."""

import pytest

from agent import db, tools
from agent.auth import AuthContext


SUPPORT = AuthContext(user_id=9501, role="support")


def test_hw1_find_order_skips_empty_titles(world):
    # The standard seed deliberately includes a product with a missing title.
    with db.connection() as conn:
        assert conn.execute(
            "SELECT 1 FROM orders o JOIN products p ON p.id = o.product_id "
            "WHERE p.title = ''"
        ).fetchone() is not None
    assert tools.find_order(SUPPORT, "zzzznonexistent9999") == {
        "ok": True, "orders": []
    }


@pytest.mark.parametrize("query", [
    "Unique Search Fixture Product",
    "  UNIQUE   search fixture PRODUCT  ",
    "search fixture",
    "Unique Search Fixture Product I bought last week",
])
def test_hw1_find_order_matches_phrases_in_order(order_search_cases, query):
    _, expected = order_search_cases
    result = tools.find_order(SUPPORT, query)
    assert [order["order_id"] for order in result["orders"]] == expected["support"][:5]


def test_hw1_find_order_does_not_match_only_one_query_word(order_search_cases):
    assert tools.find_order(SUPPORT, "Unique zzzznonexistent9999") == {
        "ok": True, "orders": []
    }
