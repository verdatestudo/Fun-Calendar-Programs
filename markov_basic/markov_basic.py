
'''
(Very) Basic Markov Model
Roughly based on: https://www.reddit.com/r/Python/comments/2ife6d/pykov_a_tiny_python_module_on_finite_regular/cl3bybj

2016-Apr-29
Python 2.7
Chris
'''

import random

my_dict = {}
my_dict[''] = ['r', 'l']
my_dict['r'] = ['e', 'a']
my_dict['a'] = ['End', 'd']
my_dict['e'] = ['o']
my_dict['o'] = ['s']
my_dict['s'] = ['t', 'h']
my_dict['t'] = ['r', 's']
my_dict['l'] = ['i']
my_dict['i'] = ['g']
my_dict['g'] = ['h']
my_dict['h'] = ['t', 'a']
my_dict['d'] = ['o']
my_dict['o'] = ['w']
my_dict['w'] = ['End']

my_answers = {}

for x in range(100):
    value = ''
    my_string = ''

    while value != 'End':
        my_string += value
        value = random.choice(my_dict[value])

    my_answers[my_string] = my_answers.get(my_string, 0) + 1

for k, v in my_answers.iteritems():
    print k, v
