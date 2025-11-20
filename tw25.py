# tw25.py
# ============================================================
# Main game loop and command parser for TW2025
#
# Depends on:
#   - ship.py     (Ship)
#   - port.py     (Port, COMMODITIES)
#   - planet.py   (Planet)
#   - galaxy.py   (Galaxy, Sector)
#   - combat.py   (CombatEngine)
#   - stardock.py (StarDock)
#   - render_map.py (render_galaxy_map)
#   - debug_tools.py (run_all_debug)
# ============================================================

import random
import textwrap
import json

from time import sleep
from ui import Color #Used to add a splash of color here and there
from ship import Ship
from port import COMMODITIES
from galaxy import Galaxy
from combat import CombatEngine
from stardock import StarDock
from descriptions import depart
from descriptions import departPort
from descriptions import landingPort
from utils import clearscr

# Optional: console clear (won't fully clear IDLE, but works in a real terminal)
# ============================================================
# UNIVERSAL CLEAR + INPUT WRAPPER
# ============================================================

def clear_screen():
    """Clear terminal screen universally."""
    print("\033[2J\033[H", end="")

def intercept_clear(cmd: str):
    """
    Detect commands that should clear the screen.
    Called both inside TW25 and inside Stardock via sd_input().
    """
    if cmd in ["cls", "clear"]:
        clear_screen()
        return True
    return False

def game_input(prompt="> "):
    """
    Replacement for input() everywhere.
    Supports:
        - CLS/CLEAR anytime, any menu, anywhere
        - Returns clean command string
    """
    while True:
        raw = input(prompt)
        if not raw:
            return ""  # allow empty input
        
        cmd = raw.strip().lower()

        # Clear-screen handling
        if intercept_clear(cmd):
            continue

        return cmd



