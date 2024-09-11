import sys
import heuristic_search
from BallSortProblem import *
from BallSortGame import *
def play_a_star_search(game, problem):
    back_trace = heuristic_search.a_star_search(game.tubes, heuristic_search.heuristic_function)
    for action in back_trace:
        game.do_action(action)
    print("Expanded nodes: %d, score: %d" % (problem.expanded, game.get_steps()))


if __name__ == '__main__':
    # if len(sys.argv) != 2 and len(sys.argv) != 3:
    #     print("Usage: BallSortPuzzle.py agent/human search/planning")
    #     exit()
    # agent = False
    # if str(sys.argv[1]) == 'agent':
    #     agent = True
    #     if str(sys.argv[2]) == 'search':
    game = BallSortGame(agent="AI")
    # problem = BallSortProblem(game.tubes)
    # play_a_star_search(game, problem)
    # t1=Tubes([[1,2,3],[]])
    # t2=Tubes([[1, 2,3],[]])
    # d={t1: 1}
    # print(t2 in d)

