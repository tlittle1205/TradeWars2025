# port.py
# ============================================================
# TW-style Port:
#   - Three commodities: ore, organics, equipment
#   - Port types determine buy/sell behavior:
#         Type 1 → BSS
#         Type 2 → SBS
#         Type 3 → SSB
#   - Dynamic prices based on supply levels
#   - Terminal-friendly summaries
#   - Auto-generated port names for galaxy creation
# ============================================================

from dataclasses import dataclass, field
import random

COMMODITIES = ["ore", "organics", "equipment"]

# Base prices used for dynamic pricing
BASE_PRICES = {
    "ore": 40,
    "organics": 30,
    "equipment": 80,
}

# Port classifications
PORT_TYPES = {
    1: {"ore": "buy",  "organics": "sell", "equipment": "sell"},  # BSS
    2: {"ore": "sell", "organics": "buy",  "equipment": "sell"},  # SBS
    3: {"ore": "sell", "organics": "sell", "equipment": "buy"},   # SSB
}

# ------------------------------------------------------------
# Random TW-style Port Name Generator
# ------------------------------------------------------------

PORT_PREFIXES = [
    "Rigel", "Sigma", "Omega", "Alpha", "Beta", "Tau",
    "Nova", "Epsilon", "Orion", "Kappa", "Gamma"
]

PORT_SUFFIXES = [
    "Tradeport", "Station", "Depot", "Exchange",
    "Market", "Outpost", "Harbor"
]

def random_port_name():
    return f"{random.choice(PORT_PREFIXES)} {random.choice(PORT_SUFFIXES)}"


@dataclass
class Port:
    """
    TradeWars-style port object.
    Automatically chooses:
    - name (if not provided)
    - port class (type_id)
    """

    name: str = None
    type_id: int = None

    commodity_levels: dict = field(default_factory=lambda: {
        c: random.randint(20, 80) for c in COMMODITIES
    })

    prices: dict = field(default_factory=dict)

    def __post_init__(self):
        # Auto-generate name if none provided
        if self.name is None:
            self.name = random_port_name()

        # Auto-assign port behavior class if none provided
        if self.type_id is None:
            self.type_id = random.choice(list(PORT_TYPES.keys()))

        self.modes = PORT_TYPES[self.type_id]
        self.update_prices()

    # ------------------------------------------------------------
    # Port Class Code (BSS/SBS/SSB)
    # ------------------------------------------------------------
    def class_code(self) -> str:
        return "".join("B" if self.modes[c] == "buy" else "S" for c in COMMODITIES)

    # ------------------------------------------------------------
    # Pricing Logic
    # ------------------------------------------------------------
    def update_prices(self) -> None:
        for c in COMMODITIES:
            base = BASE_PRICES[c]
            level = self.commodity_levels[c]

            if self.modes[c] == "sell":
                factor = 0.6 + (100 - level) / 150.0
            else:
                factor = 1.0 + level / 150.0

            self.prices[c] = max(5, int(base * factor))

    # ------------------------------------------------------------
    # Trade Operations
    # ------------------------------------------------------------
    def can_sell_to_player(self, commodity):
        return self.modes.get(commodity) == "sell"

    def can_buy_from_player(self, commodity):
        return self.modes.get(commodity) == "buy"

    def buy_from_port(self, ship, commodity, amount):
        if not self.can_sell_to_player(commodity):
            raise ValueError(f"{self.name} does not sell {commodity}.")

        price = self.prices[commodity]
        total_cost = price * amount

        ship.spend_credits(total_cost)
        ship.add_cargo(commodity, amount)

        self.commodity_levels[commodity] = max(
            0, self.commodity_levels[commodity] - amount // 2
        )
        self.update_prices()

    def sell_to_port(self, ship, commodity, amount):
        if not self.can_buy_from_player(commodity):
            raise ValueError(f"{self.name} is not buying {commodity}.")

        price = self.prices[commodity]
        total_gain = price * amount

        ship.remove_cargo(commodity, amount)
        ship.add_credits(total_gain)

        self.commodity_levels[commodity] = min(
            100, self.commodity_levels[commodity] + amount // 2
        )
        self.update_prices()

    # ------------------------------------------------------------
    # Full Quicksell
    # ------------------------------------------------------------
    def quicksell(self, ship) -> int:
        total_credits = 0
        sold_any = False

        for commodity, qty in ship.cargo.items():
            if qty > 0 and self.can_buy_from_player(commodity):
                price = self.prices[commodity]
                gain = qty * price
                total_credits += gain

                ship.remove_cargo(commodity, qty)
                self.commodity_levels[commodity] = min(
                    100, self.commodity_levels[commodity] + qty // 2
                )
                sold_any = True

        if sold_any:
            ship.add_credits(total_credits)
            self.update_prices()

        return total_credits

    # ------------------------------------------------------------
    # BUY MAX
    # ------------------------------------------------------------
    def buy_max(self, ship, commodity):
        if not self.can_sell_to_player(commodity):
            raise ValueError(f"{self.name} does not sell {commodity}.")

        price = self.prices[commodity]
        amount = min(ship.credits // price, ship.free_holds)

        if amount <= 0:
            return 0

        self.buy_from_port(ship, commodity, amount)
        return amount

    # ------------------------------------------------------------
    # Summary Display
    # ------------------------------------------------------------
    def port_summary(self):
        lines = [
            f"Port: {self.name}",
            f"Class: {self.class_code()}",
            "Commodity    Mode      Level   Price",
            "----------------------------------------",
        ]
        for c in COMMODITIES:
            mode = "Buys " if self.can_buy_from_player(c) else "Sells"
            level = self.commodity_levels[c]
            price = self.prices[c]
            lines.append(f"{c.capitalize():<12}{mode:<8}{level:>5}%   {price:>6}")

        return "\n".join(lines)

    # ------------------------------------------------------------
    # Save/Load
    # ------------------------------------------------------------
    def to_dict(self):
        return {
            "name": self.name,
            "type_id": self.type_id,
            "commodity_levels": self.commodity_levels,
            "prices": self.prices,
        }

    @staticmethod
    def from_dict(data):
        port = Port(
            name=data["name"],
            type_id=data.get("type_id")
        )
        port.commodity_levels = data["commodity_levels"]
        port.prices = data["prices"]
        port.modes = PORT_TYPES[port.type_id]
        return port
