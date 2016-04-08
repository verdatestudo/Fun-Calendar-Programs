'''
Pool Cues - Calendar Problem Solver
First Created: 2016-Mar-15
Last Updated: 2016-Apr-08
Python 2.7
Chris

See poolcues.png
answer = 4, 7, 2, 11, 9, 3, 5, 10, 1, 12, 8, 6, 15, 13, 14
'''

def calc_child_from_parents(node_list, remaining_nums, node_parents):
    '''
    This function looks at the list of possible values for the two parents of a node.
    It looks at all possible parent1 + parent2 combinations.
    And if the resulting combination is in remaining_nums and in current possible values for the node (child), it keeps that combination.
    '''

    for idx, node in enumerate(node_parents):
        print idx, node
        if node != [] and len(node_list[idx]) > 1:
            temp_node_list = node_list[idx]
            node_list[idx] = set([])
            for item1 in node_list[node[0]]:
                for item2 in node_list[node[1]]:
                    if item1 + item2 in remaining_nums and item1 + item2 in temp_node_list and item1 != item2:
                        node_list[idx].update([item1 + item2])
        elif len(node_list[idx]) < 1:
            return check_for_win(node_list)

    # original code before using enumerate
    #for idx in range(len(node_parents)):
    #    if node_parents[idx] != [] and len(node_list[idx]) > 1:
    #        temp_node_list = node_list[idx]
    #        node_list[idx] = set([])
    #        for item1 in node_list[node_parents[idx][0]]:
    #            for item2 in node_list[node_parents[idx][1]]:
    #                if item1 + item2 in remaining_nums and item1 + item2 in temp_node_list and item1 != item2:
    #                    node_list[idx].update([item1 + item2])
    #    elif len(node_list[idx]) < 1:
    #        return check_for_win(node_list)

    # check if any nodes have been solved, and if so, remove from remaining_nums
    [remaining_nums.remove(item) for item in node_list if len(item) == 1 and item in remaining_nums]

    return calc_parent_from_c_and_s(node_list, remaining_nums, node_parents)

def calc_parent_from_c_and_s(node_list, remaining_nums, node_parents):
    '''
    This function looks at the sibling and child of a node.
    It looks at all child - sibling combinations.
    And if the resulting combination is in remaining_nums and in current possible values for this node, it keeps the combination.
    '''

    for side_idx in range(2):
        for idx in range(len(node_parents)):
            other_idx = (side_idx - 1) ** 2
            if node_parents[idx] != [] and len(node_list[node_parents[idx][side_idx]]) != 1:
                temp_node_list = node_list[node_parents[idx][side_idx]]
                node_list[node_parents[idx][side_idx]] = set([])
                for item1 in node_list[idx]:
                    for item2 in node_list[node_parents[idx][other_idx]]:
                        if item1 - item2 in remaining_nums and item1 - item2 in temp_node_list:
                            node_list[node_parents[idx][side_idx]].update([item1 - item2])

    return chk_node_vs_rem_nums(node_list, remaining_nums, node_parents)

def chk_node_vs_rem_nums(node_list, remaining_nums, node_parents):
    '''
    Update the possible values in node_list, checked against possibilities in remaining_nums.
    '''

    new_node_list = []

    remaining_nums = [x for x in range(1, 16)]
    for node in node_list:
        if len(node) == 1:
            # if there is only one result, then remove value from remaining nums
            # unless it has already been removed, in which case
            # either we have won or this is not the correct solution and we need to go back.
            for value in node:
                try:
                    remaining_nums.remove(value)
                except:
                    return check_for_win(node_list)
                else:
                    print "error in chk node vs rem nums"

    for node in node_list:
        if len(node) > 1:
            new_node_list.append(set([value for value in node if value in remaining_nums]))
        elif len(node) == 1:
            new_node_list.append(set([value for value in node]))
        else:
            print "error in chk node vs rem nums"

    # if no changes then we can return this node list, else continue working
    if new_node_list == node_list:
        return node_list
    else:
        return calc_child_from_parents(new_node_list, remaining_nums, node_parents)

