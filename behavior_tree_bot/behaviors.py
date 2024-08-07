import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

max_fleets_to_send = 30

def attack_weakest_enemy_planet(state):
    if len(state.my_fleets()) >= max_fleets_to_send:
        return False

    #get my strongest planet, and the opponent's weakest planet
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    #check if they exist
    if not strongest_planet or not weakest_planet:
        return False
    else:
        #send half the ships form my planet to attack
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships // 2)


def mass_expansion(state):
    if len(state.my_fleets()) >= max_fleets_to_send:
        return False

    #determine the 5 weakest neutral planets and my 3 strongest planets
    weakest_planets = sorted(state.neutral_planets(), key=lambda p: p.num_ships)[:5]
    strongest_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)[:3]

    #check if they exist
    if not strongest_planets or not weakest_planets:
        return False

    #mass spread ships from my strongest planets to the weakest planets
    #each strongest planet sends 20% of it's troops
    for target in weakest_planets:
        for source in strongest_planets:
            ships_to_send = source.num_ships // 5
            issue_order(state, source.ID, target.ID, ships_to_send)

    return True


def reinforce_planets(state):
    if len(state.my_fleets()) >= max_fleets_to_send:
        return False

    enemy_fleets = state.enemy_fleets()
    if not enemy_fleets:
        return False

    # Find the planets that are being targeted by enemy fleets
    threatened_planets = {fleet.destination_planet: 0 for fleet in enemy_fleets}
    for fleet in enemy_fleets:
        threatened_planets[fleet.destination_planet] += fleet.num_ships

    my_threatened_planets = [planet for planet in state.my_planets() if planet.ID in threatened_planets]

    if not my_threatened_planets:
        return False

    # Reinforce each threatened planet from multiple strong planets
    for threatened_planet in my_threatened_planets:
        needed_ships = threatened_planets[threatened_planet.ID] - threatened_planet.num_ships + 1
        strong_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
        
        for strong_planet in strong_planets:
            if strong_planet.ID == threatened_planet.ID:
                continue
            ships_to_send = min(strong_planet.num_ships // 2, needed_ships)
            if ships_to_send > 0:
                issue_order(state, strong_planet.ID, threatened_planet.ID, ships_to_send)
                needed_ships -= ships_to_send
                if needed_ships <= 0:
                    break

    return True


def reinforce_weakest_planet(state):
    if len(state.my_fleets()) >= max_fleets_to_send:
        return False

    #check if there are any enemy fleets currently deployed
    enemy_fleets = state.enemy_fleets()
    if not enemy_fleets:
        return False

    #get a list of planets that have enemy ships headed towards them
    threatened_planets = {fleet.destination_planet: 0 for fleet in enemy_fleets}
    for fleet in enemy_fleets:
        threatened_planets[fleet.destination_planet] += fleet.num_ships

    #determine my weakest planet using the threatened_planets list
    weakest_planet = min(
        (planet for planet in state.my_planets() if planet.ID in threatened_planets),
        key=lambda p: p.num_ships - threatened_planets[p.ID],
        default=None
    )

    if not weakest_planet:
        return False

    #get my planets sorted strongest first, and determine how many ships are needed to defend the weakest planet
    strong_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    needed_ships = threatened_planets[weakest_planet.ID] - weakest_planet.num_ships + 1

    for strong_planet in strong_planets:
        #if current planet is the weakest planet, skip this iteration
        if strong_planet.ID == weakest_planet.ID:
            continue

        #get a safe number (max of half the ships on this planet) to send to my threatened planet
        ships_to_send = min(strong_planet.num_ships // 2, needed_ships)
        if ships_to_send > 0:
            issue_order(state, strong_planet.ID, weakest_planet.ID, ships_to_send)
            needed_ships -= ships_to_send
            if needed_ships <= 0:
                break

    return True


def coordinated_attack_strategy(state):
    #get my strongest 5 planets, and the weakest enemy planet
    strong_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)[:3]
    enemy_planets = sorted(state.enemy_planets(), key=lambda p: p.num_ships)

    #check if they exist
    if not strong_planets or not enemy_planets:
        return False

    #make each one of my strongest planets send half their ships to attack the weakest planet
    for strong_planet in strong_planets:
        target = enemy_planets[0]
        ships_to_send = strong_planet.num_ships // 2
        issue_order(state, strong_planet.ID, target.ID, ships_to_send)

    return True


def coordinated_expansion_strategy(state):
    #get my strongest 5 planets, and weakest neutral planet
    strong_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)[:5]
    neutral_planets = sorted(state.neutral_planets(), key=lambda p: p.num_ships)

    #check if they exist
    if not strong_planets or not neutral_planets:
        return False

    #send half the ships from each of my strongest planets to this neutral planet
    for strong_planet in strong_planets:
        target = neutral_planets[0]
        ships_to_send = strong_planet.num_ships // 2
        issue_order(state, strong_planet.ID, target.ID, ships_to_send)

    return True
