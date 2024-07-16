def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def check_early_game(state):
    return len(state.my_planets()) <= 2 and len(state.my_fleets()) == 0

def check_mid_game(state):
    return len(state.my_planets()) > 2 and len(state.my_fleets()) < 5

def check_late_game(state):
    return len(state.my_planets()) > 5 and len(state.enemy_planets()) <= 2
