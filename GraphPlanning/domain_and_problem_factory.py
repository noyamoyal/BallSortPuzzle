import itertools
import sys


def write_propositions(domain_file, colors, n_tubes):
    domain_file.write(f'Propositions:\n')
    balls_location = [f'{color}_{i}_{j}' for color in colors for i in range(1, n_tubes + 1) for j in range(1, 5)]
    tube_has = [f'{i}_has_{j}' for i in range(1, n_tubes + 1) for j in range(1, 5)]
    domain_file.write(" ".join(balls_location) + " ".join(tube_has))

def write_actions(domain_file, colors, n_tubes):
    domain_file.write(f"Actions:\n")
    # TODO remove finished from full tube
    for color in colors:
        for i in range(1, n_tubes + 1):
            for j in range(1, 5):
                for k in range(1, n_tubes + 1):
                    if i == k: continue
                    for l in range(1, 5):
                        name = f'Move_{color}_from_{i}_{j}_to_{k}_{l}'
                        pre = [f'{color}_{i}_{j}', f'{i}_has_{j}', f'{k}_has_{l-1}']
                        add = [f'{color}_{k}_{l}', f'{i}_has_{j-1}', f'{k}_has_{l}']
                        delete = [f'{color}_{i}_{j}', f'{i}_has_{j}', f'{k}_has_{l-1}']
                        if l!=1:
                            pre.append(f'{color}_{k}_{l-1}')
                        else:
                            delete.append(f'{k}_finished')
                        domain_file.write(f"Name: {name}\n")
                        domain_file.write("pre: " + " ".join(pre) + "\n")
                        domain_file.write("add: " + " ".join(add) + "\n")
                        domain_file.write("delete: " + " ".join(delete) + "\n")

        for color in colors:
            for i in range(1, n_tubes + 1):
                name = f'{i}_finished_with_{color}'
                pre = [f'{color}_{i}_{j}' for j in range(1, 5)]
                add = [f'{i}_finished']
                delete = []
                domain_file.write(f"Name: {name}\n")
                domain_file.write("pre: " + " ".join(pre) + "\n")
                domain_file.write("add: " + " ".join(add) + "\n")
                domain_file.write("delete: " + " ".join(delete) + "\n")

        for i in range(1, n_tubes + 1):
            name = f'{i}_finished_with_empty'
            pre = [f'{i}_has_0']
            add = [f'{i}_finished']
            delete = []
            domain_file.write(f"Name: {name}\n")
            domain_file.write("pre: " + " ".join(pre) + "\n")
            domain_file.write("add: " + " ".join(add) + "\n")
            domain_file.write("delete: " + " ".join(delete) + "\n")

def create_domain_file(domain_file_name, colors, n_tubes):
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    write_propositions(domain_file, colors, n_tubes)
    domain_file.write("\n")
    write_actions(domain_file, colors, n_tubes)
    domain_file.close()


def write_state(problem_file, disks, pegs, is_initial_state):
    if is_initial_state:
        problem_file.write(f'Initial state: ')
        clear_pegs = ['c_' + p for p in pegs[1:]]
    else:
        problem_file.write(f'Goal state: ')
    disks_on_disks = []
    for d1, d2 in itertools.combinations(disks, r=2):
        if int(d1.split("_")[1]) == int(d2.split("_")[1]) - 1:
            disks_on_disks.append(f'{d1}-ON-{d2}')
    problem_file.write(" ".join(disks_on_disks) + " ")
    if is_initial_state:
        problem_file.write(" ".join(clear_pegs) + " ")
        problem_file.write(f"d_{len(disks) - 1}-ON-p_0")
        problem_file.write(" c_d_0")
    else:
        problem_file.write(f"d_{len(disks) - 1}-ON-p_{len(pegs) - 1}")


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    write_state(problem_file, disks, pegs, True)
    problem_file.write("\n")
    write_state(problem_file, disks, pegs, False)
    problem_file.close()


# if __name__ == '__main__':
#     if len(sys.argv) != 3:
#         print('Usage: domain_and_problem_factory.py n m')
#         sys.exit(2)
#
#     n = int(float(sys.argv[1]))  # number of disks
#     m = int(float(sys.argv[2]))  # number of pegs
#
#     domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
#     problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)
#
#     create_domain_file(domain_file_name, n, m)
#     create_problem_file(problem_file_name, n, m)

if __name__ == '__main__':
    write_propositions("", ["red", "green", "blue"], 4)
