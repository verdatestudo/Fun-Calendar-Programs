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

    print ways
    return ways[-1]

print coin_calc_dynamic(200, [1, 2, 5, 10, 20, 50, 100, 200]) #73682

'''
example: (target = 5, coins = [1, 2, 5])
    for coin in coins:
        for combo_num in range(coin, target + 1):
            ways[combo_num] += ways[combo_num - coin]

COIN = 1
COMBO NUM = 1, 2, 3, 4, 5
ways[1] = 1
ways[2] = 1
ways[3] = 1
ways[4] = 1
ways[5] = 1

COIN = 2
COMBO NUM = 2, 3, 4, 5

ways[1] = 1
ways[2] = 2
ways[3] = 2
ways[4] = 3
ways[5] = 3

COIN = 5
COMBO NUM = 5

ways[1] = 1
ways[2] = 2
ways[3] = 2
ways[4] = 3
ways[5] = 4
'''
