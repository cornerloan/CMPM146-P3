import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    if len(state.my_fleets()) >= 1:
        return False

    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        return False
    else:
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships // 2)


def spread_to_weakest_neutral_planet(state):
    if len(state.my_fleets()) >= 1:
        return False

    weakest_planets = sorted(state.neutral_planets(), key=lambda p: p.num_ships)[:5]
    strongest_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)[:3]

    if not strongest_planets or not weakest_planets:
        return False

    for target in weakest_planets:
        for source in strongest_planets:
            ships_to_send = source.num_ships // 5
            issue_order(state, source.ID, target.ID, ships_to_send)

    return True


def reinforce_planets(state):
    if len(state.my_fleets()) >= 1:
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
    if len(state.my_fleets()) >= 1:
        return False

    enemy_fleets = state.enemy_fleets()
    if not enemy_fleets:
        return False

    threatened_planets = {fleet.destination_planet: 0 for fleet in enemy_fleets}
    for fleet in enemy_fleets:
        threatened_planets[fleet.destination_planet] += fleet.num_ships

    weakest_planet = min(
        (planet for planet in state.my_planets() if planet.ID in threatened_planets),
        key=lambda p: p.num_ships - threatened_planets[p.ID],
        default=None
    )

    if not weakest_planet:
        return False

    strong_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)

    needed_ships = threatened_planets[weakest_planet.ID] - weakest_planet.num_ships + 1
    for strong_planet in strong_planets:
        if strong_planet.ID == weakest_planet.ID:
            continue
        ships_to_send = min(strong_planet.num_ships // 2, needed_ships)
        if ships_to_send > 0:
            issue_order(state, strong_planet.ID, weakest_planet.ID, ships_to_send)
            needed_ships -= ships_to_send
            if needed_ships <= 0:
                break

    return True


def coordinated_attack_strategy(state):
    strong_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)[:5]
    enemy_planets = sorted(state.enemy_planets(), key=lambda p: p.num_ships)

    if not strong_planets or not enemy_planets:
        return False

    for strong_planet in strong_planets:
        target = enemy_planets[0]
        ships_to_send = strong_planet.num_ships // 2
        issue_order(state, strong_planet.ID, target.ID, ships_to_send)

    return True


def coordinated_expansion_strategy(state):
    strong_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)[:5]
    neutral_planets = sorted(state.neutral_planets(), key=lambda p: p.num_ships)

    if not strong_planets or not neutral_planets:
        return False

    for strong_planet in strong_planets:
        target = neutral_planets[0]
        ships_to_send = strong_planet.num_ships // 2
        issue_order(state, strong_planet.ID, target.ID, ships_to_send)

    return True