class TW25Game:
    def __init__(self, num_sectors: int = 24):
        self.turn = 0
        self.max_turns = 9999

        # Simple in-game time system for interest, events, etc.
        self.time = 0   # increments every command
        self.day = 0    # increments every N actions

        self.player = Ship()
        self.galaxy = Galaxy(num_sectors=num_sectors)
        self.combat_engine = CombatEngine(self.player)
        self.stardock = StarDock(self.player, self.galaxy)

        self.intro()

    # --------------------------------------------------------
    # Intro / Help
    # --------------------------------------------------------

    def intro(self):
    
        clearscr()
        print(Color.RED+r"""
                             _____             _     __        __                   
                            |_   _| __ __ _ __| |  __\ \      / /_ _ _ __ ___       
                              | || '__/ ` |/ _` | / _ \ \ /\ / / _` | '__/ __|      
                              | || | | (_| | (_| |  __/\ V  V / (_| | |  \__ \      
                              |_||_|  \__,_|\__,_|\___| \_/\_/_\__,_|_| _|___/____  
                                                            |___ \ / _ \___ \| ___| 
                                                              __) | | | |__) |___ \ 
                                                             / __/| |_| / __/ ___) |
                                                            |_____|\___/_____|____/ 
        """+Color.RESET)
        print(
            textwrap.fill(
                "You command a small trade vessel roaming a fringe star cluster. "
                "Buy low, sell high, upgrade your ship, stash goods on planets, "
                "and survive encounters with ruthless Space Pirates.",
                width=80,
            )
        )
  

    def help(self):
        print(
            """
Commands:
  M or MOVE [sector]   - Warp to a connected sector.
  SCAN                 - Show connected sectors and nearby ports/pirates.
  P or PORT            - Trade at the local port (if present).
  L or LAND            - Land on the planet in this sector (if present).
  S or STATUS          - Show ship status.
  C, I or CARGO        - Show cargo manifest.
  W or WAIT            - Pass a turn, regenerating a bit of fuel.
  MARKET or MR         - Show galaxy-wide market report of all ports.
  AUTOTRADE or AT      - Suggest an optimal two-port trade route.
  MAP                  - Render and save a visual galaxy map (PNG).
  DOCK                 - Enter Stardock (if in a Stardock sector).
  SAVE / LOAD          - Save or load your game.
  DEBUG ALL            - Run full galaxy diagnostics (dev tool).
  CLEAR or CLS         - Attempt to clear the screen.
  Q or QUIT            - End the game.

Port commands (inside PORT):
  BUY <commodity> <amount>
  BUY MAX <commodity>
  SELL <commodity> <amount>
  SELL ALL
  Q or QSELL           - Quick-sell everything this port will buy.
  REPAIR               - Repair ship hull (costs credits).
  LEAVE                - Undock from port.

Planet commands (inside LAND):
  STATUS               - Show planet summary.
  DEPOSIT <commodity> <amount>
  WITHDRAW <commodity> <amount>
  DEPOSITCR <amount>   - Deposit credits into planet treasury.
  WITHDRAWC <amount>   - Withdraw credits from planet treasury.
  LEAVE                - Take off and return to space.
"""
        )

    # --------------------------------------------------------
    # Main Loop
    # --------------------------------------------------------

    def run(self):
        while True:
            sec = self.current_sector()

            # Check for death
            if self.player.is_destroyed:
                print(Color.RED+"\nYour ship has been destroyed. Game over."+Color.RESET)
                break

            # Simple win condition
            if self.player.credits >= 5000000:
                print("\nYour accounts overflow with credits.")
                print("Merchants whisper your name with respect—and pirates with fear.")
                print("You have effectively 'won' this sector of space. Well done, captain.")
                break

            self.describe_location()

            # Possible pirate encounter
            self.maybe_pirate_encounter()

            cmd = input("\n[Terminal]: ").strip().lower()
            if not cmd:
                continue

            # Core commands
            if cmd in ["?", "help", "h"]:
                self.help()

            elif cmd in ["q", "quit", "exit"]:
                #print("\nAutosaving your game before exit...")
                self.save_game()
                print(Color.YELLOW+"Game saved. Safe travels, Captain."+Color.RESET)
                break

            elif cmd in ["clear", "cls"]:
                clear_screen()
                continue

            elif cmd == "save":
                self.save_game()
                # don't advance time on pure save
                continue

            elif cmd == "load":
                self.load_game()
                # rebind convenience
                sec = self.current_sector()
                continue

            elif cmd == "dock" and sec.type == "STARDOCK":
                clearscr()
                self.stardock.enter()
                # Stardock actions still count as time overall, but we continue loop.
                # fall through to time advance at bottom

            elif cmd.startswith("move") or cmd.startswith("m "):
                self.command_move(cmd)

            elif cmd == "m":
                self.command_move("m")

            elif cmd in ["scan"]:
                self.scan()

            elif cmd in ["port", "p"]:
                clearscr()
                print(Color.GREEN+landingPort())
                self.visit_port()

            elif cmd in ["land", "l"]:
                self.land_on_planet()

            elif cmd in ["status", "s"]:
                self.show_status()

            elif cmd in ["cargo", "c", "i"]:
                self.show_cargo()

            elif cmd in ["wait", "w"]:
                self.wait_turn()

            elif cmd in ["market", "mr"]:
                clearscr()
                self.market_report()

            elif cmd in ["autotrade", "auto-trade", "at"]:
                self.auto_trade()

            elif cmd == "map":
                try:
                    clear_screen()
                    print(Color.GREEN+"Trajectory locked. Engines humming. The void is watching. Launch the probe....")
                    sleep(1.7)
                    print("   Let the stars bear witness — deploy the seeker...")
                    sleep(1.1)
                    print("      Probe ignition in 3… 2… 1… tear open the veil")
                    sleep(2.0)
                    print("          Probe deployed. Destiny accepts our challenge...")
                    sleep(3.0)
                    print("...")
                    sleep(.9)
                    print("..............Receiving scan data...\n"+Color.RESET)
                    sleep(2.4)
                    from render_map import render_galaxy_map

                    render_galaxy_map(
                        self.galaxy,
                        player_sector=self.player.location,
                        save_png=True,
                    )
                except ImportError:
                    print("Map rendering is not available (render_map.py missing).")

            elif cmd == "debug all":
                try:
                    from debug_tools import run_all_debug

                    run_all_debug(self.galaxy)
                except ImportError:
                    print("Debug tools not available (debug_tools.py missing).")

            else:
                print("Unknown command. Type HELP for options.")

            # Turn + time progression
            self.turn += 1
            self.advance_time()

            # After each command, tick all planets
            self.planet_production_tick()

    # --------------------------------------------------------
    # Location / Status
    # --------------------------------------------------------

    def current_sector(self):
        return self.galaxy.get_sector(self.player.location)

    def describe_location(self):
        sec = self.current_sector()

        print(Color.RED+f"\n=== {sec.name} (#{sec.id}) ==="+Color.RESET)
        neighbors = ", ".join(str(n) for n in sorted(sec.neighbors))
        print(Color.MAGENTA+f"Connected sectors: {neighbors}"+Color.RESET)

        # Sector Type Announcements
        if sec.type == "STARDOCK":
            print(Color.BRIGHT_YELLOW+"\n*=*=*=*=*=*=*=*=*=*=*=*="+Color.RESET)
            print(Color.CYAN+"*=*=*=*=Stardock*=*=*=*="+Color.RESET)
            print(Color.BRIGHT_YELLOW+"*=*=*=*=*=*=*=*=*=*=*=*="+Color.RESET)
            print(Color.CYAN+"You see the massive shimmering superstructure of Stardock here.\n"+Color.RESET)
            print("Type DOCK to enter the Celestial Bazaar.")
        elif sec.type == "FEDSPACE":
            print(Color.BLUE+"This is secure FEDSPACE. Pirates avoid this region."+Color.RESET)
        elif sec.type == "PIRATE":
            print(Color.RED+"Warning: This region is known for pirate ambushes. Best to not linger for long in this sector."+Color.RESET)
        elif sec.type == "DEADEND":
            print("Dead-end sector — only one way in or out.")

        # Port
        if sec.port:
            print(Color.GREEN+f"Port present: {sec.port.name} (Class {sec.port.class_code()})"+Color.RESET)

        # Planet
        if sec.planet:
            print(Color.GREEN+f"Planet present: {sec.planet.name}"+Color.RESET)

        # Pirates
        if sec.has_pirates:
            print(Color.YELLOW+"Long-range sensors ping: possible pirate activity nearby."+Color.RESET)

    def show_status(self):
        clearscr()
        print(Color.RED+"Running diagnostics...")
        sleep(2)
        print("         .........Processing ship data")
        sleep(2)
        print("----------------------"+Color.RESET)
        print(Color.GREEN+self.player.status_summary()+Color.RESET)

    def show_cargo(self):
        print()
        print(self.player.cargo_summary())

    # --------------------------------------------------------
    # Movement / Scan / Wait
    # --------------------------------------------------------

    def command_move(self, cmd: str):
        parts = cmd.split()
        sec = self.current_sector()

        if len(parts) == 1:
            dest = input("Warp to which connected sector? ").strip()
        else:
            dest = parts[1]

        if not dest.isdigit():
            print("Invalid sector number.")
            return

        dest = int(dest)
        if dest not in sec.neighbors:
            print("That sector is not directly connected.")
            return

        if self.player.fuel <= 0:
            print("You are out of fuel! We will have to WAIT a cycle or two to rebuild our fuel.")
            return

        self.player.use_fuel(1)
        self.player.location = dest
        print(f"Warped to sector {dest}.")

    def scan(self):
        sec = self.current_sector()
        print("\nScanning...")
        for nid in sorted(sec.neighbors):
            nsec = self.galaxy.get_sector(nid)
            tags = []
            if nsec.port:
                tags.append(f"Port {nsec.port.class_code()}")
            if nsec.planet:
                tags.append("Planet")
            if nsec.has_pirates:
                tags.append("Pirates?")
            tag_str = f" [{' ,'.join(tags)}]" if tags else ""
            print(f"  Sector {nid}{tag_str}")

    def wait_turn(self):
        gained = random.randint(3, 8)
        self.player.refuel(gained)
        print(
            f"You drift in space, running low-power drills. Fuel increases by {gained}."
        )

    # --------------------------------------------------------
    # Planet Production
    # --------------------------------------------------------

    def planet_production_tick(self):
        # Every turn, planets produce resources
        for sec in self.galaxy.sectors.values():
            if sec.planet:
                sec.planet.production_tick()

    # --------------------------------------------------------
    # Port Interaction
    # --------------------------------------------------------

    def visit_port(self):
        sec = self.current_sector()
        if not sec.port:
            print("No port in this sector.")
            return

        port = sec.port
        while True:
            print()
            print(port.port_summary())
            print()
            print(Color.RED+
                f"\nYou have {self.player.credits} credits and {self.player.free_holds} free holds."+Color.RESET
            )
            print("Port Commands:")
            print("  -Buy <commodity> <amount>")
            print("  -Buy Max <commodity>")
            print("  -Sell <commodity> <amount>")
            print("  -Sell All")
            print("  -Q or QSELL  (quick-sell everything this port buys)")
            print("  -Repair")
            print("  -L or Leave")
            print()
            cmd = input("\n[Terminal]: ").strip().lower()

            if not cmd:
                continue

            if cmd in ["leave", "l", "exit"]:
                clear_screen()
                print(Color.GREEN+departPort()+Color.RESET)
                break

            if cmd in ["q", "qsell", "q-sell", "sell all"]:
                gained = port.quicksell(self.player)
                if gained > 0:
                    print(f"You quicksell your relevant cargo for {gained} credits.")
                else:
                    print("You have nothing this port wants to buy.")
                continue

            parts = cmd.split()

            if parts[0] == "repair":
                self.repair_ship_at_port()
                continue

            # BUY MAX <commodity>
            if len(parts) >= 2 and parts[0] == "buy" and parts[1] == "max":
                if len(parts) != 3:
                    print("Usage: BUY MAX <commodity>")
                    continue
                commodity = parts[2]
                if commodity not in COMMODITIES:
                    print("Unknown commodity.")
                    continue
                try:
                    amt = port.buy_max(self.player, commodity)
                    if amt > 0:
                        print(f"Purchased {amt} units of {commodity}.")
                    else:
                        print("You can't afford any, or have no cargo space.")
                except ValueError as e:
                    print(e)
                continue

            # BUY/SELL <commodity> <amount>
            if parts[0] in ["buy", "sell"] and len(parts) == 3:
                action, commodity, amount = parts
                if commodity not in COMMODITIES:
                    print("Unknown commodity.")
                    continue
                if not amount.isdigit():
                    print("Amount must be a positive number.")
                    continue
                amount = int(amount)
                if amount <= 0:
                    print("Amount must be positive.")
                    continue

                try:
                    if action == "buy":
                        port.buy_from_port(self.player, commodity, amount)
                        print(f"Purchased {amount} units of {commodity}.")
                    else:
                        port.sell_to_port(self.player, commodity, amount)
                        print(f"Sold {amount} units of {commodity}.")
                except ValueError as e:
                    print(e)
            else:
                print("Unknown port command.")

    def repair_ship_at_port(self):
        if self.player.hull >= self.player.max_hull:
            print("Your hull is already at full strength.")
            return

        needed = self.player.max_hull - self.player.hull
        cost_per_point = 5
        max_affordable = self.player.credits // cost_per_point

        if max_affordable <= 0:
            print("You can't afford any repairs.")
            return

        to_repair = min(needed, max_affordable)
        cost = to_repair * cost_per_point

        confirm = (
            input(f"Repair {to_repair} hull for {cost} credits? (y/n) ")
            .strip()
            .lower()
        )
        if confirm.startswith("y"):
            self.player.spend_credits(cost)
            self.player.repair(to_repair)
            print(
                f"Hull repaired by {to_repair}. Now at {self.player.hull}/{self.player.max_hull}."
            )
        else:
            print("Repairs cancelled.")

    # --------------------------------------------------------
    # Planet Interaction
    # --------------------------------------------------------

    def land_on_planet(self):
        sec = self.current_sector()
        if not sec.planet:
            print("No planet in this sector.")
            return

        planet = sec.planet
        print(Color.CYAN+f"\nYou descend to the surface of {planet.name}.\n"+Color.RESET)

        while True:
            print("=== Planetary Command Menu ===")
            print("1) Planet Status")
            print("2) Deposit Commodity")
            print("3) Withdraw Commodity")
            print("4) Deposit Credits")
            print("5) Withdraw Credits")
            print("6) Leave Planet")
            print("--------------------------------")
            choice = input("Planet> ").strip()

            if choice == "1":  # STATUS
                print()
                print(planet.planet_summary())

            elif choice == "2":  # DEPOSIT commodity
                print("\nAvailable cargo in your ship:")
                print(self.player.cargo_summary())
                commodity = input("Deposit which commodity? ").strip().lower()
                if commodity not in COMMODITIES:
                    print("Unknown commodity.")
                    continue
                amt = input("Amount to deposit: ").strip()
                if not amt.isdigit():
                    print("Amount must be numeric.")
                    continue
                amt = int(amt)
                try:
                    self.player.remove_cargo(commodity, amt)
                    planet.deposit_commodity(commodity, amt)
                    print(
                        f"Deposited {amt} units of {commodity} onto {planet.name}."
                    )
                except ValueError as e:
                    print(e)

            elif choice == "3":  # WITHDRAW commodity
                print("\nPlanetary stock:")
                print(planet.planet_summary())
                commodity = input("Withdraw which commodity? ").strip().lower()
                if commodity not in COMMODITIES:
                    print("Unknown commodity.")
                    continue
                amt = input("Amount to withdraw: ").strip()
                if not amt.isdigit():
                    print("Amount must be numeric.")
                    continue
                amt = int(amt)
                try:
                    planet.withdraw_commodity(commodity, amt)
                    self.player.add_cargo(commodity, amt)
                    print(
                        f"Withdrew {amt} units of {commodity} from {planet.name}."
                    )
                except ValueError as e:
                    print(e)

            elif choice == "4":  # DEPOSIT CREDITS
                print(f"\nYou have {self.player.credits} credits.")
                amt = input(
                    "Deposit how many credits into the treasury? "
                ).strip()
                if not amt.isdigit():
                    print("Amount must be numeric.")
                    continue
                amt = int(amt)
                try:
                    self.player.spend_credits(amt)
                    planet.deposit_credits(amt)
                    print(
                        f"Deposited {amt} credits into {planet.name}'s treasury."
                    )
                except ValueError as e:
                    print(e)

            elif choice == "5":  # WITHDRAW CREDITS
                print(f"\nPlanet treasury contains {planet.treasury} credits.")
                amt = input("Withdraw how many credits? ").strip()
                if not amt.isdigit():
                    print("Amount must be numeric.")
                    continue
                amt = int(amt)
                try:
                    planet.withdraw_credits(amt)
                    self.player.add_credits(amt)
                    print(
                        f"Withdrew {amt} credits from {planet.name}'s treasury."
                    )
                except ValueError as e:
                    print(e)

            elif choice == "6":  # LEAVE
                clearscr()
                print(Color.GREEN+f"You lift off from {planet.name} and return to orbit."+Color.RESET)
                break

            else:
                print("Invalid selection. Choose a number 1–6.")

    # --------------------------------------------------------
    # Market Report / Autotrade
    # --------------------------------------------------------

    def market_report(self):
        print(Color.GREEN+"\nGalaxy Market Report")
        print("Sec  Port Name           Class  Ore        Org        Eqp")
        print("---------------------------------------------------------------")
        for sid in sorted(self.galaxy.sectors.keys()):
            sec = self.galaxy.sectors[sid]
            if not sec.port:
                continue
            p = sec.port
            code = p.class_code()

            def fmt(c):
                mode = "B" if p.can_buy_from_player(c) else "S"
                return f"{mode}:{p.prices[c]:>4}"

            ore_s = fmt("ore")
            org_s = fmt("organics")
            eqp_s = fmt("equipment")
            print(Color.GREEN+
                f"{sid:>3}  {p.name:<18} {code:<5} {ore_s:<9} {org_s:<9} {eqp_s:<9}"+Color.RESET
            )

    def auto_trade(self):
        """
        Suggest a profitable two-port trade route.
        """
        best = None

        for sid1, sec1 in self.galaxy.sectors.items():
            if not sec1.port:
                continue
            p1 = sec1.port

            for sid2, sec2 in self.galaxy.sectors.items():
                if sid1 == sid2 or not sec2.port:
                    continue
                p2 = sec2.port

                dist = self.galaxy.shortest_distance(sid1, sid2)
                if dist is None or dist <= 0:
                    continue

                for c in COMMODITIES:
                    if p1.can_sell_to_player(c) and p2.can_buy_from_player(c):
                        buy_price = p1.prices[c]
                        sell_price = p2.prices[c]
                        profit_per_unit = sell_price - buy_price
                        if profit_per_unit <= 0:
                            continue

                        score = profit_per_unit / dist
                        if not best or score > best["score"]:
                            best = {
                                "from_sid": sid1,
                                "to_sid": sid2,
                                "commodity": c,
                                "buy_price": buy_price,
                                "sell_price": sell_price,
                                "profit_per_unit": profit_per_unit,
                                "dist": dist,
                                "score": score,
                            }

        if not best:
            print("\nNo profitable port-to-port trade routes detected right now.")
            return

        s = self.player
        max_units = 0
        if best["buy_price"] > 0:
            max_units = min(s.max_holds, s.credits // best["buy_price"])
        est_profit = max_units * best["profit_per_unit"]

        clearscr()
        print(Color.CYAN+"Recommended Trade Route:"+Color.RESET)
        print(
            f"  Buy  : {best['commodity'].capitalize()} in sector {best['from_sid']} "
            f"({self.galaxy.sectors[best['from_sid']].port.name}) at {best['buy_price']} cr/unit."
        )
        print(
            f"  Sell : {best['commodity'].capitalize()} in sector {best['to_sid']} "
            f"({self.galaxy.sectors[best['to_sid']].port.name}) at {best['sell_price']} cr/unit."
        )
        print(f"  Profit per unit : {best['profit_per_unit']} credits")
        print(f"  Distance: {best['dist']} hops")
        if max_units > 0:
            print(Color.RED+
                f"  With your current finances and holds, a full run could net ~{est_profit} credits."+Color.RESET
            )
        else:
            print("  You currently lack credits or cargo space to exploit this fully.")
            print(Color.GREEN+"<<<==x==x==x==x==x==x==x==x==>>>"+Color.RESET)

        path_to_buy = self.galaxy.shortest_path(
            self.player.location, best["from_sid"]
        )
        if path_to_buy:
            print("\nRoute from your current sector to buy port:")
            print("  " + " -> ".join(str(sid) for sid in path_to_buy))
            print(Color.GREEN+"<<<==x==x==x==x==x==x==x==x==>>>"+Color.RESET)
        else:
            print(
                "\nCould not find a path from your location to the recommended buy port."
            )
            print(Color.GREEN+"<<<==x==x==x==x==x==x==x==x==>>>"+Color.RESET)

    # --------------------------------------------------------
    # Pirate Encounters
    # --------------------------------------------------------

    def maybe_pirate_encounter(self):
        sec = self.current_sector()
        if not sec.has_pirates:
            return

        # 40% chance of actual encounter when pirates present
        if random.random() >= 0.4:
            return

        print("\nALERT: Sensors detect a hostile ship in this sector...")
        result = self.combat_engine.engage()

        print()
        for line in result["log"]:
            print(line)

        if result["result"] == "win":
            sec.has_pirates = False
        elif result["result"] == "death":
            # handled on next loop
            pass
        elif result["result"] == "escaped":
            pass

    # --------------------------------------------------------
    # Time & Interest
    # --------------------------------------------------------

    def advance_time(self):
        """
        Advance global time and check for daily interest.
        """
        self.time += 1
        self._check_daily_interest_tick()

    def _check_daily_interest_tick(self):
        # Every 20 actions = 1 in-game day
        if self.time > 0 and self.time % 20 == 0:
            self.day += 1
            self.apply_daily_interest()

    def apply_daily_interest(self):
        """
        Apply 0.5% daily interest to banked credits (if any).
        """
        # Ship is expected to have bank_balance (used by Stardock bank)
        balance = getattr(self.player, "bank_balance", 0)
        if balance <= 0:
            return

        rate = 0.005  # 0.5% per day
        interest = int(balance * rate)
        if interest <= 0:
            return

        self.player.bank_balance += interest
        print(
            f"\nDaily Interest: +{interest} credits added to your bank balance "
            f"(Day {self.day}, New Balance: {self.player.bank_balance})."
        )

    # --------------------------------------------------------
    # Save / Load
    # --------------------------------------------------------

    def save_game(self, filename="savegame.json"):
        data = {
            "turn": self.turn,
            "time": self.time,
            "day": self.day,
            "player": self.player.to_dict(),
            "galaxy": self.galaxy.to_dict(),
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        #print(f"Game saved to {filename}.")

    def load_game(self, filename="savegame.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No savegame.json file found.")
            return

        self.turn = data.get("turn", 0)
        self.time = data.get("time", 0)
        self.day = data.get("day", 0)

        self.player = Ship.from_dict(data["player"])
        self.galaxy = Galaxy.from_dict(data["galaxy"])
        self.combat_engine = CombatEngine(self.player)
        self.stardock = StarDock(self.player, self.galaxy)

        # Validate player location
        if self.player.location not in self.galaxy.sectors:
            print(
                f"WARNING: Save file points to invalid sector {self.player.location}. "
                "Resetting to sector 1."
            )
            self.player.location = 1

        print("Game successfully loaded.")


# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------

def main():
    random.seed()
    game = TW25Game(num_sectors=100)
    game.run()


if __name__ == "__main__":
    main()
