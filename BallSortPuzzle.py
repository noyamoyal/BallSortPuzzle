import sys
import heuristic_search
from BallSortGame import *
from GraphPlanning.domain_and_problem_factory import create_graph_plan_files
from GraphPlanning.planning_problem import PlanningProblem, level_sum, max_level
from GraphPlanning.search import *

# Constants to represent different agents and solving methods
HUMAN = "human"
AI = "AI"
GRAPHPLAN = "graph_plan"
SEARCH = "search"
PLANNING = "planning"


def play_a_star_search(game, problem):
    """
    Solves the BallSort puzzle using the A* search algorithm.

    Parameters:
    game (BallSortGame): The current state of the BallSort game.
    problem (BallSortProblem): The BallSort problem representation for the A* search.

    Returns:
    tuple: Expanded nodes and the number of steps taken by the solution.
    """
    actions = heuristic_search.a_star_search(problem, heuristic_search.heuristic_function)
    game.game_runner(actions=actions)
    print("Expanded nodes: %d, score: %d" % (problem.expanded, game.get_steps()))
    return problem.expanded, game.get_steps()


def play_graph_planning(game):
    """
    Solves the BallSort puzzle using Graph Planning.

    Parameters:
    game (BallSortGame): The current state of the BallSort game.

    Returns:
    tuple: Expanded nodes and the number of steps taken by the solution.
    """
    domain, problem = create_graph_plan_files(game.get_tubes(), game.get_colors())
    prob = PlanningProblem(domain, problem)
    start = time.perf_counter()

    plan = a_star_search(prob, level_sum)
    elapsed = time.perf_counter() - start
    if plan is not None:

        custom_plan = [f'{p.name[-10]}_to_{p.name[-3]}' for p in plan if p.name.split('_')[1] != "finished"]
        game.game_runner(actions=custom_plan)
        print("Plan found with %d actions in %.2f seconds" % (len(custom_plan), elapsed))
        print([plane_ for plane_ in custom_plan])
    else:
        print("Could not find a plan in %.2f seconds" % elapsed)
    print("Search nodes expanded: %d" % prob.expanded)
    return prob.expanded, game.get_steps()


def main():
    """
    Main function to run the BallSort game and solve it either with AI (A* or Graph Planning) or by a human player.
    """
    n_colors, agent, solve_plan = check_input_validity()
    n_games = 1
    expands, steps = 0, 0

    for i in range(n_games):
        game = BallSortGame(agent=agent, n_colors=n_colors)
        game_tube = game.get_tubes()
        if solve_plan:
            if solve_plan == SEARCH:
                cur_expand, cur_steps = play_a_star_search(game, BallSortProblem(game_tube))
            else:
                cur_expand, cur_steps = play_graph_planning(game)
            expands += cur_expand
            steps += cur_steps
        else:
            game.game_runner()
    # if solve_plan:
    #
        # with open("results/summary.txt", 'a') as file:
        #     file.write(f"\nfor agent : {solve_plan}\n"
        #                f"with n_colors : {n_colors}\n"
        #                f"num of games : {n_games}\n"
        #                f"average Expanded nodes : %d, average steps : %d\nusing :\n"
        #                f"######\n" % (expands / n_games, steps / n_games))
        #

def check_input_validity():
    """
    Validates the input arguments provided for the BallSort game.

    Parameters:
    None

    Returns:
    tuple: (n_colors, agent, solve_plan) where:
        - n_colors (int): The number of colors for the puzzle.
        - agent (str): The type of player (human/ai).
        - solve_plan (str or None): The solving method ('search' or 'planning'), or None if human.
    """
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: BallSortPuzzle.py n_color agent/human search/planning")
        exit(1)

    n_colors = int(sys.argv[1])
    if n_colors < 2 or n_colors > 9:
        print("ERROR: number of colors must be between 2 to 9 colors")
        exit(1)
    agent = sys.argv[2]
    if agent == 'ai':

        if sys.argv[3] == 'search':
            return n_colors, AI, SEARCH
        elif sys.argv[3] == 'planning':
            return n_colors, AI, PLANNING
        else:
            print("Usage: agent can be only one of the following: search/planning")
            exit(1)
    elif agent == "human":
        return n_colors, HUMAN, None
    else:
        print("Usage: agent can be only one of the following:  ai/human")
        exit(1)


if __name__ == '__main__':
    main()
