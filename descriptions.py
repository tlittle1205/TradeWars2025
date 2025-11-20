import random
import textwrap

DOCK_DEPARTURE_TEXTS = [
    "The roar of the bazaar lingers as your ship rises from the landing pad. Vendors shout final offers, star-charts flap in the wind, and a haggling droid curses in binary as you slip away. The sun hits the durasteel rooftops at a harsh angle, turning the whole port into a patchwork of glowing steel. With a final hiss of vapor, your thrusters kick, lifting you above the noise, the smell of spice-dust, and the teeming crowds. Space stretches ahead — quiet, cold, and nothing like the chaos below.",
    "You bank left, gliding past the rusted communications spire where underpaid controllers wave traffic through with more hope than precision. Ships of every legal status flash their running lights as they weave between freight haulers and smugglers pretending to be freight haulers. The whole port looks like a metal anthill from up here — bustling, bright, and just a little lawless. By the time your nav-computer locks onto the next sector, the planet’s haze has already swallowed the port behind you.",
    "Your engines punch through the thick amber smog clinging to the port like a second atmosphere. Below, the fuel depots flicker with blue flame and the cantina district buzzes with neon signs advertising things no sane pilot would try. You shake off the grit, literally — the hull rattles from blown sand and stray refuse — and the port dissolves into a grid of trembling lights. Ahead lies open void and whatever waits for you in the next sector.",
    "As you lift off, you can feel it — hundreds of eyes tracking your ship. Dock workers, scavengers, bounty hunters, and drifters all look up for just a heartbeat, wondering whether you’ll return rich, ruined, or not at all. You clear the docking rings, each one humming with magnetic coils that tug at your ship’s plating. When the last ring falls away, the port becomes nothing more than a scar of bright metal on the planet’s skin. Space welcomes you with indifferent silence.",
    "Traffic control cracks over your comm with a bored warning you promptly ignore. Four ships cut across your path, engines whining like dying beasts. A bulk carrier belches coolant into the sky as someone swears at it in four languages. You thrust past the chaos, leaving the clang of cargo cranes and the electro-jazz thumping from a rooftop bar behind. Then — just like walking through a door — the noise dies and stars bloom across your canopy.",
    "Your ship rises over a patchwork hellscape of scavenger huts, jury-rigged refueling stations, and the skeletal remains of older vessels. Sparks fly as welders tear another derelict apart. Kids chase each other between towering mounds of scrap. A mechanical beast — half loader, half garbage compactor — roars to life beneath you. Once you clear the outer ring, the scrapyard becomes a swirl of metallic color, and you’re free of the gravitational pull of that chaotic world.",
    "You pass over the glow of night markets and cantinas still throbbing with music. Shadows dance between buildings as smugglers deal spice, starfarers bluff through card games, and droids argue with barkeeps. The whole district hums like a neon beehive — vibrant, loud, and dangerous if you look at anyone too long. You angle up, engines spooling hot, and the lights dissolve into a smear of electric color as you break for orbit.",
    "Leaving the port means threading your way through the drifting junk cloud — everything from broken panels to the occasional unreported corpse. Thrusters flare, shields flicker, and warning lights ping as debris skitters off your hull. Below, the port’s floodlights carve sharp shadows across the wasteland of cargo pallets and fuel pools. Then, with a final jolt, you break free of the cloud and the void opens wide before you.",
    "A pair of bored port security craft track you for exactly three seconds before returning to their card game. On the docks below, a brawl breaks out near a spice stall while a preacher shouts doomsday prophecies at passing miners. Your ship climbs steadily, the din fading into a faint rumble. Once you breach the upper atmosphere, the port becomes a bright scar on the horizon — small, loud, and full of trouble you’re glad to leave behind.",
    "Heat vents belch steam upward, fogging the lower viewing ports. You rise past the undercity’s rusted walkways and patched-together apartments stacked like mismatched bricks. A shuttle screams by on emergency burn, chased by two smaller ships with weapons charged. Typical day. You punch your thrusters, roll starboard, and the entire mess of humanity, droids, thieves, traders, and saints collapses into distance. Ahead is a sky full of possibility — and probably a few mistakes."
]

