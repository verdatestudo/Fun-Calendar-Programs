'''
Beach Combing - Calendar Problem Solver
First Created: 2016-May-18
Last Updated: 2016-May-28
Python 2.7
Chris

See beach_combing_puzzle.png
'''

import cv2
import detect_color_bc as dcbc

GRID_SIZE = 9
DIRECTIONS = {(-1, 0): 'up', (1, 0): 'down', (0, -1): 'left', (0, 1): 'right'}

###
# This was manually input so I could create the BFS solution first.
# Now useful as a check that the automatic color/shape detection is working.

# colours ... blue = 0, green = 1, red = 2
# shapes ... star = 0, circle = 1, shell = 2
GRAPH = [[[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [0, 2], [1, 0], [1, 1], [1, 2]],\
[[0, 2], [2, 2], [0, 1], [1, 0], [1, 1], [2, 2], [1, 1], [2, 0], [0, 2]],\
[[1, 1], [2, 1], [0, 0], [1, 2], [2, 0], [0, 0], [0, 1], [0, 0], [2, 1]],\
[[2, 2], [1, 2], [1, 0], [0, 2], [2, 2], [2, 1], [0, 2], [1, 2], [1, 1]],\
[[2, 1], [0, 2], [1, 1], [2, 0], [1, 1], [0, 1], [2, 2], [2, 0], [2, 2]],\
[[1, 0], [0, 0], [2, 2], [0, 0], [1, 0], [0, 2], [2, 0], [0, 1], [1, 2]],\
[[1, 2], [2, 0], [1, 2], [0, 1], [2, 0], [1, 1], [1, 0], [1, 1], [2, 1]],\
[[0, 2], [2, 1], [1, 0], [0, 0], [1, 2], [0, 1], [1, 2], [0, 2], [2, 0]],\
[[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [0, 0], [2, 0], [2, 1], [1, 1]]]
###
###

NEW_GRAPH = dcbc.detect_color() # returns 2d grid in format ['blue', 'shell']

def test_ml_vs_manual_graph(ml_graph, man_graph):
    '''
    Checks whether the automatically generated color/shape detection matches manual input.
    Checks both graphs produce the same list of nebors.
    '''
    ml_nebors = get_nebors(ml_graph)
    man_nebors = get_nebors(man_graph)

    if ml_nebors == man_nebors:
        print 'ML graph matches manual graph!'
        return True
    else:
        print 'Test fail: ML graph does not match manual graph'
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if ml_nebors[x][y] != man_nebors[x][y]:
                    print (x, y), ml_graph[x][y], man_graph[x][y], '\n' # compare this with eye test to see what is incorrect
        return False

def get_nebors(graph):
    '''
    Get the neighbors of each node.
    Return an adjcency list.
    '''
    # adjacency list
    graph_adj_list = [[[] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            for direction in DIRECTIONS:
                potential_nebor = map(sum, zip((row, col), direction))
                if 0 <= potential_nebor[0] < GRID_SIZE and 0 <= potential_nebor[1] < GRID_SIZE: # ensure pot nebor is on the grid
                    if graph[potential_nebor[0]][potential_nebor[1]][0] == graph[row][col][0] \
                    or graph[potential_nebor[0]][potential_nebor[1]][1] == graph[row][col][1]:
                        # check that pot nebor colour or shape is same as current item, if so it must be a pot nebor.
                        graph_adj_list[row][col].append(potential_nebor)

    return graph_adj_list

def bfs(graph, start_pos):
    '''
    BFS for finding the route through the grid.
    Adapted for [row][col] graph storage instead of just [node].
    '''
    node_bfs = [[[float('inf'), None] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] # for each node, set default distance and parent
    queue = [start_pos] # enq starting node
    node_bfs[start_pos[0]][start_pos[1]][0] = 0 # starting node distance = 0

    while queue:
        current_node = queue.pop(0) # FIFO queue rather than LIFO stack

        for nebor in graph[current_node[0]][current_node[1]]:
            if node_bfs[nebor[0]][nebor[1]][0] == float('inf'): # if not visited
                node_bfs[nebor[0]][nebor[1]][0] = node_bfs[current_node[0]][current_node[1]][0] + 1 # distance = parent distance + 1
                node_bfs[nebor[0]][nebor[1]][1] = current_node # set it's parent
                queue.append(nebor) #enq

    return node_bfs

def get_final_results(node_bfs):
    '''
    Use gathered information to return a list containing all nodes in path.
    '''

    end_num = [max(row)[0] for row in node_bfs] # get the node with distance furthest away from the starting node.

    final_answers = [(8, 8)]

    cur_pos = (8, 8)
    while end_num > 1:
        end_num, cur_pos = node_bfs[cur_pos[0]][cur_pos[1]] # get parent and parent distance from origin
        final_answers.insert(0, tuple(cur_pos))

    return final_answers

def draw_result(mark_tiles):
    '''
    Draws line on original image to show the path.
    '''
    # reversed to get x and y in right order.
    img_pos = [tuple([40 + 80 * x for x in reversed(tile)]) for tile in mark_tiles]

    print img_pos

    img = cv2.imread('beach_combing_grid.png')

    for idx, tile in enumerate(img_pos):
        if idx < len(img_pos) - 1:
            cv2.line(img, tile, img_pos[idx + 1], (255, 255, 255), 5)

    cv2.imwrite('beach_combing_grid_result.png', img)
    cv2.imshow('image', img)
    cv2.waitKey(0)


def run():
    '''
    Run program.
    '''
    #test_ml_vs_manual_graph(NEW_GRAPH, GRAPH)
    graph_adj_list = get_nebors(NEW_GRAPH)
    node_bfs = bfs(graph_adj_list, (0, 0))
    final_results = get_final_results(node_bfs)
    print final_results
    draw_result(final_results)

run()
