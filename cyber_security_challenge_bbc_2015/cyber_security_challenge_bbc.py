
'''
UK Cyber Security BBC article challenge
Questions: http://www.bbc.co.uk/news/technology-34312697
Answers: http://www.bbc.co.uk/news/technology-35929741

First Created: 2016-Mar-25
Last Update: 2016-Apr-04
Python 2.7
Chris
'''

def csarCipher(myString, section=None):
    '''
    Caesar Cipher
    If section = None do all rotations, else only that specific rotation number
    '''
    myFile = open('codecode.txt', 'r+')
    myDict = {}

    for line in myFile:
        first, middle, rest = line.partition(":")
        rest = rest.rstrip()
        myDict[first] = rest.replace(" ", "")

    if section != None:
        section = str(section)
        newWord = ''
        for letter in myString.upper():
            try:
                newWord += myDict['PP'][myDict[section].index(letter)]
            except:
                newWord += letter
        print section, newWord
    else:
        for section in myDict:
            newWord = ''
            for letter in myString.upper():
                try:
                    newWord += myDict['PP'][myDict[section].index(letter)]
                except:
                    newWord += letter
            print section, newWord

    myFile.close()

def translate_morse_code(my_string, from_morse=True):
    '''
    Morse code translator
    http://stackoverflow.com/questions/32094525/morse-code-to-english-python3
    '''

    #examples
    #translate_morse_code('hello', from_morse = False)
    #translate_morse_code('.... . .-.. .-.. ---')

    CODE = {'A': '.-',     'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.'
        }

    CODE_REVERSED = {value:key for key, value in CODE.items()}

    if from_morse == False:
        my_morse = ' '.join(CODE.get(i.upper()) for i in my_string)
    else:
        my_morse = ''.join(CODE_REVERSED.get(i) for i in my_string.split())

    return my_morse

def question_one():
    '''
    Bletchley
    Turing
    Transistor
    '''
    pass

def question_two():
    '''
    Challenge Two

    This time there is no key to help decipher this short string of numbers, so it is a bit harder.
    However, here is a hint - once deciphered the string will reveal the name of a famous maths code that uses numbers.

    5 8 1 14 13 0 2 2 8 18 4 16 20 4 13 2 4

    ans = Fibonacci Sequence
    '''
    my_string = [5, 8, 1, 14, 13, 0, 2, 2, 8, 18, 4, 16, 20, 4, 13, 2, 4]
    my_string2 = [x + 97 for x in my_string]
    return [chr(x) for x in my_string2]

def question_three():
    '''
    Challenge Three
    Code-breaking was practised in Roman times: Julius Caesar was known to use a code to securely send messages to his armies.
    This message uses a type of cipher named after the general to conceal its meaning.
    When you crack it you will find out where he kept his armies.

    ans = up his sleevies

    X S K L V V O H H Y L H V
    '''

    return csarCipher('XSKLVVOHHYLHV', '03')


def question_four():
    '''
    Challenge Four
    Now the puzzles get more tricky.
    This code does not use numbers and letters to hide what it says.
    Instead, it swaps those familiar characters for symbols.
    Once cracked, the following message reveals who famously made use of this type of enciphering and the name of the technique.
    Here is a hint: it requires a code that shares its name with a place where a smelly farm animal is kept.

    Pigpen Cipher
    see pigpen.png

    ans = In the 18th century, freemasons used pig pen ciphers to keep their private records.
    '''

def question_five():
    '''
    Challenge Five

    This one is a real step up in difficulty.
    It can probably be done by trial and error, but it will be quicker to work out the rules governing the substitution and apply them.
    The key to cracking the message is elementary and you may find it easier to sit at a table rather than a desk to crack it.
    Breaking the cipher will reveal a question. The solution is the answer to that question.

    ans = J and Q
    '''

    import csv
    csv_file = 'elementlist.csv'

    my_elements = {}

    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            # create a dictionary in the format {element no: element letters}
            my_elements[row[0]] = row[1]

    my_string = [81, 1, 68, 59, 68, 86, 53, 76, 105, 53, 24, 22, 89, 5, 57, 68, 77, 50, 89, 81, 85, 4, 113, 71, 95, 86, 47, 44, 45, 33, 11,\
     64, 99, 12, 63, 10, 73, 8, 87, 52, 67, 68, 24, 72, 63, 25, 77, 6, 13, 3, 68, 57, 63, 101, 99, 60, 43, 14, 76, 88, 64, 47, 7, 53,\
      50, 99, 66, 76, 60, 22, 1, 99, 5, 47, 62, 53, 106, 8, 9, 81, 2, 68, 53, 75, 89, 52, 8, 25, 77, 27, 28, 113, 42, 4, 63, 75, 34, 63, 71, 63, 27, 52,\
      88, 76, 11, 17, 8, 11, 26, 77, 32, 113, 45, 13, 52, 77, 76, 11, 14, 13, 11, 66, 44, 63, 6, 115, 44, 37, 77, 7, 31, 6, 67, 63, 42, 77, 17,\
       13, 57, 84, 45, 8, 15, 63, 86, 43, 77, 68, 62, 74, 68, 23, 63, 92, 14, 68, 66, 53, 22, 52, 8, 24, 44, 68, 13, 81, 63, 18, 17, 53, 46, 72,\
        68, 44, 83, 39, 92, 62, 77, 28, 31, 52, 67, 63, 53, 28, 77, 43, 53, 13, 3, 3, 68, 65, 43, 63, 45, 34, 8, 26, 73, 67, 63, 68, 3, 63, 42, 68,\
         60, 65, 21, 4, 92, 73, 52, 74, 8, 57, 68, 65, 43, 63, 44, 38, 20, 13, 10, 52, 5, 63, 92, 50, 68, 66, 74, 67, 13, 81, 33, 75, 68, 81, 80, 63, 70]

    # simply convert the given string into letters using the periodic table (only take the first letter if element has more than one)
    my_answer = ''
    for item in my_string:
        my_answer += my_elements[str(item)][0]

    # create a set of letters used above
    my_letters = set([])
    for k, v in my_elements.iteritems():
        my_letters.update(v[0])

    # find the letters in the alphabet not used above
    missing_letters = []
    my_letter_nums = [ord(item) for item in my_letters]
    for idx in range(65, 91):
        if idx not in my_letter_nums:
            missing_letters.append([idx, chr(idx)])

    return my_answer.lower(), missing_letters


