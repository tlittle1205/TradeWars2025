# combat.py
# ===============================================================
# Combat System + Pirate AI
#
# This module provides:
#   - PirateShip class (lightweight NPC ship)
#   - CombatEngine class (handles fights between player + pirates)
#   - Damage calculation
#   - Escape attempts
#   - Loot drops
#
# This is the foundation. Later we can expand:
#   - Fighter duels
#   - Shields
#   - Multiple pirates
#   - Planetary defense
#   - TW-style ambushes
# ===============================================================

import random
from dataclasses import dataclass
from ship import Ship


# ---------------------------------------------------------------
# Pirate Ship (simple NPC opponent)
# ---------------------------------------------------------------

@dataclass
class PirateShip:
    """
    Simple NPC pirate ship.
    More complex AI can be added later.
    """
    name: str = "Space Pirate"
    hull: int = 50
    max_hull: int = 50
    attack: int = 8
    defense: int = 4
    bounty: int = 200

    @property
    def is_destroyed(self):
        return self.hull <= 0

    def take_damage(self, dmg: int):
        self.hull -= dmg


# ---------------------------------------------------------------
# Combat Engine
# ---------------------------------------------------------------

class CombatEngine:
    """
    Handles encounters between the player's ship and pirates.
    """

    def __init__(self, player: Ship):
        self.player = player

    # -----------------------------------------------------------
    # Random Pirate Generator
    # -----------------------------------------------------------

    def spawn_pirate(self) -> PirateShip:
        """
        Pirates scale slightly with the player's ship stats.
        """
        bonus = random.randint(0, self.player.attack // 2)

        return PirateShip(
            hull=40 + bonus,
            max_hull=40 + bonus,
            attack=6 + bonus,
            defense=3 + bonus,
            bounty=150 + bonus * 10,
        )

    # -----------------------------------------------------------
    # Combat Resolution
    # -----------------------------------------------------------

    def attack_roll(self, atk: int, defense: int) -> int:
        """
        Basic attack roll:
          damage = (atk + random bonus) - defense
        """
        roll = random.randint(0, atk)
        dmg = max(1, roll - defense)
        return dmg

    def take_turn(self, pirate: PirateShip):
        """
        One exchange of attacks between player and pirate.
        Returns a tuple: (player_damage, pirate_damage)
        """
        # player attacks pirate
        player_dmg = self.attack_roll(self.player.attack, pirate.defense)
        pirate.take_damage(player_dmg)

        # pirate attacks player (if still alive)
        if not pirate.is_destroyed:
            pirate_dmg = self.attack_roll(pirate.attack, self.player.defense)
            self.player.take_damage(pirate_dmg)
        else:
            pirate_dmg = 0

        return player_dmg, pirate_dmg

    # -----------------------------------------------------------
    # Escape Attempt
    # -----------------------------------------------------------

    def attempt_escape(self) -> bool:
        """
        Escape chance:
          Base 40% + 1% per free cargo hold
        """
        bonus = self.player.free_holds
        chance = 40 + bonus

        roll = random.randint(1, 100)
        return roll <= chance

    # -----------------------------------------------------------
    # Combat Loop
    # -----------------------------------------------------------

    def engage(self):
        """
        Run full combat until:
          - Pirate destroyed
          - Player destroyed
          - Player escapes
        Returns dict describing outcome.
        """

        pirate = self.spawn_pirate()
        log = []

        log.append(f"A {pirate.name} appears! Hull: {pirate.hull}")

        while True:
            # offer escape chance if the system wants
            if random.random() < 0.15:
                log.append("The pirate hesitates — opportunity to escape!")
                if self.attempt_escape():
                    log.append("You escape successfully!")
                    return {"result": "escaped", "log": log}
                else:
                    log.append("Escape failed!")

            # exchange attacks
            p_dmg, s_dmg = self.take_turn(pirate)
            log.append(f"You deal {p_dmg} damage. Pirate hull: {max(0, pirate.hull)}")

            if pirate.is_destroyed:
                log.append("You destroyed the pirate!")
                self.player.add_credits(pirate.bounty)
                log.append(f"You gain {pirate.bounty} credits.")
                return {"result": "win", "log": log}

            log.append(f"The pirate hits you for {s_dmg}. Hull: {max(0, self.player.hull)}")

            if self.player.is_destroyed:
                log.append("Your ship is destroyed!")
                return {"result": "death", "log": log}
