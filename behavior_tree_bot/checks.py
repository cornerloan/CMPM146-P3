num_my_planets = 2

def check_early_game(state):
    return len(state.my_planets()) <= num_my_planets and len(state.my_fleets()) < 6

def check_mid_game(state):
    return len(state.my_planets()) > num_my_planets and len(state.my_fleets()) < 25

def check_late_game(state):
    return len(state.my_planets()) >= num_my_planets and len(state.enemy_planets()) <= 2
