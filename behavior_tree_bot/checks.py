def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


def is_early_game(state):
    return sum(planet.num_ships for planet in state.my_planets()) < 50


def is_mid_game(state):
    return 50 <= sum(planet.num_ships for planet in state.my_planets()) < 200


def is_late_game(state):
    return sum(planet.num_ships for planet in state.my_planets()) >= 200
