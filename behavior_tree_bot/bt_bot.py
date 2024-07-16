#!/usr/bin/env python

import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


def setup_behavior_tree():
    root = Selector(name='High Level Strategy')

    early_game_strategy = Sequence(name='Early Game Strategy')
    is_early_game = Check(check_early_game)
    spread_action = Action(mass_expansion)
    early_game_strategy.child_nodes = [is_early_game, spread_action]

    mid_game_strategy = Sequence(name='Mid Game Strategy')
    is_mid_game = Check(check_mid_game)
    coordinated_expansion = Action(coordinated_expansion_strategy)
    reinforce_action = Action(reinforce_weakest_planet)
    mid_game_strategy.child_nodes = [is_mid_game, coordinated_expansion, reinforce_action]

    late_game_strategy = Sequence(name='Late Game Strategy')
    is_late_game = Check(check_late_game)
    coordinated_attack = Action(coordinated_attack_strategy)
    consolidate_action = Action(reinforce_weakest_planet)
    late_game_strategy.child_nodes = [is_late_game, coordinated_attack, consolidate_action]

    root.child_nodes = [early_game_strategy, mid_game_strategy, late_game_strategy, Action(attack_weakest_enemy_planet)]

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
