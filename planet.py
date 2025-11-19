# planet.py
# ============================================================
# Planet object for TW2025
#
# Supports:
#   - Goods storage (ore, organics, equipment)
#   - Credit treasury
#   - Production over time
#   - Save/load (to_dict / from_dict)
# ============================================================

from dataclasses import dataclass, field
from port import COMMODITIES
import random


def generate_planet_name():
    prefixes = ["New", "Alpha", "Beta", "Gamma", "Delta", "Nova", "Terra", "Fort", "Sigma"]
    suffixes = ["Prime", "Station", "Base", "Haven", "One", "II", "Harbor", "Reach"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"


@dataclass
class Planet:
    """
    Represents a planet that the player can land on.
    Planets can store goods and credits, and produce goods each turn.
    """

    sector_id: int
    name: str = field(default_factory=generate_planet_name)

    # Inventory is called GOODS (not inventory)
    goods: dict = field(default_factory=lambda: {
        "ore": 0,
        "organics": 0,
        "equipment": 0
    })

    # Planet treasury
    treasury: int = 0

    # Production rates for each commodity per tick (game turn)
    production_rates: dict = field(default_factory=lambda: {
        "ore": 1,
        "organics": 1,
        "equipment": 1
    })

    # -------------------------------------------------------
    # Production tick — planets slowly generate resources
    # -------------------------------------------------------
    def production_tick(self):
        for c in COMMODITIES:
            self.goods[c] += self.production_rates.get(c, 0)

    # -------------------------------------------------------
    # Depositing / Withdrawing goods
    # -------------------------------------------------------
    def deposit_commodity(self, commodity, amount):
        if commodity not in COMMODITIES:
            raise ValueError("Unknown commodity.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.goods[commodity] += amount

    def withdraw_commodity(self, commodity, amount):
        if commodity not in COMMODITIES:
            raise ValueError("Unknown commodity.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if self.goods[commodity] < amount:
            raise ValueError("Planet does not have that much.")
        self.goods[commodity] -= amount

    # -------------------------------------------------------
    # Planet credit treasury
    # -------------------------------------------------------
    def deposit_credits(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.treasury += amount

    def withdraw_credits(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if self.treasury < amount:
            raise ValueError("Treasury does not contain that much.")
        self.treasury -= amount

    # -------------------------------------------------------
    # Pretty summary
    # -------------------------------------------------------
    def planet_summary(self):
        text = [f"=== Planet {self.name} (Sector {self.sector_id}) ==="]
        text.append("Goods Stored:")
        for c in COMMODITIES:
            text.append(f"  {c.capitalize()}: {self.goods[c]}")
        text.append(f"Treasury: {self.treasury} credits")
        return "\n".join(text)

    # -------------------------------------------------------
    # SAVE / LOAD SUPPORT
    # -------------------------------------------------------
    def to_dict(self):
        return {
            "name": self.name,
            "sector_id": self.sector_id,
            "goods": self.goods,
            "treasury": self.treasury,
            "production_rates": self.production_rates,
        }

    @staticmethod
    def from_dict(data):
        p = Planet(sector_id=data["sector_id"])
        p.name = data["name"]
        p.goods = data["goods"]
        p.treasury = data["treasury"]
        p.production_rates = data.get("production_rates", {
            "ore": 1,
            "organics": 1,
            "equipment": 1
        })
        return p
