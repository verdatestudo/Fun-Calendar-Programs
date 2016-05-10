
import re
import operator
import string

def get_operator_fn(op):
    '''
    Operator Dictionary helper function
    Used in string_and_int
    '''
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.div,
        '%' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, operator, op2):
    '''
    Calculator helper function
    Used in string_and_int
    '''
    op1, op2 = int(op1), int(op2)
    return get_operator_fn(operator)(op1, op2)

def string_and_int(my_string, quick_add=False):
    '''
    https://www.reddit.com/r/cscareerquestions/comments/3nwscx/why_do_programming_interview_tests_only_focus_on/cvs2bm3

    The question asks the following:
    Given a string containing numbers and the addition sign, return the integer value represented by the expression
    -- i.e. myFunction("3+5+8") should return 16, and myFunction("1+2+3+4+5") should return 15.

    Algorithmic knowledge:
    Can the candidate come up with a suitable algorithm to solve the problem at hand?
    (As an extension, what if we also supported subtraction, as well as parentheses to indicate order of operations. Then what would we do?)
    '''
    if quick_add:
        return sum(int(n) for n in my_string.split('+'))

    bracket_list = re.findall('\((.*?)\)',my_string)
    for item in bracket_list:
        first, op, second = re.split("([+-/*])", item.replace(" ", ""))
        bracket_calc = eval_binary_expr(first, op, second)
        my_string = my_string.replace(item, str(bracket_calc))

    my_string = my_string.replace('(', '')
    my_string = my_string.replace(')', '')

    split_list = re.split("([+-/*])", my_string.replace(" ", ""))

    my_total = int(split_list[0])
    for x in range(1, len(split_list), 2):
        my_total = eval_binary_expr(my_total, split_list[x], split_list[x + 1])

    return my_total

print string_and_int("10+12+13", quick_add=True), 35
print string_and_int("3+5+8", quick_add=True), 16
print string_and_int("10+12+13"), 35
print string_and_int("10-12*13"), -26
print string_and_int("10*(4-4)-9*(2*2)"), -36
