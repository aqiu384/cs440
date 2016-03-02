import numpy as np


def solve_puzzle(puzzle_file):
    wordlist = open('./input/wordlist.txt', 'r')
    puzzle = open(puzzle_file, 'r')

    length = int(puzzle.readline())
    START_CONSTRAINTS = [[] for x in xrange(length)]
    cat2ind = {}
    cat2wor = {}
    word_hits = {}

    for line in wordlist:
        category, words = line.strip().replace(', ', '').split(':\t')
        cat2wor[category] = np.fromstring(words, dtype=np.uint8).reshape((-1, 3))
        word_hits[category] = np.shape(cat2wor[category])[0]

    for line in puzzle:
        category, index = line.strip().split(': ')
        indexes = np.array(map(int, index.split(', ')), dtype=np.uint8) - 1
        cat2ind[category] = indexes

        for x, ind in enumerate(indexes):
            START_CONSTRAINTS[ind].append((category, x))

    SPACE = 46
    START_ASSIGNMENT = np.zeros(length, dtype=np.uint8) + SPACE
    CONSTRAINTS = cat2ind.items()
    CONSTRAINTS.sort(key=lambda x: -1 * word_hits[x[0]])


    def alphabet():
        return np.arange(26, dtype=np.uint8) + 65


    def word_most_constrained_var(assignment, constraints):
        category, letter_inds = constraints.pop()
        letter_checks = []

        for local_ind, global_ind in enumerate(letter_inds):
            local_letter = assignment[global_ind]

            if local_letter != SPACE:
                letter_check = np.array([local_letter], dtype=np.uint8)
            else:
                letter_check = cat2wor[category][:, local_ind]

            for curr_cat, curr_ind in START_CONSTRAINTS[global_ind]:
                letter_check = np.intersect1d(letter_check, cat2wor[curr_cat][:, curr_ind])

            letter_checks.append(np.in1d(cat2wor[category][:, local_ind], letter_check))

        valid_words = np.logical_and(letter_checks[0], np.logical_and(letter_checks[1], letter_checks[2]))
        valid_words = cat2wor[category][valid_words, :]

        return category, letter_inds, valid_words

    START_LEN = len(CONSTRAINTS) - 1
    PRINT_STRING = 'search order: category with the fewest entries in word list\nroot'
    ARROW_OVER = ' -> '


    def word_search(assignment, constraints, print_string):
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
            category, letter_inds, valid_words = word_most_constrained_var(assignment, constraints)
            result = False

            for word in valid_words:
                if print_string.endswith('\n    '):
                    print_string += ('       ' * (START_LEN - len(constraints)) + ARROW_OVER + word.tostring())
                else:
                    print_string += (ARROW_OVER + word.tostring())

                # print word.tostring(), START_LEN - len(constraints)

                new_assign = np.copy(assignment)
                new_assign[letter_inds] = word
                temp_result, print_string = word_search(new_assign, constraints, print_string)
                result = result or temp_result

            if not result:
                # print 'Backtracking...'
                print_string += (ARROW_OVER + 'backtrack' + '\n    ')

            constraints.append((category, letter_inds))
            return True, print_string

    return word_search(START_ASSIGNMENT, CONSTRAINTS, PRINT_STRING)[1] + '\n\n'


word_output = open('./output/word_trace.txt', 'w+')
for x in xrange(1, 6):
    word_output.write(solve_puzzle('./input/puzzle{}.txt'.format(x)))
