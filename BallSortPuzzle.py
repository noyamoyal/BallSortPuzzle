import sys

from BallSortGame import *

HUMAN = "human"
AI = "AI"
GRAPHPLAN = "graph_plan"
SEARCH = "search"
PLANNING = "planning"


def play_a_star_search(game, problem):
    actions = heuristic_search.a_star_search(problem, heuristic_search.heuristic_function)
    game.game_runner(actions=actions)
    print("Expanded nodes: %d, score: %d" % (problem.expanded, game.get_steps()))
    return problem.expanded, game.get_steps()


def main():
    n_colors, agent, solve_plan = check_input_validity()
    n_games = 2
    expands, steps = 0, 0

    for i in range(n_games):

        game = BallSortGame(agent=agent, n_colors=n_colors)
        game_tube = game.get_tubes()
        if solve_plan:
            if solve_plan == SEARCH:
                cur_expand, cur_steps = play_a_star_search(game, BallSortProblem(game_tube))
            else:
                pass
            expands += cur_expand
            steps += cur_steps
            with open("results/summary.txt", 'a') as file:
                file.write(f"\nfor agent :AI\n"
                           f"with n_colors:{n_colors}\n"
                           f"num of games : {n_games}\n"
                           f"average Expanded nodes: %d, average steps: %d\nusing:\n"
                           f"######\n" % (expands / n_games, steps / n_games))

        else:
            game.game_runner()
        # cur_expand, cur_steps = game.game_runner()


def check_input_validity():
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


