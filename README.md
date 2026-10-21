# 🍽️ Restaurant System (CLI)

A simple, dependency-free command-line restaurant ordering system written in Python. Browse a menu, place orders, and get an itemized receipt with VAT calculated automatically.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

## Features

- View the menu with prices (EGP)
- Place an order with multiple items and quantities
- Automatic merging of repeated items into a single order line
- Input validation (non-numeric input, invalid item IDs, zero/negative quantities)
- Itemized receipt with subtotal, VAT (14%), and total
- Add / remove menu items from the CLI
- Exact currency arithmetic using `Decimal` (no float rounding errors)
- Unit tests with `pytest`

## Demo

```text
====== Restaurant System ======
1) View Menu
2) New Order
3) Manage Menu
4) Exit
Choose: 2

=== Place your order ===

--- MENU ---
1. Chicken Burger       45.00 EGP
2. Pizza Margherita     70.00 EGP
3. Pasta Alfredo        65.00 EGP
4. French Fries         25.00 EGP
5. Cola                 15.00 EGP
-------------
Enter item id (or 0 to finish): 1
Enter quantity for Chicken Burger: 2
Added!
Enter item id (or 0 to finish): 5
Enter quantity for Cola: 2
Added!
Enter item id (or 0 to finish): 0

===== RECEIPT =====
Chicken Burger       x2   = 90.00 EGP
Cola                 x2   = 30.00 EGP
--------------------
Subtotal: 120.00 EGP
Tax (14%): 16.80 EGP
TOTAL: 136.80 EGP
====================
```

## Getting Started

### Requirements

- Python 3.8 or newer (standard library only, no `pip install` needed)

### Run

```bash
git clone https://github.com/<your-username>/restaurant-system.git
cd restaurant-system
python main.py
```

## Project Structure

```text
restaurant-system/
├── main.py                  # Application code
├── conftest.py              # Lets pytest import main.py
├── tests/
│   └── test_restaurant.py   # Unit tests
├── README.md
├── LICENSE
└── .gitignore
```

## How It Works

| Component          | Responsibility                                              |
| ------------------ | ----------------------------------------------------------- |
| `MenuItem`         | Dataclass holding an item's id, name, and price             |
| `OrderLine`        | Dataclass for an item + quantity, with a computed `total`   |
| `RestaurantSystem` | Menu management, order handling, billing, receipt, CLI loop |

## Running the Tests

```bash
pip install pytest
pytest
```

## Customization

- **Menu:** edit the `self.menu` dictionary in `RestaurantSystem.__init__`.
- **Tax rate:** change `self.tax_rate` (default `0.14`).

## Roadmap

- [x] Add / remove menu items from the CLI
- [x] Use `Decimal` for exact currency arithmetic
- [x] Unit tests with `pytest`
- [ ] Edit existing menu items
- [ ] Save menu and order history to JSON
- [ ] Discounts and tipping

## Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License

Distributed under the MIT License. See `LICENSE` for details.

## Author

**Mostafa** — Computer Science student (AI/ML & Cybersecurity)
GitHub: [@Mostafa112-alt](https://github.com/Mostafa112-alt)
