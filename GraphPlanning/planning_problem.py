import math

# from util import Pair
import copy
from GraphPlanning.proposition_layer import PropositionLayer
from GraphPlanning.plan_graph_level import PlanGraphLevel
from GraphPlanning.pgparser import PgParser
from GraphPlanning.action import Action

try:
    from GraphPlanning.search import SearchProblem
    from GraphPlanning.search import a_star_search

except:
    try:
        from CPF.search import SearchProblem
        from CPF.search import a_star_search
    except:
        from CPF.search_win_34 import SearchProblem
        from CPF.search_win_34 import a_star_search


class PlanningProblem:
    def __init__(self, domain_file, problem_file):
        """
        Constructor
        """
        p = PgParser(domain_file, problem_file)
        self.actions, self.propositions = p.parse_actions_and_propositions()
        self.actions_dict = {action.name: action for action in self.actions}
        # list of all the actions and list of all the propositions

        initial_state, goal = p.parse_problem()
        # the initial state and the goal state are lists of propositions

        self.initialState = frozenset(initial_state)
        self.goal = frozenset(goal)

        self.create_noops()
        # creates noOps that are used to propagate existing propositions from one layer to the next

        PlanGraphLevel.set_actions(self.actions)
        PlanGraphLevel.set_props(self.propositions)
        self.expanded = 0

    def get_start_state(self):
        return self.initialState

    def is_goal_state(self, state):
        """
        Hint: you might want to take a look at goal_state_not_in_prop_payer function
        """
        return not self.goal_state_not_in_prop_layer(state)

    def get_successors(self, state):
        """
        For a given state, this should return a list of triples,
        (successor, action, step_cost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'step_cost' is the incremental
        cost of expanding to that successor, 1 in our case.
        You might want to this function:
        For a list / set of propositions l and action a,
        a.all_preconds_in_list(l) returns true if the preconditions of a are in l

        Note that a state *must* be hashable!! Therefore, you might want to represent a state as a frozenset
        """
        colors = set()
        top_idx_for_tube = {}
        ball_ind = {}
        for s in state:
            segments = s.name.split('_')
            if len(segments) != 3: continue
            if segments[1] == 'has':
                top_idx_for_tube[int(segments[0])] = int(segments[2])
            else:
                ball_ind[(int(segments[1]), int(segments[2]))] = segments[0]
                colors.add(segments[0])
        self.expanded += 1
        successor_list = []
        # actions = [f'Move_{tube[len(tube) - 1]}_from_{i}_{j}_to_{k}_{l}' for tube in state]
        actions = [f'Move_{color}_from_{i}_{top_idx_for_tube[i]}_to_{k}_{top_idx_for_tube[k] + 1}' for color in colors
                   for i in range(1, len(top_idx_for_tube) + 1) for k in range(1, len(top_idx_for_tube) + 1)
                   if i != k and top_idx_for_tube[i] > 0 and top_idx_for_tube[k] < 4
                   and ball_ind[(i, top_idx_for_tube[i])] == color]
        noop_actions_full = [f'{i}_finished_with_{color}' for color in colors for i in range(1, len(top_idx_for_tube) + 1)]
        noop_actions_empty = [f'{i}_finished_with_empty' for i in range(1, len(top_idx_for_tube) + 1)]
        actions += noop_actions_full + noop_actions_empty

        for action in actions:
            action_obj = self.actions_dict[action]
            if not action_obj.is_noop() and action_obj.all_preconds_in_list(state):
                successor = list(state) + [prop for prop in action_obj.get_add() if prop not in state]

                successor = [prop for prop in successor if prop not in action_obj.get_delete()]
                # successor_prop = state_prop_lst + action.get_add()
                successor = frozenset(successor)
                successor_list.append((successor, action_obj, 1))

        return successor_list

    @staticmethod
    def get_cost_of_actions(actions):
        return len(actions)

    def goal_state_not_in_prop_layer(self, propositions):
        """
        Helper function that receives a  list of propositions (propositions) and returns true
        if not all the goal propositions are in that list
        """
        for goal in self.goal:
            if goal not in propositions:
                return True
        return False

    def create_noops(self):
        """
        Creates the noOps that are used to propagate propositions from one layer to the next
        """
        for prop in self.propositions:
            name = prop.name
            precon = []
            add = []
            precon.append(prop)
            add.append(prop)
            delete = []
            act = Action(name, precon, add, delete, True)
            self.actions.append(act)


