from decimal import Decimal

import pytest

from main import OrderLine, RestaurantSystem


@pytest.fixture
def rs():
    return RestaurantSystem()


def test_default_menu_loaded(rs):
    assert len(rs.menu) == 5
    assert rs.menu[1].name == "Chicken Burger"


def test_add_to_order_merges_same_item(rs):
    order = []
    rs.add_to_order(order, 1, 2)
    rs.add_to_order(order, 1, 3)
    assert len(order) == 1
    assert order[0].qty == 5


def test_add_to_order_invalid_id(rs):
    with pytest.raises(ValueError):
        rs.add_to_order([], 999, 1)


@pytest.mark.parametrize("qty", [0, -1])
def test_add_to_order_invalid_qty(rs, qty):
    with pytest.raises(ValueError):
        rs.add_to_order([], 1, qty)


def test_compute_bill(rs):
    order = []
    rs.add_to_order(order, 1, 2)  # 90.00
    rs.add_to_order(order, 5, 2)  # 30.00
    subtotal, tax, total = rs.compute_bill(order)
    assert subtotal == Decimal("120.00")
    assert tax == Decimal("16.80")
    assert total == Decimal("136.80")


def test_compute_bill_empty_order(rs):
    assert rs.compute_bill([]) == (Decimal("0.00"), Decimal("0.00"), Decimal("0.00"))


def test_tax_rounding_half_up():
    rs = RestaurantSystem(tax_rate=Decimal("0.14"))
    item = rs.add_menu_item("Test", Decimal("0.25"))  # tax = 0.035 -> 0.04
    _, tax, _ = rs.compute_bill([OrderLine(item, 1)])
    assert tax == Decimal("0.04")


def test_add_and_remove_menu_item(rs):
    item = rs.add_menu_item("Salad", Decimal("30"))
    assert item.id == 6
    assert rs.remove_menu_item(6).name == "Salad"
    assert 6 not in rs.menu


def test_new_id_never_reuses_after_removing_middle(rs):
    rs.remove_menu_item(2)
    assert rs.add_menu_item("Salad", Decimal("30")).id == 6


@pytest.mark.parametrize("name,price", [("", Decimal("10")), ("X", Decimal("0")), ("X", Decimal("-5"))])
def test_add_menu_item_validation(rs, name, price):
    with pytest.raises(ValueError):
        rs.add_menu_item(name, price)


def test_receipt_contains_totals(rs):
    order = []
    rs.add_to_order(order, 1, 1)
    receipt = rs.format_receipt(order)
    assert "Tax (14%)" in receipt
    assert "TOTAL: 51.30 EGP" in receipt
