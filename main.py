"""Restaurant System (CLI).

Features: view/manage menu, place orders, itemized receipt with VAT.
Run: python main.py
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Dict, List, Optional

CENT = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    """Round to 2 decimal places (half up) for currency."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass
class MenuItem:
    id: int
    name: str
    price: Decimal


@dataclass
class OrderLine:
    item: MenuItem
    qty: int

    @property
    def total(self) -> Decimal:
        return self.item.price * self.qty


class RestaurantSystem:
    def __init__(self, tax_rate: Decimal = Decimal("0.14")):
        self.tax_rate = tax_rate  # 14% VAT by default
        self.menu: Dict[int, MenuItem] = {}
        for name, price in [
            ("Chicken Burger", "45.00"),
            ("Pizza Margherita", "70.00"),
            ("Pasta Alfredo", "65.00"),
            ("French Fries", "25.00"),
            ("Cola", "15.00"),
        ]:
            self.add_menu_item(name, Decimal(price))

    # ---------- menu management ----------
    def add_menu_item(self, name: str, price: Decimal) -> MenuItem:
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
        new_id = max(self.menu, default=0) + 1
        item = MenuItem(new_id, name, money(price))
        self.menu[new_id] = item
        return item

    def remove_menu_item(self, item_id: int) -> MenuItem:
        if item_id not in self.menu:
            raise ValueError("Invalid item id.")
        return self.menu.pop(item_id)

    def show_menu(self) -> None:
        print("\n--- MENU ---")
        if not self.menu:
            print("(empty)")
        for item in sorted(self.menu.values(), key=lambda x: x.id):
            print(f"{item.id}. {item.name:20} {item.price:.2f} EGP")
        print("-------------")

    # ---------- orders ----------
    def add_to_order(self, order: List[OrderLine], item_id: int, qty: int) -> None:
        if item_id not in self.menu:
            raise ValueError("Invalid item id.")
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0.")

        # merge quantities if the item is already in the order
        for line in order:
            if line.item.id == item_id:
                line.qty += qty
                return
        order.append(OrderLine(item=self.menu[item_id], qty=qty))

    def compute_bill(self, order: List[OrderLine]):
        subtotal = money(sum((line.total for line in order), Decimal("0")))
        tax = money(subtotal * self.tax_rate)
        return subtotal, tax, subtotal + tax

    def format_receipt(self, order: List[OrderLine]) -> str:
        subtotal, tax, total = self.compute_bill(order)
        lines = ["===== RECEIPT ====="]
        for line in order:
            lines.append(f"{line.item.name:20} x{line.qty:<3} = {line.total:.2f} EGP")
        lines += [
            "--------------------",
            f"Subtotal: {subtotal:.2f} EGP",
            f"Tax ({self.tax_rate:.0%}): {tax:.2f} EGP",
            f"TOTAL: {total:.2f} EGP",
            "====================",
        ]
        return "\n".join(lines)

    # ---------- CLI ----------
    @staticmethod
    def _read_int(prompt: str) -> Optional[int]:
        try:
            return int(input(prompt).strip())
        except ValueError:
            return None

    def take_order(self) -> None:
        order: List[OrderLine] = []
        print("\n=== Place your order ===")
        self.show_menu()
        print("Type 0 to finish ordering.\n")

        while True:
            item_id = self._read_int("Enter item id (or 0 to finish): ")
            if item_id is None:
                print("Please enter a number.")
                continue
            if item_id == 0:
                break
            if item_id not in self.menu:
                print("Invalid item id. Try again.")
                continue

            qty = self._read_int(f"Enter quantity for {self.menu[item_id].name}: ")
            if qty is None or qty <= 0:
                print("Quantity must be a whole number greater than 0.")
                continue

            self.add_to_order(order, item_id, qty)
            print("Added!")

        if not order:
            print("\nNo items ordered.")
            return
        print("\n" + self.format_receipt(order) + "\n")

    def manage_menu(self) -> None:
        while True:
            print("\n--- Manage Menu ---")
            print("1) Add item")
            print("2) Remove item")
            print("3) Back")
            choice = input("Choose: ").strip()

            if choice == "1":
                name = input("Item name: ")
                try:
                    price = Decimal(input("Price (EGP): ").strip())
                    item = self.add_menu_item(name, price)
                    print(f"Added: {item.id}. {item.name} - {item.price:.2f} EGP")
                except (InvalidOperation, ValueError) as exc:
                    print(f"Could not add item: {exc if isinstance(exc, ValueError) else 'invalid price'}")
            elif choice == "2":
                self.show_menu()
                item_id = self._read_int("Item id to remove: ")
                try:
                    if item_id is None:
                        raise ValueError("Please enter a number.")
                    print(f"Removed: {self.remove_menu_item(item_id).name}")
                except ValueError as exc:
                    print(f"Could not remove item: {exc}")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please choose 1-3.")

    def run(self) -> None:
        while True:
            print("\n====== Restaurant System ======")
            print("1) View Menu")
            print("2) New Order")
            print("3) Manage Menu")
            print("4) Exit")
            choice = input("Choose: ").strip()

            if choice == "1":
                self.show_menu()
            elif choice == "2":
                self.take_order()
            elif choice == "3":
                self.manage_menu()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please choose 1-4.")


if __name__ == "__main__":
    RestaurantSystem().run()
