import itertools
import sys


def write_propositions(domain_file, colors, n_tubes):
    """
    Writes the propositions for the domain file, which represent the possible states of the puzzle.

    Parameters:
    domain_file (file object): The file object to write the propositions to.
    colors (list): List of colors used in the puzzle.
    n_tubes (int): Number of tubes in the puzzle.

    Returns:
    None
    """
    domain_file.write(f'Propositions:\n')
    balls_location = [f'{color}_{i}_{j}' for color in colors for i in range(1, n_tubes + 1) for j in range(1, 5)]
    tube_has = [f'{i}_has_{j}' for i in range(1, n_tubes + 1) for j in range(0, 5)]
    finished_tubes = [f'{i}_finished' for i in range(1, n_tubes + 1)]
    domain_file.write(" ".join(balls_location) + " " + " ".join(tube_has) + " " + " ".join(finished_tubes))


def write_actions(domain_file, colors, n_tubes):
    """
    Writes the actions for the domain file, which define the possible moves and states of the tubes.

    Parameters:
    domain_file (file object): The file object to write the actions to.
    colors (list): List of colors used in the puzzle.
    n_tubes (int): Number of tubes in the puzzle.

    Returns:
    None
    """
    domain_file.write(f"Actions:\n")
    create_general_action(colors, domain_file, n_tubes)
    create_full_tube_action(colors, domain_file, n_tubes)
    create_empty_tube_action(domain_file, n_tubes)


def create_general_action(colors, domain_file, n_tubes):
    """
    Creates the general move actions for transferring balls between tubes.

    Parameters:
    colors (list): List of colors used in the puzzle.
    domain_file (file object): The file object to write the actions to.
    n_tubes (int): Number of tubes in the puzzle.

    Returns:
    None
    """
    for color in colors:
        for i in range(1, n_tubes + 1):
            for j in range(1, 5):
                for k in range(1, n_tubes + 1):
                    if i == k:
                        continue
                    for l in range(1, 5):
                        name = f'Move_{color}_from_{i}_{j}_to_{k}_{l}'
                        pre = [f'{color}_{i}_{j}', f'{i}_has_{j}', f'{k}_has_{l - 1}']
                        add = [f'{color}_{k}_{l}', f'{i}_has_{j - 1}', f'{k}_has_{l}']
                        delete = [f'{color}_{i}_{j}', f'{i}_has_{j}', f'{k}_has_{l - 1}']
                        if l != 1:
                            pre.append(f'{color}_{k}_{l - 1}')
                        else:
                            delete.append(f'{k}_finished')
                        write_to_domain_file(add, delete, domain_file, name, pre)


def create_full_tube_action(colors, domain_file, n_tubes):
    """
    Creates actions for identifying when a tube is full of the same color.

    Parameters:
    colors (list): List of colors used in the puzzle.
    domain_file (file object): The file object to write the actions to.
    n_tubes (int): Number of tubes in the puzzle.

    Returns:
    None
    """
    for color in colors:
        for i in range(1, n_tubes + 1):
            name = f'{i}_finished_with_{color}'
            pre = [f'{color}_{i}_{j}' for j in range(1, 5)]
            add = [f'{i}_finished']
            delete = []
            write_to_domain_file(add, delete, domain_file, name, pre)


def create_empty_tube_action(domain_file, n_tubes):
    """
    Creates actions for identifying when a tube is empty.

    Parameters:
    domain_file (file object): The file object to write the actions to.
    n_tubes (int): Number of tubes in the puzzle.

    Returns:
    None
    """
    for i in range(1, n_tubes + 1):
        name = f'{i}_finished_with_empty'
        pre = [f'{i}_has_0']
        add = [f'{i}_finished']
        delete = []
        write_to_domain_file(add, delete, domain_file, name, pre)


def write_to_domain_file(add, delete, domain_file, name, pre):
    """
    Writes an individual action to the domain file, including its preconditions, add effects, and delete effects.

    Parameters:
    add (list): List of propositions that are added as effects of the action.
    delete (list): List of propositions that are deleted as effects of the action.
    domain_file (file object): The file object to write the action to.
    name (str): The name of the action.
    pre (list): List of preconditions for the action.

    Returns:
    None
    """
    domain_file.write(f"Name: {name}\n")
    domain_file.write("pre: " + " ".join(pre) + "\n")
    domain_file.write("add: " + " ".join(add) + "\n")
    domain_file.write("delete: " + " ".join(delete) + "\n")


def create_domain_file(domain_file_name, colors, n_tubes):
    """
    Creates a domain file that defines the propositions and actions for the ball sort puzzle.

    Parameters:
    domain_file_name (str): The name of the domain file to be created.
    colors (list): List of colors used in the puzzle.
    n_tubes (int): Number of tubes in the puzzle.

    Returns:
    None
    """
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    write_propositions(domain_file, colors, n_tubes)
    domain_file.write("\n")
    write_actions(domain_file, colors, n_tubes)
    domain_file.close()


def create_problem_file(problem_file_name_, tubes):
    """
    Creates a problem file that defines the initial state and goal state of the ball sort puzzle.

    Parameters:
    problem_file_name_ (str): The name of the problem file to be created.
    tubes (list): A list of tubes where each tube is a list representing the initial ball configuration.

    Returns:
    None
    """
    problem_file = open(problem_file_name_, 'w')
    initial_balls_state = [f'{tubes[i][j]}_{i + 1}_{j + 1}' for i in range(len(tubes)) for j in range(len(tubes[i]))]
    initial_tubes_state = [f'{i + 1}_has_{len(tubes[i])}' for i in range(len(tubes))]
    goal_state = [f'{i}_finished' for i in range(1, len(tubes) + 1)]
    problem_file.write('Initial state: ' + " ".join(initial_balls_state) + " " + " ".join(initial_tubes_state) + "\n")
    problem_file.write('Goal state: ' + " ".join(goal_state) + "\n")
    problem_file.close()


def create_graph_plan_files(tubes, colors):
    """
    Creates the domain and problem files for the ball sort puzzle, which are used in Graph Planning.

    Parameters:
    tubes (list): A list of tubes where each tube is a list representing the initial ball configuration.
    colors (list): List of colors used in the puzzle.

    Returns:
    tuple: The names of the created domain and problem files.
    """
    domain_file_name = f'ball_sort_puzzle_{len(colors)}_domain.txt'
    problem_file_name = f'ball_sort_puzzle_{len(colors)}_problem.txt'
    # create_domain_file(domain_file_name, colors, len(tubes)) # Unmarked for creating new domain file
    create_problem_file(problem_file_name, tubes)
    return domain_file_name, problem_file_name