def question_six_part_one():
    '''
    Good work if you have got this far.
    This final challenging set of puzzles has three parts; when each one is completed it will reveal a quote from a well-known work of literature,
    whose author loved intellectual games of all kinds.
    Can you find all three?

    Bear in mind while you are working on these that each puzzle is not necessarily just a cipher - there are some computer science basics mixed in.
    Each one is designed to be solved independently so if one of the puzzles defeats you then move on.
    Here's one final clue: Alice fell down a rabbit hole and left clues so Bob could find her...

    Note: for Q6 this blog post was helpful:
    http://adventuresincyberchallenges.blogspot.co.uk/2016/03/bbccom-cyber-security-article-partial.html

    See lastquestion.png

    Hex string + Caesar Cipher rotation 13
    '''

    my_string = '224a72276572206e7979207a6e7120757265722e2056277a207a6e712e204c6268276572207a6e712e22202255626a207162206c6268207861626a2056277a207a6e713f2220666e7671204e797670722e20224c6268207a686667206f722c2220666e76712067757220506e672c20226265206c6268206a6268797161276720756e69722070627a7220757265722e'
    my_hex_string = my_string.decode("hex")
    return csarCipher(my_hex_string, 13)

def question_six_part_two():
    '''
    See part_one

    From BBC answer page:

    Puzzle two was a bit of a beast. The key, literally, was using the five numbers arranged around the pentagon in the picture.
    Starting at 3 and going clockwise gives the five character string 38108.
    Repeating this 29 times gives a string 145-characters long, the same length as the one below the pentagon.
    Getting intelligible text out of this first requires using both strings and then performing what is known as an "exclusive or" (XOR) operation on them.
    Xor calculator - https://xor.pw/
    Performing this operation produces another 145-character string that can be converted into English by looking up the numbers on a table of Ascii characters.
    Use the decimal column.
    The sneaky part was realising that in some cases two numbers represented a character and in others it was three. Not easy.
    Anyone who went through these steps would reveal the following text: 'It's a poor sort of memory that only works backwards.'
    '''

    # go around the pentagon until we have the exact length as the given answer string below the pentagon
    char_string = '38108' * 29
    given_answer_string = '1528262114512379959787446361667336365541049710185448490827733939750117578606349583824805994668155766548948086204569455380471171904239315967452691'

    assert len(char_string) == len(given_answer_string)

    # using the xor calculator above
    xor_string = '3973116391153297321121111111143211511111411632111102321091011091111141213211610497116321111101081213211911111410711532989799107119971141001154639'
    assert len(xor_string) == len(given_answer_string)

    # convert xor string to ascii characters.
    count = 0
    ans_string = ''
    while count < (len(xor_string) - 1):
        # if it does not start with a 1, then we take the 2 digit code
        if xor_string[count] != '1':
            two_num_int = int(xor_string[count] + xor_string[count + 1])
            ans_string += chr(two_num_int)
            count += 2
        # else it is a three digit code
        else:
            three_num_int = int(xor_string[count] + xor_string[count + 1] + xor_string[count + 2])
            ans_string += chr(three_num_int)
            count += 3

    return ans_string

def question_six_part_three():
    '''
    See part_one

    My initial guess for this puzzle was a knight's tour / trellis cipher but couldn't find a solution.
    From the blog post above it's actually morse code.
    '''
    my_string = '--- ..-. ..-.  .-- .. - ....  - .... . .. .-.  .... . .- -.. ...'
    return translate_morse_code(my_string)

def all_questions():
    '''
    All questions
    '''
    print '\n', 'Question 2: '
    print question_two()
    print '\n', 'Question 3: '
    print question_three()
    print '\n', 'Question 5: '
    print question_five()[0], '\n', question_five()[1]
    print '\n', 'Question 6 - part one: '
    print question_six_part_one()
    print '\n', 'Question 6 - part two: '
    print question_six_part_two()
    print '\n', 'Question 6 - part three: '
    print question_six_part_three()

all_questions()
