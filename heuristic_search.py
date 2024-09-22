from PriorityQueue import PriorityQueue

def a_star_search(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    queue = PriorityQueue()
    # Inserting starting point
    queue.push(problem.get_start_state(), heuristic(problem.get_start_state()))
    # Dictionary which holds the cost of the minimum cost from the beggining up to this point.
    reached_nodes = {problem.get_start_state(): 0}
    paths_actions = {}
    # List which will hold the path to solution
    path_to_goal = []
    goal = None

    while not queue.isEmpty():

        # Extracting current point and evaluate its cost from start.
        node = queue.pop()
        # print(problem.expanded)
        cost = reached_nodes[node]

        # If got to the goal point break.
        if problem.is_goal_state(node):
            goal = node
            break
        # Loop over node neighbors and add them to queue.
        for neighbor in problem.get_successors(node):
            if neighbor[0] not in reached_nodes:
                g_n = cost + neighbor[2]
                f_n = g_n + heuristic(neighbor[0])
                # Adding the cose to get to that neighbor from node.
                reached_nodes[neighbor[0]] = f_n
                # Adding the action from node to get to neighbor
                paths_actions[neighbor[0]] = (node, neighbor[1])
                # Add to priority queue the neighbor and the total cost to it from beginning.
                queue.push(neighbor[0], f_n)

    # Fetching path using our dictionary
    while goal != problem.get_start_state():
        # Take the action from last goal.
        path_to_goal.append(paths_actions[goal][1])
        # Change goal to point before goal.
        goal = paths_actions[goal][0]

    path_to_goal.reverse()
    return path_to_goal



def heuristic_function(board):
    return blocking_balls(board)


def misplaced_balls(board):
    """
    Heuristic function to estimate the cost of reaching the goal state.

    :param board: List of lists, where each inner list represents a tube with balls represented as color strings.
    :return: Estimated cost to reach the goal state (lower is better).
    """
    misplaced = 0
    for tube in board:
        if not tube:  # Skip empty tubes
            continue

        current_color = tube[0]
        for ball in tube:
            # Count balls that are misplaced
            if ball != current_color:
                misplaced += 1

            # Update current color to keep tracking only the top color correctly placed
            current_color = ball
    return misplaced


def grouped_ungrouped(board):
    """
    Heuristic function that counts grouped and ungrouped balls in each tube.

    :param board: List of lists, where each inner list represents a tube with balls represented as color strings.
    :return: Estimated cost to reach the goal state.
    """
    ungrouped_balls = 0

    for tube in board:
        if not tube:  # Skip empty tubes
            continue

        # Count the number of groups in the tube
        groups = 1
        for i in range(1, len(tube)):
            if tube[i] != tube[i - 1]:
                groups += 1

        # Ungrouped balls are those that belong to a new group
        ungrouped_balls += groups - 1

    return ungrouped_balls


def empty_tubes(board):
    """
    Heuristic function that takes into account the number of empty tubes.

    :param board: List of lists, where each inner list represents a tube with balls represented as color strings.
    :return: Estimated cost to reach the goal state.
    """
    empty_tubes = sum(1 for tube in board if not tube)

    misplaced_balls = 0
    for tube in board:
        if not tube:
            continue

        # Count misplaced balls
        current_color = tube[0]
        for ball in tube:
            if ball != current_color:
                misplaced_balls += 1
            current_color = ball
    # The more empty tubes, the lower the heuristic value since it makes rearranging easier
    return misplaced_balls - empty_tubes


def blocking_balls(board):
    """
    Heuristic function that counts blocking balls in each tube.

    :param board: List of lists, where each inner list represents a tube with balls represented as color strings.
    :return: Estimated cost to reach the goal state.
    """
    blocking_balls = 0

    for tube in board:
        if not tube:
            continue

        # Count blocking balls
        correct_color = tube[0]
        for i in range(1, len(tube)):
            if tube[i] != correct_color:
                blocking_balls += 1
                break  # Count only first blocker per tube for simplicity

    return blocking_balls


def color_mismatch_penalty(board):
    """
    Heuristic function that penalizes mismatched colors within tubes, with heavier penalties for deeper mismatches.

    :param board: List of lists, where each inner list represents a tube with balls represented as color strings.
    :return: Estimated cost to reach the goal state.
    """
    mismatch_penalty = 0

    for tube in board:
        if not tube:
            continue

        correct_color = tube[0]
        for i, ball in enumerate(tube):
            if ball != correct_color:
                # Penalize deeper mismatches more
                mismatch_penalty += (i + 1)
                correct_color = ball  # Update expected color after mismatch

    return mismatch_penalty
