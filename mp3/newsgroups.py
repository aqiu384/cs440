import numpy as np

TRAINING_DATA = './8category/8category.training.txt'
TESTING_DATA = './8category/8category.testing.txt'
LAPLACE_K = float(1)
SIZE = 8

category_dicts = [{} for _ in xrange(SIZE)]
doc_totals = np.zeros(SIZE, dtype=np.float)

with open(TRAINING_DATA) as training_data:
    for line in training_data:
        words = line.split()
        category = int(words[0])

        doc_totals[category] += 1

        for pair in words[1:]:
            word, count = pair.split(':')
            count = int(count)

            try:
                category_dicts[category][word] += 1 #count
            except KeyError:
                for curr_category in xrange(SIZE):
                    category_dicts[curr_category][word] = LAPLACE_K
                category_dicts[category][word] += 1 #count

word_totals = [sum(x.values()) for x in category_dicts]
category_priors = doc_totals / sum(doc_totals)
confusion_matrix = np.zeros((SIZE, SIZE), dtype=np.uint32)

for category in xrange(SIZE):
    curr_dict = category_dicts[category]
    curr_total = doc_totals[category] #word_totals[category]
    for word in curr_dict:
        curr_dict[word] = np.log(curr_dict[word] / curr_total)

with open(TESTING_DATA) as testing_data:
    i = 0
    for line in testing_data:
    # while i < 10:
    #     line = next(spam_testing)
        words = line.split()
        category_actual = int(words[0])

        curr_scores = np.zeros(SIZE, dtype=np.float)

        for pair in words[1:]:
            word, count = pair.split(':')
            count = int(count)

            try:
                for category in xrange(SIZE):
                    curr_scores[category] += category_dicts[category][word] * count
            except KeyError:
                pass

        category_guess = np.argmax(curr_scores)
        confusion_matrix[category_actual, category_guess] += 1

        i += 1

print confusion_matrix
print np.divide(np.diag(confusion_matrix).astype(np.float), np.sum(confusion_matrix, axis=1))
for category_dict in category_dicts:
    for word, score in sorted(category_dict.items(), key=lambda x: x[1], reverse=True)[:20]:
        print word, score
    print