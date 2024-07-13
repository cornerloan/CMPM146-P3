#!/usr/bin/env python

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# Set up the behavior tree with different strategies for early, mid, and late game
def setup_behavior_tree():
    root = Selector(name='High Level Ordering of Strategies')

    # Early Game Strategy
    early_game = Sequence(name='Early Game Strategy')
    early_game_check = Check(is_early_game)
    early_game_action = Action(spread_to_weakest_neutral_planet)
    early_game.child_nodes = [early_game_check, early_game_action]

    # Mid Game Strategy
    mid_game = Sequence(name='Mid Game Strategy')
    mid_game_check = Check(is_mid_game)
    mid_game_action = Action(attack_weakest_enemy_planet)
    mid_game.child_nodes = [mid_game_check, mid_game_action]

    # Late Game Strategy
    late_game = Sequence(name='Late Game Strategy')
    late_game_check = Check(is_late_game)
    late_game_action = Action(attack_strongest_enemy_planet)
    late_game.child_nodes = [late_game_check, late_game_action]

    # Reinforcement strategy
    reinforce = Action(reinforce_planets)

    # Top-level root node
    root.child_nodes = [early_game, mid_game, late_game, reinforce]

    logging.info('\n' + root.tree_to_string())
    return root

def do_turn(state):
    behavior_tree.execute(state)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
