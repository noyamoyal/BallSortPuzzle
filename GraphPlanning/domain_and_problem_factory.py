import itertools
import sys


def proposition_string_template(param):
    pass


def write_propositions(domain_file, disks, pegs):
    domain_file.write(f'Propositions:\n')
    clear_disks = ['c_' + d for d in disks]
    clear_pegs = ['c_' + p for p in pegs]
    disks_on_disks = [f'{d1}-ON-{d2}' for d1, d2 in itertools.combinations(disks, r=2)]
    disks_on_pegs = [f'{d}-ON-{p}' for d, p in itertools.product(disks, pegs)]
    domain_file.write(" ".join(clear_pegs) + " ")
    domain_file.write(" ".join(clear_disks) + " ")
    domain_file.write(" ".join(disks_on_pegs) + " ")
    domain_file.write(" ".join(disks_on_disks))


def write_action(domain_file, disk, src, dest):
    name = f'Move-{disk}-to-{dest}-from-{src}'
    pre = ['c_' + disk, 'c_' + dest, f'{disk}-ON-{src}']
    add = [f'{disk}-ON-{dest}', f'c_{src}']
    delete = ['c_' + dest, f'{disk}-ON-{src}']
    domain_file.write(f"Name: {name}\n")
    domain_file.write("pre: " + " ".join(pre) + "\n")
    domain_file.write("add: " + " ".join(add) + "\n")
    domain_file.write("delete: " + " ".join(delete) + "\n")


def write_actions(domain_file, disks, pegs):
    domain_file.write("Actions:\n")
    move_disk_between_disks(disks, domain_file)
    move_disk_between_pegs(disks, domain_file, pegs)
    move_disk_between_peg_and_disk(disks, domain_file, pegs)


def move_disk_between_peg_and_disk(disks, domain_file, pegs):
    for disk_to_move in disks:
        for disk, peg in itertools.product(disks, pegs):
            if int(disk_to_move.split("_")[1]) < int(disk.split("_")[1]):
                write_action(domain_file, disk_to_move, peg, disk)
                write_action(domain_file, disk_to_move, disk, peg)


def move_disk_between_pegs(disks, domain_file, pegs):
    for disk in disks:
        for p1, p2 in itertools.combinations(pegs, r=2):
            write_action(domain_file, disk, p1, p2)
            write_action(domain_file, disk, p2, p1)


def move_disk_between_disks(disks, domain_file):
    for disk, disk1, disk2 in itertools.combinations(disks, r=3):
        write_action(domain_file, disk, disk1, disk2)
        write_action(domain_file, disk, disk2, disk1)


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    write_propositions(domain_file, disks, pegs)
    domain_file.write("\n")
    write_actions(domain_file, disks, pegs)
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
