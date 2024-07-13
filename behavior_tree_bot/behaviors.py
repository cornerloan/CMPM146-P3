import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_weakest_enemy_planet(state):
    if len(state.my_fleets()) >= 2:  # Allow multiple fleets to be sent
        return False

    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        return False
    else:
        # Send two fleets, each with half the ships from the strongest planet
        ships_to_send = strongest_planet.num_ships // 2
        result1 = issue_order(state, strongest_planet.ID, weakest_planet.ID, ships_to_send)
        result2 = issue_order(state, strongest_planet.ID, weakest_planet.ID, ships_to_send)
        return result1 and result2  # Both orders must succeed for action to succeed


def spread_to_weakest_neutral_planet(state):
    if len(state.my_fleets()) >= 2:  # Allow multiple fleets to be sent
        return False

    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        return False
    else:
        # Send two fleets, each with half the ships from the strongest planet
        ships_to_send = strongest_planet.num_ships // 2
        result1 = issue_order(state, strongest_planet.ID, weakest_planet.ID, ships_to_send)
        result2 = issue_order(state, strongest_planet.ID, weakest_planet.ID, ships_to_send)
        return result1 and result2  # Both orders must succeed for action to succeed


def attack_strongest_enemy_planet(state):
    if len(state.my_fleets()) >= 2:  # Allow multiple fleets to be sent
        return False

    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    strongest_enemy_planet = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not strongest_enemy_planet:
        return False
    else:
        # Send two fleets, each with half the ships from the strongest planet
        ships_to_send = strongest_planet.num_ships // 2
        result1 = issue_order(state, strongest_planet.ID, strongest_enemy_planet.ID, ships_to_send)
        result2 = issue_order(state, strongest_planet.ID, strongest_enemy_planet.ID, ships_to_send)
        return result1 and result2  # Both orders must succeed for action to succeed


def reinforce_planets(state):
    if len(state.my_fleets()) >= 2:  # Allow multiple fleets to be sent
        return False

    my_planets = state.my_planets()
    if not my_planets:
        return False

    strongest_planet = max(my_planets, key=lambda p: p.num_ships)
    
