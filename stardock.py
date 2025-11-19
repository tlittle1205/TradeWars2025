# stardock.py
# ============================================================
# STARDOCK — "THE CELESTIAL BAZAAR"
#
# Tone:
# - Mos Eisley (chaotic scum hub)
# - Blade Runner (neon, rain, cyberpunk gutters)
# - Hedonistic Paradise (pleasure dens, indulgence)
# - Rodeo Drive (luxury boutiques, elite fashion)
#
# The heart of civilization, crime, decadence, and commerce.
# ============================================================

import random


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

            cmd = input("\nChoose destination: ").strip()

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
                print("\nYou step back onto your ship as the airlock seals behind you...")
                return

    # ------------------------------------------------------------
    # Atmosphere
    # ------------------------------------------------------------
    def _print_banner(self):
        print("\n")
        print("███  STARDOCK // CELESTIAL BAZAAR  ███")
        print("A shimmering hive of decadence, danger, and deals.\n")

    # ------------------------------------------------------------
    # Corporate Concourse — Luxury & Legitimacy
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

            cmd = input("Select: ").strip()

            if cmd == "1":
                cost = 150
                healed = 10
                self.ship.spend_credits(cost)
                self.ship.hull = min(self.ship.max_hull, self.ship.hull + healed)
                print(f"Hull repaired by {healed} points.")

            elif cmd == "2":
                cost = 500
                boost = 5
                self.ship.spend_credits(cost)
                self.ship.shields += boost
                print(f"Shield capacity upgraded by {boost}.")

            elif cmd == "3":
                cost = 300
                self.ship.spend_credits(cost)
                self.ship.cargo_holds += 5
                print("Cargo bay expanded by 5 units.")

            elif cmd == "4":
                print("The corporate AI injects updated star charts into your nav system.")

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

            cmd = input("Select: ").strip()

            if cmd == "1":
                amt = int(input("Amount to deposit: "))
                self.ship.spend_credits(amt)
                self.ship.bank_balance += amt
                print("Deposited.")

            elif cmd == "2":
                amt = int(input("Withdraw how much: "))
                if amt > self.ship.bank_balance:
                    print("Insufficient funds.")
                else:
                    self.ship.bank_balance -= amt
                    self.ship.credits += amt
                    print("Withdrawn.")

            elif cmd == "3":
                print(f"Bank balance: {self.ship.bank_balance} credits")
                print("Interest accrues automatically each in-game day (0.5%).")

            elif cmd == "0":
                return

    # ------------------------------------------------------------
    # Rusty Nebula — Seedy Cantina
    # ------------------------------------------------------------
    def rusty_nebula(self):
        print("\n--- THE RUSTY NEBULA ---")
        print("A smoky bar full of mercs, scammers, augmented dancers,")
        print("and black-market hustlers. A place where bad decisions")
        print("are made enthusiastically.\n")

        while True:
            print("1. Hear Rumors")
            print("2. Gamble")
            print("3. Hire Mercenaries (Coming Soon)")
            print("4. Black Market Upgrades (Coming Soon)")
            print("0. Return")

            cmd = input("Select: ").strip()

            if cmd == "1":
                self._random_rumor()

            elif cmd == "2":
                self._gambling_den()

            elif cmd == "3":
                print("Three bruised mercenaries size you up… This feature is coming soon.")

            elif cmd == "4":
                print("A cloaked smuggler whispers: 'I got the good stuff… but not today.'")

            elif cmd == "0":
                return

    def _random_rumor(self):
        rumors = [
            "A rogue AI ship was spotted near sector 12.",
            "Smugglers say there's a hidden wormhole near sector 17.",
            "A corporate transport vanished near the rim — pirates suspected.",
            "Someone found a planet producing rare organics at insane rates.",
            "A dancer whispers: 'Some sectors aren’t what they seem…'"
        ]
        print("\nA stranger leans close and mutters:")
        print("   \"" + random.choice(rumors) + "\"\n")

    def _gambling_den(self):
        print("\nYou sit at a neon-lit gambling table. A dealer with chrome eyes smirks.")
        bet = int(input("Place your bet: "))
        self.ship.spend_credits(bet)
        roll = random.randint(1, 100)
        if roll > 50:
            winnings = bet * 2
            self.ship.credits += winnings
            print(f"You win! Payout: {winnings} credits.")
        else:
            print("You lose. The table absorbs your credits coldly.")

    # ------------------------------------------------------------
    # Market Promenade — Luxury & Exotic Goods
    # ------------------------------------------------------------
    def market(self):
        print("\n--- MARKET PROMENADE ---")
        print("Holographic storefronts. Alien fragrances. Fashionistas and scammers.\n")

        while True:
            print("1. Buy Vanity Items")
            print("2. Browse Exotic Wares")
            print("0. Return")

            cmd = input("Select: ").strip()

            if cmd == "1":
                print("A chrome-plated clerk offers a gold-trimmed hull paintjob.")

            elif cmd == "2":
                item = random.choice(["Glitter Spice", "Xeno Wine", "Star Silk", "Void Perfume"])
                price = random.randint(100, 500)
                print(f"Exotic item: {item} — {price} credits")

            elif cmd == "0":
                return

    # ------------------------------------------------------------
    # Tech Lab — Experimental Mods (No fuel efficiency)
    # ------------------------------------------------------------
    def tech_lab(self):
        print("\n--- SCIENCE & TECH LAB ---")
        print("Sparks fly as engineers bicker over unstable prototypes.\n")

        while True:
            print("1. Buy Experimental Weapons")
            print("2. Install Minor Shield Capacitor Upgrade")
            print("3. Commission Prototype Tech (Random Effect)")
            print("0. Return")

            cmd = input("Select: ").strip()

            if cmd == "1":
                cost = 600
                self.ship.spend_credits(cost)
                print("You acquire a questionable plasma destabilizer. Handle with care.")

            elif cmd == "2":
                cost = 350
                self.ship.spend_credits(cost)
                self.ship.shields += 2
                print("A small but noticeable shield capacitor is installed (+2 shields).")

            elif cmd == "3":
                cost = 400
                self.ship.spend_credits(cost)
                effect = random.choice([
                    "hull reinforced (+5 hull)",
                    "sensor boost (+1 scanner range — cosmetic for now)",
                    "ship AI optimized (no visible effect)",
                    "reactor surge (+1 shield)",
                ])
                print(f"The prototype tech completes… {effect}.")

            elif cmd == "0":
                return