def max_level(state, planning_problem):
    """
    The heuristic value is the number of layers required to expand all goal propositions.
    If the goal is not reachable from the state your heuristic should return float('inf')
    A good place to start would be:
    prop_layer_init = PropositionLayer()          #create a new proposition layer
    for prop in state:
        prop_layer_init.add_proposition(prop)        #update the proposition layer with the propositions of the state
    pg_init = PlanGraphLevel()                   #create a new plan graph level (level is the action layer and the propositions layer)
    pg_init.set_proposition_layer(prop_layer_init)   #update the new plan graph level with the the proposition layer
    """
    prop_layer_init = PropositionLayer()  # create a new proposition layer
    for prop in state:
        prop_layer_init.add_proposition(prop)  # update the proposition layer with the propositions of the state
    pg_init = PlanGraphLevel()  # create a new plan graph level (level is the action layer and the propositions layer)
    pg_init.set_proposition_layer(prop_layer_init)
    max_cur_level = 0
    graph_plan = [pg_init]
    # While goal state is not in proposition layer, keep expanding
    while not planning_problem.is_goal_state(graph_plan[max_cur_level].get_proposition_layer().get_propositions()):
        # If the graph has not changed between expansions, we should halt
        if is_fixed(graph_plan, max_cur_level):
            return float('inf')
        max_cur_level += 1
        pgNext = PlanGraphLevel()
        # Expand without mutex (relaxed version of problem)
        pgNext.expand_without_mutex(graph_plan[max_cur_level - 1])
        graph_plan.append(pgNext)
    return max_cur_level



def level_sum(state, planning_problem):
    """
    The heuristic value is the sum of sub-goals level they first appeared.
    If the goal is not reachable from the state your heuristic should return float('inf')
    """
    prop_layer_init = PropositionLayer()  # create a new proposition layer
    for prop in state:
        prop_layer_init.add_proposition(prop)  # update the proposition layer with the propositions of the state
    pg_init = PlanGraphLevel()  # create a new plan graph level (level is the action layer and the propositions layer)
    pg_init.set_proposition_layer(prop_layer_init)
    max_cur_level = 0
    level_sum_result = 0
    sub_goal_appeared = set()
    graph_plan = [pg_init]
    for prop in graph_plan[max_cur_level].get_proposition_layer().get_propositions():
        if prop in planning_problem.goal and prop not in sub_goal_appeared:
            sub_goal_appeared.add(prop)
    # While goal state is not in proposition layer, keep expanding
    while not planning_problem.is_goal_state(graph_plan[max_cur_level].get_proposition_layer().get_propositions()):
        # If the graph has not changed between expansions, we should halt
        if is_fixed(graph_plan, max_cur_level):
            return float('inf')
        max_cur_level += 1
        pgNext = PlanGraphLevel()
        # Expand without mutex (relaxed version of problem)
        pgNext.expand_without_mutex(graph_plan[max_cur_level - 1])
        graph_plan.append(pgNext)
        for prop in graph_plan[max_cur_level].get_proposition_layer().get_propositions():
            if prop in planning_problem.goal and prop not in sub_goal_appeared:
                level_sum_result += max_cur_level
                sub_goal_appeared.add(prop)
    return level_sum_result


def is_fixed(graph, level):
    """
    Checks if we have reached a fixed point,
    i.e. each level we'll expand would be the same, thus no point in continuing
    """
    if level == 0:
        return False
    return len(graph[level].get_proposition_layer().get_propositions()) == len(
        graph[level - 1].get_proposition_layer().get_propositions())


def null_heuristic(*args, **kwargs):
    return 0


# if __name__ == '__main__':
#     import sys
#     import time
#
#     if len(sys.argv) != 1 and len(sys.argv) != 4:
#         print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
#         exit()
#     # domain = 'dwrDomain.txt'
#     # problem = 'dwrProblem.txt'
#     domain = 'hanoi_tower_problem_domains/hanoi_2_3_domain.txt'
#     problem = 'hanoi_tower_problem_domains/hanoi_2_3_problem.txt'
#     heuristic = null_heuristic
#     if len(sys.argv) == 4:
#         domain = str(sys.argv[1])
#         problem = str(sys.argv[2])
#         if str(sys.argv[3]) == 'max':
#             heuristic = max_level
#         elif str(sys.argv[3]) == 'sum':
#             heuristic = level_sum
#         elif str(sys.argv[3]) == 'zero':
#             heuristic = null_heuristic
#         else:
#             print("Usage: planning_problem.py domain_name problem_name heuristic_name[max, sum, zero]")
#             exit()
#     domain = 'hanoi_tower_problem_domains/hanoi_2_3_domain.txt'
#     problem = 'hanoi_tower_problem_domains/hanoi_2_3_problem.txt'
#     prob = PlanningProblem(domain, problem)
#     start = time.perf_counter()
#     plan = a_star_search(prob, heuristic)
#     elapsed = time.perf_counter() - start
#     if plan is not None:
#         print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
#         print([plane_.name for plane_ in plan])
#     else:
#         print("Could not find a plan in %.2f seconds" % elapsed)
#     print("Search nodes expanded: %d" % prob.expanded)
