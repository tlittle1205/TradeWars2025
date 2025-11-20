# debug_tools.py
import pprint

# Colors for terminal clarity (IDLE ignores them but VSCode/console will show)
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


def header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)


# ============================================================
# 1. VALIDATE ALL SECTORS
# ============================================================

def validate_sectors(galaxy):
    header("SECTOR VALIDATION")

    errors = []
    for sid, sec in galaxy.sectors.items():

        # Sector ID sanity
        if sid != sec.id:
            errors.append(f"Sector dict key {sid} mismatches sec.id {sec.id}")

        # Name sanity
        if not isinstance(sec.name, str):
            errors.append(f"Sector {sid} name invalid: {sec.name}")

        # Neighbor format
        if not isinstance(sec.neighbors, set):
            errors.append(f"Sector {sid} neighbors is not a set!")

        # Neighbor exists
        for n in sec.neighbors:
            if n not in galaxy.sectors:
                errors.append(f"Sector {sid} links to unknown neighbor {n}")

    if errors:
        print(RED + "❌ Sector problems detected:" + RESET)
        for e in errors:
            print(" -", e)
    else:
        print(GREEN + "✔ All sectors valid." + RESET)


# ============================================================
# 2. VALIDATE WARP LANES (BIDIRECTIONAL)
# ============================================================

def validate_warp_lanes(galaxy):
    header("WARP LANE VALIDATION")

    bad_links = []

    for sid, sec in galaxy.sectors.items():
        for n in sec.neighbors:
            # A must list B, AND B must list A
            if sid not in galaxy.sectors[n].neighbors:
                bad_links.append((sid, n))

    if bad_links:
        print(RED + "❌ One-way warp lanes detected!" + RESET)
        for a, b in bad_links:
            print(f" - {a} lists {b}, but {b} does NOT list {a}")
    else:
        print(GREEN + "✔ All warp lanes are correctly bidirectional." + RESET)


# ============================================================
# 3. VALIDATE MAP CONNECTIVITY (NO ISOLATED SECTORS)
# ============================================================

def validate_connectivity(galaxy):
    header("CONNECTIVITY VALIDATION")

    isolated = [sid for sid, sec in galaxy.sectors.items() if len(sec.neighbors) == 0]

    if isolated:
        print(RED + "❌ Isolated sectors found:" + RESET, isolated)
    else:
        print(GREEN + "✔ No isolated sectors." + RESET)


# ============================================================
# 4. VALIDATE PATHFINDING
# ============================================================

def validate_pathfinding(galaxy):
    header("PATHFINDING VALIDATION")

    # Sanity: every sector should be reachable from every other sector
    unreachable = []

    all_sids = list(galaxy.sectors.keys())

    for a in all_sids:
        for b in all_sids:
            dist = galaxy.shortest_distance(a, b)
            if dist is None:
                unreachable.append((a, b))

    if unreachable:
        print(RED + "❌ Unreachable sector pairs found!" + RESET)
        for pair in unreachable[:20]:  # avoid screen spam
            print(" -", pair)
        if len(unreachable) > 20:
            print("  ...and more omitted.")
    else:
        print(GREEN + "✔ All sectors mutually reachable." + RESET)


# ============================================================
# 5. VALIDATE PORTS
# ============================================================

def validate_ports(galaxy):
    header("PORT VALIDATION")

    errors = []

    for sid, sec in galaxy.sectors.items():
        if sec.port:
            port = sec.port

            # Check prices
            for c, price in port.prices.items():
                if not isinstance(price, int) or price <= 0:
                    errors.append(f"Sector {sid} port has invalid price for {c}: {price}")

            # Modes
            if not isinstance(port.modes, dict):
                errors.append(f"Sector {sid} port modes invalid.")

    if errors:
        print(RED + "❌ Port issues detected:" + RESET)
        for e in errors:
            print(" -", e)
    else:
        print(GREEN + "✔ All ports valid." + RESET)


# ============================================================
# 6. VALIDATE PLANETS
# ============================================================

def validate_planets(galaxy):
    header("PLANET VALIDATION")

    errors = []

    for sid, sec in galaxy.sectors.items():
        if sec.planet:
            p = sec.planet

            # Goods structure
            if not isinstance(p.goods, dict):
                errors.append(f"Sector {sid}: planet.goods is not a dict.")

            # Treasury
            if p.treasury < 0:
                errors.append(f"Sector {sid}: planet treasury negative ({p.treasury}).")

            # Production
            if not isinstance(p.production_rates, dict):
                errors.append(f"Sector {sid}: production_rates missing or invalid.")

    if errors:
        print(RED + "❌ Planet issues detected:" + RESET)
        for e in errors:
            print(" -", e)
    else:
        print(GREEN + "✔ All planets valid." + RESET)


# ============================================================
# 7. VALIDATE SPECIAL SECTORS (FEDSPACE, PIRATE, STARDOCK)
# ============================================================

def validate_special_sectors(galaxy):
    header("SPECIAL SECTOR VALIDATION")

    problems = []

    for sid, sec in galaxy.sectors.items():
        if sec.type == "STARDOCK" and sec.port is not None:
            problems.append(f"Stardock sector {sid} should NOT have a port.")

        if sec.type == "PIRATE" and not sec.has_pirates:
            problems.append(f"Pirate sector {sid} has no has_pirates flag.")

    if problems:
        print(RED + "❌ Special-sector issues found:" + RESET)
        for p in problems:
            print(" -", p)
    else:
        print(GREEN + "✔ All special-sector rules validated." + RESET)

# ============================================================
# 8. LIST SECTORS WITH PORTS AND PLANETS (FORMATTED)
# ============================================================

def list_sectors_with_ports_and_planets(galaxy):
    header("SECTORS WITH PORTS AND PLANETS")

    for sid, sec in galaxy.sectors.items():
        port_name   = sec.port.name   if sec.port else ""
        planet_name = sec.planet.name if sec.planet else ""

        # Format as:  Sector: Port: [name] | Planet: [name]
        print(f"Sector {sid}: Port: [{port_name:<20}] | Planet: [{planet_name:<20}]")



# ============================================================
# 9. FULL GALAXY DIAGNOSTIC
# ============================================================

def run_all_debug(galaxy):
    """
    Run every validation check in order.
    """
    validate_sectors(galaxy)
    validate_warp_lanes(galaxy)
    validate_connectivity(galaxy)
    validate_pathfinding(galaxy)
    validate_ports(galaxy)
    validate_planets(galaxy)
    validate_special_sectors(galaxy)
    list_sectors_with_ports_and_planets(galaxy)