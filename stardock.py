# stardock.py
# ============================================================
# STARDOCK — "THE CELESTIAL BAZAAR"
# ============================================================

import random

from descriptions import depart
# ============================================================
# LOCAL INPUT WRAPPER (avoids circular import with tw25)
# ============================================================

def sd_input(prompt="> "):
    """Stardock-safe input that supports CLS/CLEAR."""
    from tw25 import intercept_clear   # safe 1-way dependency
    while True:
        cmd = input(prompt).strip()
        if intercept_clear(cmd.lower()):
            continue
        return cmd


class StarDock:
    def __init__(self, ship, galaxy):
        self.ship = ship
        self.galaxy = galaxy

    # ------------------------------------------------------------
    # Entry Point
    # ------------------------------------------------------------
    def enter(self):
        self._print_banner()

        while True:
            print("\n=== THE CELESTIAL BAZAAR — MAIN CONCOURSE ===")
            print("Neon rains down across chrome walkways as merchants,")
            print("augmented courtesans, corporate agents, and bounty")
            print("hunters weave through the chaos.\n")

            print("1. Corporate Concourse (Luxury Upgrades)")
            print("2. Interstellar Bank (Citadel Vaults)")
            print("3. The Rusty Nebula (Seedy Cantina)")
            print("4. Market Promenade (Shops & Exotic Goods)")
            print("5. Tech Lab (Experimental Mods)")
            print("0. Return to Space")

            cmd = sd_input("\nChoose destination: ")

            if cmd == "1":
                self.corporate_concourse()
            elif cmd == "2":
                self.bank()
            elif cmd == "3":
                self.rusty_nebula()
            elif cmd == "4":
                self.market()
            elif cmd == "5":
                self.tech_lab()
            elif cmd == "0":
                print(depart())
                #print("\nYou step back onto your ship as the airlock seals behind you...")
                return

    # ------------------------------------------------------------
    # Atmosphere
    # ------------------------------------------------------------
    def _print_banner(self):
        print("\n")
        print("███  STARDOCK // CELESTIAL BAZAAR  ███")
        print("A shimmering hive of decadence, danger, and deals.\n")

    # ------------------------------------------------------------
    # Corporate Concourse — Luxury Section
    # ------------------------------------------------------------
    def corporate_concourse(self):
        print("\n--- CORPORATE CONCOURSE ---")
        print("White marble floors. Corporate reps. Smug security.")
        print("Everything here is overpriced.\n")

        while True:
            print("1. Repair Hull")
            print("2. Upgrade Shields")
            print("3. Expand Cargo Hold")
            print("4. Purchase Star Charts")
            print("0. Return")

            cmd = sd_input("Select: ")

            # Repair Hull
            if cmd == "1":
                cost = 150
                healed = 10

                if self.ship.credits < cost:
                    print("You cannot afford repairs.")
                    continue

                self.ship.spend_credits(cost)
                self.ship.hull = min(self.ship.max_hull, self.ship.hull + healed)
                print(f"Hull repaired by {healed} points.")

            # Upgrade Shields
            elif cmd == "2":
                cost = 500
                boost = 5

                if self.ship.credits < cost:
                    print("You cannot afford shield upgrades.")
                    continue

                self.ship.spend_credits(cost)
                self.ship.shields += boost          # <-- FIXED
                print(f"Shield capacity upgraded by {boost}.")


            # Expand Cargo Hold
            elif cmd == "3":
                cost = 5000
                print(f"Expanding cargo hold by +5 units costs {cost} credits.")
                confirm = sd_input("Proceed? (y/n) ")

                if confirm.startswith("y"):
                    if self.ship.credits < cost:
                        print("You cannot afford this upgrade.")
                        continue

                    self.ship.spend_credits(cost)
                    self.ship.max_holds += 5        # <-- ONLY THIS
                    print(f"Cargo capacity expanded! New capacity: {self.ship.max_holds}")

                else:
                    print("Upgrade cancelled.")


            # Star Charts
            elif cmd == "4":
                print("Corporate AI injects updated star charts into nav system.")

            elif cmd == "0":
                return

    # ------------------------------------------------------------
    # Bank — Citadel Vaults
    # ------------------------------------------------------------
    def bank(self):
        print("\n--- INTERSTELLAR BANK ---")
        print("Polished floors. Robotic tellers. Soft corporate music.\n")

        while True:
            print("1. Deposit Credits")
            print("2. Withdraw Credits")
            print("3. Check Interest Rate")
            print("0. Return")

            cmd = sd_input("Select: ")

            if cmd == "1":
                amt = int(sd_input("Amount to deposit: "))
                if amt > self.ship.credits:
                    print("You do not have that many credits.")
                    continue
                self.ship.spend_credits(amt)
                self.ship.bank_balance += amt
                print("Deposited.")

            elif cmd == "2":
                amt = int(sd_input("Withdraw how much: "))
                if amt > self.ship.bank_balance:
                    print("Insufficient funds.")
                    continue
                self.ship.bank_balance -= amt
                self.ship.credits += amt
                print("Withdrawn.")

            elif cmd == "3":
                print(f"Bank balance: {self.ship.bank_balance} credits")
                print("Interest accrues automatically each game day (0.5%).")

            elif cmd == "0":
                return

    # ------------------------------------------------------------
    # Rusty Nebula — Seedy Cantina
    # ------------------------------------------------------------
    def rusty_nebula(self):
        print("\n--- THE RUSTY NEBULA ---")
        print("A smoky bar full of mercs, scammers, dancers, and hustlers.\n")

        while True:
            print("1. Hear Rumors")
            print("2. Gamble")
            print("3. Hire Mercenaries (Coming Soon)")
            print("4. Black Market Upgrades (Coming Soon)")
            print("0. Return")

            cmd = sd_input("Select: ")

            if cmd == "1":
                self._random_rumor()
            elif cmd == "2":
                self._gambling_den()
            elif cmd == "3":
                print("Mercenaries unavailable — union strike.")
            elif cmd == "4":
                print("Black market closed after a shootout.")
            elif cmd == "0":
                return

    def _random_rumor(self):
        rumors = [
            "A rogue AI ship was spotted near sector 12.",
            "Hidden wormhole detected near sector 17.",
            "Corporate transport vanished near the rim — pirates suspected.",
            "A planet producing rare organics at insane rates has been found.",
            "A dancer whispers: 'Some sectors aren’t what they seem…'"
        ]
        print("\nA stranger leans close and mutters:")
        print("  \"" + random.choice(rumors) + "\"\n")

    def _gambling_den(self):
        print("\nYou sit at a neon-lit gambling table.")
        bet = int(sd_input("Place your bet: "))

        if bet > self.ship.credits:
            print("You can't bet more credits than you have.")
            return

        self.ship.spend_credits(bet)
        roll = random.randint(1, 100)

        if roll > 50:
            winnings = bet * 2
            self.ship.credits += winnings
            print(f"You win! Payout: {winnings} credits.")
        else:
            print("You lose.")

    # ------------------------------------------------------------
    # Market Promenade
    # ------------------------------------------------------------
    def market(self):
        print("\n--- MARKET PROMENADE ---")
        print("Holographic storefronts. Alien fragrances. Shady vendors.\n")

        while True:
            print("1. Buy Vanity Items")
            print("2. Browse Exotic Wares")
            print("0. Return")

            cmd = sd_input("Select: ")

            if cmd == "1":
                print("A clerk offers a gold-trimmed hull paintjob.")
            elif cmd == "2":
                item = random.choice(["Glitter Spice", "Xeno Wine", "Star Silk", "Void Perfume"])
                price = random.randint(100, 500)
                print(f"Exotic item: {item} — {price} credits")
            elif cmd == "0":
                return

    # ------------------------------------------------------------
    # Tech Lab
    # ------------------------------------------------------------
    def tech_lab(self):
        print("\n--- SCIENCE & TECH LAB ---")
        print("Sparks fly as engineers argue over unstable prototypes.\n")

        while True:
            print("1. Buy Experimental Weapons")
            print("2. Install Minor Shield Capacitor Upgrade")
            print("3. Commission Prototype Tech (Random Effect)")
            print("0. Return")

            cmd = sd_input("Select: ")

            if cmd == "1":
                cost = 600
                if self.ship.credits < cost:
                    print("Insufficient credits.")
                    continue
                self.ship.spend_credits(cost)
                print("You acquire a questionable plasma destabilizer.")

            elif cmd == "2":
                cost = 350
                if self.ship.credits < cost:
                    print("Insufficient credits.")
                    continue
                self.ship.spend_credits(cost)
                #self.ship.shield_strength += 2 #This was crashing the game.
                self.ship.shields += 2
                print("Shield capacitor installed (+2 shields).")

            elif cmd == "3":
                cost = 400
                if self.ship.credits < cost:
                    print("Insufficient credits.")
                    continue
                self.ship.spend_credits(cost)
                effect = random.choice([
                    "hull reinforced (+5 hull)",
                    "sensor boost (+1 range — cosmetic)",
                    "ship AI optimized (no visible effect)",
                    "reactor surge (+1 shield)"
                ])
                print(f"Prototype tech installed: {effect}")

            elif cmd == "0":
                return