def depart():
    return random.choice(DOCK_DEPARTURE_TEXTS)

PORT_DEPARTURE_TEXTS = [
    "Your ship lifts off as the noise, neon, and chaos of the port collapse into a shrinking smear of color below you.",
    "Thrusters roar, scattering dust and vendors alike as you punch upward through the crowded launch lanes.",
    "The docking clamps release with a metallic clunk, and the port fades behind you like a half-remembered danger.",
    "You rise through the heat vents and exhaust plumes, leaving the grime-soaked city sprawled beneath your hull.",
    "Engines flare bright as you blast past shuttles, cargo drones, and a few pilots who definitely shouldn’t be flying.",
    "The port’s tangled web of lights and shadows drops away, replaced by the cold, honest stars above.",
    "A final burst of thrust carries you clear of the smog halo, severing the last ties between you and the port’s chaos.",
    "Your ship slips through the departure lanes, dodging freighters and hustlers as the world below softens into distance.",
    "The comm crackles with static warnings you ignore while the port shrinks into a dim, flickering memory.",
    "With a smooth upward burn, you leave behind the noise, the deals, and the eyes that never stop watching."
]

def departPort():
    return textwrap.fill(random.choice(PORT_DEPARTURE_TEXTS), width=80)
    
PORT_LANDING_TEXTS = [
    "Your ship breaks through a curtain of swirling dust as the outpost’s lone landing beacon flickers weakly in the haze. Your ship touches down on a pad made of mismatched metal sheets held together by stubbornness and old welds. A single dockhand wanders over, squinting like he’s not sure whether you’re a visitor or bad weather.",
    "Freighters swarm the airspace like bees around a hive as you descend toward the brightly lit trading port. Traffic control barks rapid-fire instructions, barely keeping up with the flow of inbound ships. When your skids hit the deck, the surrounding chaos doesn’t even pause — it simply envelopes you.",
    "You land amid a maze of shadowy figures loitering between cargo crates and flickering neon signs. A group of rough-looking traders size up your ship the moment your engines cool. You step onto the platform knowing half the people here want to sell you something — and the other half want to steal it.",
    "Your ship touches down in a vast docking bay where your landing echoes louder than any welcome. A handful of maintenance drones glide by, ignoring you with mechanical indifference. The air feels stale, like this place hasn’t seen real traffic in months.",
    "A plume of reddish grit rises as your thrusters kick up the barren soil around the landing zone. The outpost is little more than a cluster of prefab huts and rattling power generators struggling to stay upright. A weather-beaten marshal watches from a distance, hand resting on a sidearm out of habit, not fear.",
    "You touch down on a pad wedged between two massive freighters, both of them offloading cargo at a frantic pace. The shouts of merchants, the hum of machinery, and the hiss of coolant lines all merge into a relentless industrial rhythm. Workers weave between ships with the determination of ants defending a hive.",
    "Your landing gear clanks onto metal stained with oil, scorch marks, and a few things better left unexamined. Several tough-looking locals eye you from behind dark visors, whispering among themselves. You get the sense this is the sort of place where credits spend fast and lives end faster.",
    "Your ship descends onto a desolate pad surrounded by silent, darkened buildings. A single service droid rolls by on half-functioning wheels, sparking as it passes. The emptiness is thick enough to make you wonder whether you missed an evacuation notice.",
    "You glide through a canyon of glittering skyscrapers before settling onto a polished commercial landing deck. Advert screens flash nonstop around you, selling everything from starship parts to questionable pharmaceuticals. Crowds surge through walkways like you're landing in the beating heart of a galactic bazaar.",
    "Your ship hits down with a thud on a cracked, sunbaked landing slab surrounded by rusting cargo containers. A pair of smugglers argue loudly nearby, their weapons casually visible and their patience clearly not. The air smells like heat, old gunpowder, and deals made under duress.",
    ]
    
def landingPort():
    return textwrap.fill(random.choice(PORT_LANDING_TEXTS),width=80)
    
    