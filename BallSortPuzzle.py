import sys
import heuristic_search
from BallSortProblem import *
from BallSortGame import *
def play_a_star_search(game, problem):
    back_trace = heuristic_search.a_star_search(game.tubes, heuristic_search.heuristic_function(problem))
    game.run_actions(back_trace)
    print("Expanded nodes: %d, score: %d" % (problem.expanded, game.get_steps()))


if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: BallSortPuzzle.py agent/human search/planning")
        exit()
    agent = False
    if str(sys.argv[1]) == 'agent':
        agent = True
        if str(sys.argv[2]) == 'search':
            game = BallSortGame()
            problem = BallSortProblem(game.tubes)
            play_a_star_search(game, problem)