def get_shortest_node(node_list):
    '''
    Get node with smallest number of possibilities.
    '''
    cur_len = float('inf')
    cur_node = -1
    count = -1
    for node in node_list:
        count += 1
        if 1 < len(node) < cur_len:
            cur_len = len(node)
            cur_node = count

    if cur_node != -1:
        return cur_node
    else:
        # win
        return node_list


def set_node_number(node, node_value, node_list, remaining_nums):
    '''
    Set a node to a specific number.
    Remove from remaining nums.
    '''

    node_list[node] = set([node_value])
    remaining_nums.remove(node_value)
    return node_list, remaining_nums

def print_node_list(node_list, message=''):
    '''
    Print function
    '''
    print '*** Printing node list *** %s' %(message)
    for node in node_list:
        print node
    print '*** Printing node list *** %s \n' %(message)

def solve_puzzle(node_list, remaining_nums, node_parents):
    '''
    Puzzle solver function
    Takes a board which has had all "forced" moves completed and
    now needs to be solved by trial and error.
    Starts with node with smallest number of possibilities and works through them
    until it finds a solution.
    Returns the node_list result.
    '''

    if check_for_win(node_list) == node_list:
        return node_list

    next_node = get_shortest_node(node_list)

    reset_node_list = node_list[:]
    reset_remaining_nums = remaining_nums[:]

    possible_node_lists = []
    for value in node_list[next_node]:
        node_list, remaining_nums = set_node_number(next_node, value, node_list, remaining_nums)
        node_list = chk_node_vs_rem_nums(node_list, remaining_nums, node_parents)
        print "Node %d and Value %d" %(next_node, value)
        print_node_list(node_list)
        if node_list != []:
            possible_node_lists.append(node_list)
        node_list = reset_node_list[:]
        remaining_nums = reset_remaining_nums[:]

    for node_list in possible_node_lists:
        node_list = chk_node_vs_rem_nums(node_list, remaining_nums, node_parents)
        return solve_puzzle(node_list, remaining_nums, node_parents)

    return node_list

def get_starting_board(node_list, remaining_nums, node_parents):
    '''
    Takes the starting position given by the problem, and makes the "forced" moves.
    Then sets the puzzle solver in motion.
    Returns the final node list.
    '''
    print_node_list(node_list, '--Starting Position--')
    node_list = chk_node_vs_rem_nums(node_list, remaining_nums, node_parents)
    print_node_list(node_list, '--After forced moves--')
    return solve_puzzle(node_list, remaining_nums, node_parents)

def check_for_win(node_list):
    '''
    Check whether all nodes have exactly one entry and that each entry is unique.
    '''
    count = 0
    node_answers = set([])
    for node in node_list:
        if len(node) != 1 or node_list == []:
            return []
        else:
            count += 1
            node_answers.update(node)

    if count == len(node_list) and len(node_answers) == len(node_list):
        return node_list


def puzzle_one():
    '''
    Puzzle given by poolcues.png
    '''
    #####
    #####
    # set up default values - all possible numbers for all possible nodes
    node_default = [x for x in range(1, 16)]
    node_list = [set(node_default[:])] * 15

    # set up default node parents []
    node_parents = [[]] * 15

    # set up remaining_nums
    remaining_nums = [x for x in range(1, 16)]

    # set up given information
    node_list[0] = set([4])
    node_list[6] = set([5])
    node_list[9] = set([12])

    remaining_nums.remove(4)
    remaining_nums.remove(5)
    remaining_nums.remove(12)

    # set parents for each node
    node_parents[3] = [0, 1]
    node_parents[4] = [1, 2]
    node_parents[9] = [4, 5]
    node_parents[10] = [5, 6]
    node_parents[12] = [6, 7]
    node_parents[13] = [8, 9]
    node_parents[14] = [10, 11]
    #####
    #####

    result = get_starting_board(node_list, remaining_nums, node_parents)
    print_node_list(result, '--Final Board--')

puzzle_one()
