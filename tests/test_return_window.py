"""Offline regression coverage for the delivery-age capability gap."""
import pytest
from agent.auth import AuthContext
from agent.tools import check_return_window_logic
from agent.agent import TOOLS_BY_ROLE

CTX = AuthContext(user_id=1, role="shopper")

@pytest.mark.parametrize("age,within,remaining", [(10, True, 4), (14, True, 0), (15, False, 0)])
def test_juniper_override_and_inclusive_boundary(world, age, within, remaining):
    result = check_return_window_logic(CTX, "Juniper Home Goods", age)
    assert result["return_window_days"] == 14
    assert result["within_return_window"] is within
    assert result["days_remaining"] == remaining
    assert "store-juniper-home-goods-policy" in result["policy_ids"]


def test_platform_default(world):
    result = check_return_window_logic(CTX, "Blue Heron Ceramics", 20)
    assert result["return_window_days"] == 30
    assert result["within_return_window"] is True
    assert result["days_remaining"] == 10

@pytest.mark.parametrize("age", [-1, 1.5, True])
def test_invalid_delivery_age(world, age):
    assert check_return_window_logic(CTX, "Juniper Home Goods", age)["error"] == "invalid_argument"

@pytest.mark.parametrize("store,error", [("", "invalid_argument"), ("Unknown Store", "not_found")])
def test_invalid_store(world, store, error):
    assert check_return_window_logic(CTX, store, 10)["error"] == error


def test_registered_for_all_roles():
    assert all(any(t.name == "check_return_window" for t in tools) for tools in TOOLS_BY_ROLE.values())
