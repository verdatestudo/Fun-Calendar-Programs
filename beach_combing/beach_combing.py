'''
Beach Combing - Calendar Problem Solver
First Created: 2016-May-18
Last Updated: 2016-May-19
Python 2.7
Chris

See beach_combing.png

todo
- split into 81 sections of 9x9 grid (done! using slice image)
- recognise shape of each
- recognise color of each
- draw line through chosen cells, combine back into one picture
'''

GRID_SIZE = 9
DIRECTIONS = {(-1, 0): 'up', (1, 0): 'down', (0, -1): 'left', (0, 1): 'right'}

###
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

def slice_image(image):
    '''
    Slice the 9x9 grid into equal sized pieces.
    '''
    import image_slicer
    image_slicer.slice('beach_combing_grid.png', 81)

def get_nebors():
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
                    if GRAPH[potential_nebor[0]][potential_nebor[1]][0] == GRAPH[row][col][0] \
                    or GRAPH[potential_nebor[0]][potential_nebor[1]][1] == GRAPH[row][col][1]:
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

    # get the node distance furthest away from the starting node.
    end_num = 0
    for row in node_bfs:
        if max(row)[0] > end_num:
            end_num = max(row)[0]

    final_answers = [(8, 8)]

    cur_pos = (8, 8)
    while end_num > 1:
        end_num, cur_pos = node_bfs[cur_pos[0]][cur_pos[1]]
        final_answers.append(cur_pos)

    return final_answers[::-1]

def run():
    '''
    Run program.
    '''
    graph_adj_list = get_nebors()
    node_bfs = bfs(graph_adj_list, (0, 0))
    print get_final_results(node_bfs)

run()
