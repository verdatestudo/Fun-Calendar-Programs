'''
Misc Interview Questions
Python 2.7
Chris
'''

def fizzBuzz(num):
    '''
    Good old FizzBuzz
    '''
    for x in range(1, num + 1):
        my_string = ''
        if x % 3 == 0:
            my_string += 'Fizz'
        if x % 5 == 0:
            my_string += 'Buzz'

        print my_string or x

def freq_of_letters(my_string):
    '''
    Takes a string, returns list of letters sorted in descending order of frequency.
    '''
    letter_freq = {}
    for letter in my_string:
        letter_freq[letter] = letter_freq.get(letter, 0) + 1

    for letter in sorted(letter_freq, key=letter_freq.get, reverse=True):
        print letter, letter_freq[letter]

def factorial(num):
    '''
    Simple recursive function for calculating factorial
    '''
    if num == 1:
        return 1
    else:
        return num * factorial(num - 1)

def coin_calc_dynamic(target, coins):
    '''
    Takes a target integer and a list of coins.
    Dynamic Programming version.
    See this blog for info: http://www.mathblog.dk/project-euler-31-combinations-english-currency-denominations/
    '''
    coins.sort() #list needs to be ascending
    ways = [0] * (target + 1) # no. of combinations
    ways[0] = 1 # with 0p change there is only one way to do it
    for coin in coins:
        for combo_num in range(coin, target + 1):
            ways[combo_num] += ways[combo_num - coin]

    return ways[-1]

def testing():
    fizzBuzz(100)
    print freq_of_letters('foefdsjdasidjspdjwspdjdpejpiejeifjefj')
    print factorial(8), 40320
    print factorial(5), 120
    print coin_calc_dynamic(200, [1, 2, 5, 10, 20, 50, 100, 200]), 73682 #73682

testing()
