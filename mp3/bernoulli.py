import numpy as np

SPAM_TRAIN = './sentiment/rt-train.txt' #'./spam_detection/train_email.txt'
SPAM_TEST = './sentiment/rt-test.txt' #'./spam_detection/test_email.txt'
LAPLACE_K = float(1)

norm_dict = {}
spam_dict = {}
norm_prior = float(0)
spam_prior = float(0)

with open(SPAM_TRAIN) as spam_training:
    for line in spam_training:
        words = line.split()

        if int(words[0]) == 1:
            curr_dict = spam_dict
            other_dict = norm_dict
            spam_prior += 1
        else:
            curr_dict = norm_dict
            other_dict = spam_dict
            norm_prior += 1

        for pair in words[1:]:
            word, count = pair.split(':')
            count = int(count)

            try:
                curr_dict[word] += 1
            except KeyError:
                curr_dict[word] = float(count) + LAPLACE_K
                other_dict[word] = LAPLACE_K

# print sorted(norm_dict.items(), key=lambda x: x[1], reverse=True)[:20]
# print sorted(spam_dict.items(), key=lambda x: x[1], reverse=True)[:20]

#norm_count = sum(norm_dict.values())
#spam_count = sum(spam_dict.values())
norm_base = np.log(norm_prior / (norm_prior + spam_prior))
spam_base = np.log(spam_prior / (norm_prior + spam_prior))

#print norm_base, spam_base

confusion_matrix = np.zeros((2, 2), dtype=np.uint16)

for key in norm_dict:
    norm_dict[key] = np.log(norm_dict[key] / norm_prior)
for key in spam_dict:
    spam_dict[key] = np.log(spam_dict[key] / spam_prior)

with open(SPAM_TEST) as spam_testing:
    i = 0
    for line in spam_testing:
    #while i < 1:
    #    line = next(spam_testing)
        words = line.split()
        label = (int(words[0]) == 1)

        norm_score = {}
        spam_score = {}

        for pair in words[1:]:
            word, count = pair.split(':')
            count = int(count)

            try:
                norm_score[word] = norm_dict[word] #* count
            except KeyError:
                pass
            try:
                spam_score[word] = spam_dict[word] #* count
            except KeyError:
                pass

        #print norm_score
        #print spam_score
        #print len(norm_score), len(spam_score)
        #print sum(norm_score.values()), sum(spam_score.values())

        label_guess = (sum(norm_score.values()) < sum(spam_score.values()))
        i += 1

        confusion_matrix[label, label_guess] += 1

print confusion_matrix
print np.divide(np.diag(confusion_matrix).astype(np.float), np.sum(confusion_matrix, axis=1))
for word, score in sorted(norm_dict.items(), key=lambda x: x[1], reverse=True)[:20]:
    print word, score
print
for word, score in sorted(spam_dict.items(), key=lambda x: x[1], reverse=True)[:20]:
    print word, score