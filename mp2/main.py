import numpy as np


def solve_puzzle(puzzle_file):
    wordlist = open('./input/wordlist.txt', 'r')
    puzzle = open(puzzle_file, 'r')

    length = int(puzzle.readline())
    START_CONSTRAINTS = [[] for x in xrange(length)]
    cat2ind = {}
    cat2wor = {}

    for line in wordlist:
        category, words = line.strip().replace(', ', '').split(':\t')
        cat2wor[category] = np.fromstring(words, dtype=np.uint8).reshape((-1, 3))

    for line in puzzle:
        category, index = line.strip().split(': ')
        indexes = np.array(map(int, index.split(', ')), dtype=np.uint8) - 1
        cat2ind[category] = indexes

        for x, ind in enumerate(indexes):
            START_CONSTRAINTS[ind].append((category, x))

    SPACE = 46
    START_ASSIGNMENT = np.zeros(length, dtype=np.uint8) + SPACE
    EMPTY_LIST = []


    def alphabet():
        return np.arange(26, dtype=np.uint8) + 65


    def letter_most_constrained_var(assignment, constraints):
        letter_index, letter_const = max(enumerate(constraints), key=lambda x: len(x[1]))
        letter_choices = alphabet()

        for category, assign_index in letter_const:
            clue_words = cat2wor[category]
            letter_vals = assignment[cat2ind[category]]

            whereabouts = np.ones(np.shape(clue_words)[0], dtype=bool)

            for lut_index, assign_letter in enumerate(letter_vals):
                if assign_letter != SPACE:
                    np.logical_and(whereabouts, clue_words[:, lut_index] == assign_letter, whereabouts)

            letter_choices = np.intersect1d(letter_choices, clue_words[whereabouts, assign_index])

        return letter_index, letter_const, letter_choices


    START_LEN = len(START_CONSTRAINTS) - 1
    PRINT_STRING = 'search order: letter with the most word dependencies\nroot'
    ARROW_OVER = ' -> '


    def letter_search(assignment, constraints, print_string):
        # print assignment.tostring()

        if all(assignment != SPACE):
            # print 'FOUND A MATCH'
            print_string += (ARROW_OVER + assignment.tostring() + '\n    ')
            # temp = {}
            # for category in cat2ind:
            #     temp[category] = assignment[cat2ind[category]].tostring()
            # print temp
            return True, print_string
        else:
            letter_index, letter_const, letter_choices = letter_most_constrained_var(assignment, constraints)
            constraints[letter_index] = EMPTY_LIST

            result = False

            for value in letter_choices:
                if print_string.endswith('\n    '):
                    print_string += ('     ' * (START_LEN - sum(len(x) != 0 for x in constraints)) + ARROW_OVER + value.tostring())
                else:
                    print_string += (ARROW_OVER + value.tostring())

                assignment[letter_index] = value
                temp_result, print_string = letter_search(assignment, constraints, print_string)
                result = result or temp_result
                assignment[letter_index] = SPACE

            if not result:
                # print 'Backtracking...'
                print_string += (ARROW_OVER + 'backtrack' + '\n    ')

            constraints[letter_index] = letter_const
            return True, print_string

    return letter_search(START_ASSIGNMENT, START_CONSTRAINTS, PRINT_STRING)[1] + '\n\n'


letter_output = open('./output/letter_trace.txt', 'w+')
for x in xrange(1, 6):
    letter_output.write(solve_puzzle('./input/puzzle{}.txt'.format(x)))