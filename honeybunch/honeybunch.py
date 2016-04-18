'''
Honey Bunch - Calendar Problem Solver
First Created: 2016-Apr-08
Last Updated: 2016-Apr-17
Python 2.7
Chris

See honeybunch.png
Useful hexagon post - http://www.redblobgames.com/grids/hexagons/
'''

#answer_tiles for this problem = set([(-4,4,0),(-2,-2,4),(-2,3,-1),(1,3,-4),(2,1,-3),(3,-4,1),(1,-4,3),(0,-2,2)])

import itertools

# Numbered directions for hexagonal grid, ordered clockwise at 60 degree intervals
DIRECTIONS = {0 : (-1, 1, 0), 1 : (1, 0, -1), 2 : (0, 1, -1),
              3 : (1, -1, 0), 4 : (-1, 0, 1), 5 : (0, -1, 1)}

class HoneyBunch(object):
    '''
    Basic HoneyBunch class
    '''
    def __init__(self, size, starting_tiles):
        '''
        Board set-up.
        Note: only tested on board size of nine.
        '''
        self._size = size
        self._tile_value = {}
        self._starting_number_values = {}

        # len = 61 for grid size 9

        # centre tile is (0, 0, 0)
        # so in each direction it should be half size of the grid
        middle_col = size / 2
        for col in range(-middle_col, middle_col + 1):
            for row in range(-middle_col, middle_col + 1):
                if -middle_col <= row + col <= middle_col:
                    self._tile_value[(col, row, -(row+col))] = 'o'

        # set starting tiles
        for key, value in starting_tiles.iteritems():
            self.set_starting_number_tile(key, value)


    def print_layout(self):
        '''
        Print the board in a readable fashion.
        '''

        tiles_key = []
        tiles_dict = {}

        # convert coordinates so can differentiate between rows
        for key, value in self._tile_value.iteritems():
            tiles_key.append((key[0], key[1]-key[2]))
            tiles_dict[(key[0], key[1]-key[2])] = value

        mid_value = self._size / 2
        for row in range(self._size, -(self._size + 1), -1):
            my_string = ''
            for col in range(-mid_value, mid_value + 1):
                if (col, row) in tiles_key:
                    my_string += ' ' + str(tiles_dict[(col, row)]) + ' '
                else:
                    my_string += '   '
            print my_string

    def set_starting_number_tile(self, tile, value):
        '''
        Sets the starting tiles given by the puzzle.
        '''
        self._starting_number_values[tile] = value
        self.change_tile_value(tile, value)

    def change_tile_value(self, tile, value):
        '''
        Changes the value of a specific tile.
        If tile is changed to bee or number, neighbors must be 0.
        '''
        assert tile in self._tile_value
        self._tile_value[tile] = value

        if value == 'b' or str(value) in str(range(1, 9)):
            return self.make_neighbors_zero(tile)
        else:
            return True

    def get_neighbors(self, tile):
        '''
        Get all neighbors of a tile.
        '''
        return [tuple(map(sum, zip(tile, direction))) for direction in DIRECTIONS.itervalues() if tuple(map(sum, zip(tile, direction))) in self._tile_value]

    def make_neighbors_zero(self, tile):
        '''
        If tile is a starting number or bee, the neighbors must be not bee.
        '''
        neighbors = self.get_neighbors(tile)
        for neighbor in neighbors:
            if self._tile_value[neighbor] == 0 or self._tile_value[neighbor] == 'o':
                self._tile_value[neighbor] = 0
            else:
                return False
        return True

    def find_line_empty_sq(self, tile, and_bees=False):
        '''
        Find all empty tiles in all lines from given tile.
        '''
        squares = self.find_all_tiles_in_line(tile)
        if not and_bees:
            empty_squares = [tile for tile in squares if self._tile_value[tile] == 'o']
        else:
            empty_squares = [tile for tile in squares if self._tile_value[tile] == 'o' or self._tile_value[tile] == 'b']

        return empty_squares

    def find_all_tiles_in_line(self, tile):
        '''
        Find all tiles (empty and filled) in all lines from given tile.
        '''
        starting_tile = tuple(tile)
        mid_value = self._size/2
        edge_range = range(-mid_value, mid_value + 1)

        squares = []
        for direction in DIRECTIONS.itervalues():
            while tile[0] in edge_range and tile[1] in edge_range and tile[2] in edge_range:
                possible_neighbor = tuple(map(sum, zip(tile, direction)))
                if possible_neighbor[0] in edge_range and possible_neighbor[1] in edge_range and possible_neighbor[2] in edge_range:
                    squares.append(possible_neighbor)
                tile = possible_neighbor
            tile = starting_tile

        return squares

    def count_change_bees_in_line(self, tile):
        '''
        Count the number of bees in any of the directions from a given tile.
        '''
        squares = self.find_all_tiles_in_line(tile)
        count = sum(1 for square in squares if self._tile_value[square] == 'b')
        new_value = self._starting_number_values[tile] - count

        self.change_tile_value(tile, new_value)

        return self._tile_value[tile]

    def final_win_set_board(self, winning_combo):
        '''
        Takes a winning combo and applies it to the starting board position.
        '''

        for tile in winning_combo:
            self.change_tile_value(tile, 'b')

        for tile, value in self._tile_value.iteritems():
            if value == 'o':
                self.change_tile_value(tile, '0')

        self.print_layout()
        return winning_combo

    def find_all_bee_combos(self, tile, number):
        '''
        Takes a number tile and it's number of bees.
        Iterates through all possible bee placements.
        Returns all combinations.
        (below rules are applied later in the program)
        #1 can place bee and clear neighbors to 0.
        #2 can clear lines from the number tile to 0.
        #3 other number tiles don't have more than their number of bees in a line.
        #4 other number tiles still have enough space to put their remaining bees.
        '''

        if number < 1:
            return []

        empty_squares = self.find_line_empty_sq(tile, and_bees=True)

        combos = [list(item) for item in itertools.combinations(empty_squares, number)]
        return combos

    def check_is_board_legal(self, combo, eight_bees=False):
        '''
        Checks if a combo is legal.
        eight_bees is if a combo contains all eight bees.
        '''

        backup_board = dict(self._tile_value)

        for tile in combo:
            if not self.change_tile_value(tile, 'b'): #1
                self._tile_value = dict(backup_board)
                return False

        if eight_bees:
            for start_tile in self._starting_number_values:
                if self.count_change_bees_in_line(start_tile) != 0:
                    self._tile_value = dict(backup_board)
                    return False
            self._tile_value = dict(backup_board)
            return True
        else:
            for start_tile, number_tile_value in self._starting_number_values.iteritems():
                bee_line_count = self.count_change_bees_in_line(start_tile)
                if bee_line_count > number_tile_value or bee_line_count > self.find_line_empty_sq(start_tile): # 3 and 4
                    return False

            return True


    def honey_solver(self):
        '''
        Solver.
        Takes a honey board and returns the positions of all bees.
        Iterates through starting number tiles, collecting legal combos.
        By the end there should only be one combo of len(8) that meets legal criteria.
        '''

        start_num_list = list(self._starting_number_values.iteritems())
        legal_combos = self.find_all_bee_combos(start_num_list[0][0], start_num_list[0][1])
        starting_board = dict(self._tile_value)
        for item in start_num_list[1:]:
            print 'Calculating...'

            new_legal_combos = []
            for combo in legal_combos:
                if self.check_is_board_legal(combo):
                    new_legals = [thing + combo for thing in self.find_all_bee_combos(item[0], item[1])]
                    new_legal_combos.extend(new_legals)
                    self._tile_value = dict(starting_board)

            legal_combos = new_legal_combos

        for combo in legal_combos:
            if self.check_is_board_legal(combo, eight_bees=True):
                return self.final_win_set_board(set(combo))

        return False


def puzzle_one():
    '''
    Honey puzzle - see honeybunch.png
    '''
    # init board and set starting tiles
    honey1_starting_tiles = {(-4, 0, 4): 2, (-2, 1, 1): 4,\
    (-1, 4, -3): 2, (1, 0, -1): 3, (2, -2, 0): 4, (4, -3, -1): 1}

    honey1 = HoneyBunch(9, honey1_starting_tiles)
    honey1.print_layout()
    result = honey1.honey_solver()
    print len(result), result

puzzle_one()
