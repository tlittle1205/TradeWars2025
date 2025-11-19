# ship.py
# =====================================================
# Ship class for player ships
# =====================================================

from dataclasses import dataclass, field

COMMODITIES = ["ore", "organics", "equipment"]


@dataclass
class Ship:
    """
    Represents the player's ship.
    """
    name: str = "GodSpeed II"
    max_hull: int = 100
    hull: int = 100
    attack: int = 10
    defense: int = 5

    # NEW — unified shield system
    shields: int = 10

    max_holds: int = 30
    credits: int = 1000
    fuel: int = 300
    location: int = 1

    cargo: dict = field(default_factory=lambda: {c: 0 for c in COMMODITIES})

    # -------------------------------------------------
    # Properties
    # -------------------------------------------------
    @property
    def used_holds(self) -> int:
        return sum(self.cargo.values())

    @property
    def free_holds(self) -> int:
        return self.max_holds - self.used_holds

    @property
    def is_destroyed(self) -> bool:
        return self.hull <= 0

    # -------------------------------------------------
    # Cargo
    # -------------------------------------------------
    def add_cargo(self, commodity: str, amount: int) -> None:
        if commodity not in self.cargo:
            raise ValueError(f"Unknown commodity: {commodity}")
        if amount < 0:
            raise ValueError("Cannot add negative cargo.")
        if self.free_holds < amount:
            raise ValueError("Not enough cargo space.")
        self.cargo[commodity] += amount

    def remove_cargo(self, commodity: str, amount: int) -> None:
        if commodity not in self.cargo:
            raise ValueError(f"Unknown commodity: {commodity}")
        if amount < 0:
            raise ValueError("Cannot remove negative cargo.")
        if self.cargo[commodity] < amount:
            raise ValueError("Not enough cargo to remove.")
        self.cargo[commodity] -= amount

    def clear_all_cargo(self) -> None:
        for c in self.cargo:
            self.cargo[c] = 0

    # -------------------------------------------------
    # Hull / Combat
    # -------------------------------------------------
    def repair(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Repair amount must be positive.")
        self.hull = min(self.max_hull, self.hull + amount)

    def take_damage(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Damage must be positive.")
        self.hull -= amount

    # -------------------------------------------------
    # Credits
    # -------------------------------------------------
    def spend_credits(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot spend negative credits.")
        if self.credits < amount:
            raise ValueError("Not enough credits.")
        self.credits -= amount

    def add_credits(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot add negative credits.")
        self.credits += amount

    # -------------------------------------------------
    # Fuel
    # -------------------------------------------------
    def use_fuel(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot use negative fuel.")
        if self.fuel < amount:
            raise ValueError("Not enough fuel.")
        self.fuel -= amount

    def refuel(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot refuel negative amount.")
        self.fuel += amount

    # -------------------------------------------------
    # Status
    # -------------------------------------------------
    def cargo_summary(self) -> str:
        lines = [f"Cargo Manifest ({self.used_holds}/{self.max_holds} holds used):"]
        for c, amt in self.cargo.items():
            lines.append(f"  {c.capitalize():<10}: {amt}")
        return "\n".join(lines)

    def status_summary(self) -> str:
        return (
            f"Ship: {self.name}\n"
            f"Hull: {self.hull}/{self.max_hull}\n"
            f"Attack/Defense: {self.attack}/{self.defense}\n"
            f"Shields: {self.shields}\n"                 # NEW LINE
            f"Fuel: {self.fuel}\n"
            f"Credits: {self.credits}\n"
            f"Cargo: {self.used_holds}/{self.max_holds} holds used\n"
            f"Location: Sector {self.location}"
        )

    # -------------------------------------------------
    # Save/Load
    # -------------------------------------------------
    def to_dict(self):
        return {
            "hull": self.hull,
            "max_hull": self.max_hull,
            "attack": self.attack,
            "defense": self.defense,
            "shields": self.shields,            # NEW
            "fuel": self.fuel,
            "max_holds": self.max_holds,
            "credits": self.credits,
            "cargo": self.cargo,
            "location": self.location,
        }

    @staticmethod
    def from_dict(data):
        ship = Ship()
        ship.hull = data["hull"]
        ship.max_hull = data["max_hull"]
        ship.attack = data["attack"]
        ship.defense = data["defense"]
        ship.shields = data.get("shields", 10)  # NEW (fallback for old saves)
        ship.fuel = data["fuel"]
        ship.max_holds = data["max_holds"]
        ship.credits = data["credits"]
        ship.cargo = data["cargo"]
        ship.location = data["location"]
        return ship
