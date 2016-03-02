import numpy as np

FACE_WIDTH = 60
FACE_HEIGHT = 70
TRAINING_LEN = 451
TEST_LEN = 150

SIZE = 28
TRAINING_LEN = 5000
TEST_LEN = 1000
IMAGE_TYPE = np.float
LAPLACE_K = 1

np.set_printoptions(precision=3, linewidth=200)

image = np.empty((SIZE, SIZE), dtype=np.uint8)
image_sums = np.zeros((SIZE, SIZE, 10), dtype=IMAGE_TYPE)
label_sums = np.zeros(10, dtype=IMAGE_TYPE)

training_images = open('./digitdata/trainingimages')
training_labels = open('./digitdata/traininglabels')

test_sums = np.zeros(10, dtype=IMAGE_TYPE)
confusion_matrix = np.zeros((10, 10), dtype=np.uint16)

highest_match = np.zeros((SIZE, SIZE, 10), dtype=np.uint8)
lowest_match = np.zeros((SIZE, SIZE, 10), dtype=np.uint8)
highest_score = np.ones(10, dtype=IMAGE_TYPE) * -np.inf
lowest_score = np.zeros(10, dtype=IMAGE_TYPE)

i = 0

while i < TRAINING_LEN:
    label = int(next(training_labels))

    j = 0
    while j < SIZE:
        image[j] = np.fromstring(next(training_images)[:-1], dtype=np.uint8)
        j += 1

    image -= ord(' ')
    image[image > 0] = 1

    image_sums[:, :, label] += image
    label_sums[label] += 1
    i += 1

for i in xrange(10):
    image_sums[:, :, i] = (image_sums[:, :, i] + LAPLACE_K) / (label_sums[i] + LAPLACE_K * 10)
    #print image_sums[:, :, i]

image_nots = np.log(1 - image_sums)
image_sums = np.log(image_sums)
label_sums = np.log(label_sums / TRAINING_LEN)

#print label_sums

test_images = open('./digitdata/testimages')
test_labels = open('./digitdata/testlabels')

i = 0

while i < TEST_LEN:
    label = int(next(test_labels))

    j = 0
    while j < SIZE:
        image[j] = np.fromstring(next(test_images)[:-1], dtype=np.uint8)
        j += 1

    j = 0
    while j < 10:
        curr_sum = image_sums[:, :, j]
        curr_not = image_nots[:, :, j]

        test_sums[j] = sum(curr_sum[image != ord(' ')]) + sum(curr_not[image == ord(' ')]) + label_sums[j]

        j += 1

    new_label = np.argmax(test_sums)
    confusion_matrix[label, new_label] += 1
    score = max(test_sums)

    if score > highest_score[new_label]:
        highest_score[new_label] = score
        highest_match[:, :, new_label] = image
    if score < lowest_score[new_label]:
        lowest_score[new_label] = score
        lowest_match[:, :, new_label] = image

    i += 1

print confusion_matrix
print np.divide(np.diag(confusion_matrix).astype(np.float), np.sum(confusion_matrix, axis=1))

for i in xrange(10):
    for j in xrange(SIZE):
        print highest_match[j, :, i].tostring()
    print

for i in xrange(10):
    for j in xrange(SIZE):
        print lowest_match[j, :, i].tostring()
    print
