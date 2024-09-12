import GUI
import copy


class BallSortProblem:
    def __init__(self, tubes):
        self.tubes = tubes
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.tubes

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        for tube in state:
            if not (len(tube) == 0 or (len(tube) == 4 and len(set(tube)) == 1)):
                return False
        return True

    def move_between_tubes(self, state, tube1, tube2, t1_idx, t2_idx):
        """
        Thjis function try to move the top ball from t1 to t2 and return the new state
        :param tube1:
        :param tube2:
        :return:
        """
        if len(tube2) == 4 or (len(tube2) and tube1[-1] != tube2[-1]):
            return None
        post_tubes = copy.deepcopy(state)
        post_tubes[t2_idx].append(post_tubes[t1_idx].pop())
        return post_tubes

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        successors = []
        for t1_idx, tube1 in enumerate(state):
            if len(tube1) == 0:  # Skip empty tubes
                continue
            for t2_idx, tube2 in enumerate(state):
                if t1_idx != t2_idx:
                    suc = self.move_between_tubes(state, tube1, tube2, t1_idx, t2_idx)
                    if suc is not None:
                        successors.append((suc, f"{t1_idx}_to_{t2_idx}", 1))
        self.expanded += 1
        return successors

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


