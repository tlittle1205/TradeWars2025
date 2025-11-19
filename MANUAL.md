# TradeWars 2025 Pilot Manual

## Core Loop
- **Objective:** Accumulate 50,000 credits to become the sector’s dominant trader; hit that mark and the game congratulates you as a winner. "Game over" also triggers if your hull is destroyed.【F:tw25.py†L120-L168】
- **Commands at a glance:** Type `HELP` in game to see navigation, trading, planet, map, and save/load commands, plus quick-sell/repair options when docked at a port.【F:tw25.py†L68-L105】
- **Time and turns:** Every command advances time and a global turn counter; planets produce goods after each command, so even waiting progresses the economy.【F:tw25.py†L219-L225】

## Navigation & Awareness
- **Movement:** Use `MOVE`/`M` plus a connected sector number. Each warp costs 1 fuel, so avoid bouncing without a plan and use `WAIT` to regenerate 3–8 fuel when empty.【F:tw25.py†L271-L320】
- **Scanning:** `SCAN` lists neighboring sectors and flags ports, planets, and possible pirates—use it to chart safe or profitable routes before you commit to a jump.【F:tw25.py†L301-L314】
- **Region cues:** Sector descriptions warn about Stardock, FedSpace (safe), pirate ambush regions, and dead-ends. Treat pirate zones as higher-risk but potentially necessary shortcuts.【F:tw25.py†L233-L262】

## Trading & Profit Strategy
- **Port logic:** Each port class (BSS/SBS/SSB) defines which commodity it buys vs. sells. Prices rise when stock is low and fall when stock is high, so `BUY` where the port sells a scarce good and `SELL` where ports buy it.【F:port.py†L5-L101】【F:port.py†L105-L140】
- **Cashflow tools:** `BUY MAX` fills holds with what you can afford; `QSELL/SELL ALL` liquidates everything a port buys, updating prices afterward. Great for quick exits from dangerous sectors.【F:port.py†L142-L165】【F:tw25.py†L88-L95】
- **Market intel:** `MARKET` shows all port inventories and prices, while `AUTOTRADE` suggests a two-port route optimized for profit—use these before long hauls.【F:tw25.py†L78-L80】【F:tw25.py†L190-L195】
- **Planet storage:** Planets passively produce goods every turn. Land, stash surplus cargo or credits, and treat them as decentralized banks/warehouses that grow while you roam.【F:tw25.py†L219-L225】

## Combat & Risk Management
- **Encounter flow:** Certain sectors or random checks can spawn pirates; combat resolves in turns where you and the pirate exchange attacks until someone escapes or explodes.【F:tw25.py†L129-L130】【F:combat.py†L130-L168】
- **Damage model:** Each attack roll is attacker power plus randomness minus defense, with at least 1 damage guaranteed. Escapes have a base 40% success rate plus 1% per free cargo hold—travel light if you plan to run.【F:combat.py†L84-L125】
- **Scaling & rewards:** Pirate stats scale slightly with your attack, and victories pay bounties that can fund repairs or upgrades.【F:combat.py†L66-L78】【F:combat.py†L158-L162】
- **Defensive habits:** Keep an eye on hull via `STATUS`; repair at ports or Stardock before entering pirate-tagged space. Carry some free holds to improve escape odds, but don’t leave them empty too long—unused space is lost profit.

## Stardock & Upgrades
- **Access:** When the sector description calls out the massive superstructure, use `DOCK` to enter the Celestial Bazaar hub.【F:tw25.py†L240-L243】【F:tw25.py†L161-L164】
- **Upgrades:** Corporate Concourse lets you repair hulls, boost shields, and expand cargo holds—key for surviving longer runs or increasing trade volume.【F:stardock.py†L73-L107】
- **Banking:** The Interstellar Bank stores credits and accrues 0.5% interest each in-game day; deposit profits before risky trips and withdraw when you need a cash infusion.【F:stardock.py†L111-L144】
- **Entertainment & flavor:** The Rusty Nebula offers rumors and gambling for narrative color and the chance to double a bet (or lose it). Use with caution if funds are tight.【F:stardock.py†L146-L200】

## Practical Routes & Playstyle Tips
- **Early game:** Scan for nearby sell ports, fill holds with cheap organics/ore from selling ports, and run short hops to buying ports. Use `AUTOTRADE` as a tutor for profitable loops.【F:port.py†L105-L140】【F:tw25.py†L190-L195】
- **Midgame:** Expand cargo at Stardock, then chain multi-port circuits. Store overflow on planets you trust and withdraw later to bankroll upgrades or absorb combat repairs.【F:stardock.py†L73-L107】【F:tw25.py†L219-L225】
- **Pirate country:** Enter pirate-tagged sectors only when hull is healthy and fuel topped off. If holds are full, consider quickselling at the nearest port before crossing to keep escape odds high.【F:tw25.py†L240-L262】【F:port.py†L142-L165】
- **Win push:** Once your trading loop nets reliable profits, bank surplus for interest and keep running autotrade routes until you hit 50,000 credits to finish the run.【F:tw25.py†L120-L125】【F:stardock.py†L111-L144】
