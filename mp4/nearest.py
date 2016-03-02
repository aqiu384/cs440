import numpy as np
import matplotlib.pyplot as plt

def mode(a, axis=0):
    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)

    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent

    return np.int32(mostfrequent[0])

SIZE = 28
TRAINING_LEN = 5000
TEST_LEN = 1000
IMAGE_TYPE = np.float
LAPLACE_K = 1

np.set_printoptions(precision=8, linewidth=200)
confusion_matrix = np.zeros((10, 10), dtype=np.uint16)

images = np.zeros((TRAINING_LEN, SIZE ** 2), dtype=np.int32)
labels = np.empty(TRAINING_LEN, dtype=np.uint8)

training_images = open('./digitdata/trainingimages')
training_labels = open('./digitdata/traininglabels')

i = 0

while i < TRAINING_LEN:
    labels[i] = int(next(training_labels))

    j = 0
    while j < SIZE:
        images[i, j*SIZE:(j+1)*SIZE] = np.fromstring(next(training_images)[:-1], dtype=np.uint8)
        j += 1

    i += 1

images -= ord(' ')
images[images > 0] = 1
images[images == 0] = -1

image = np.zeros(SIZE ** 2, dtype=np.int32)

test_images = open('./digitdata/testimages')
test_labels = open('./digitdata/testlabels')

K_CONSTANT = 5
i = 0

# TEST_LEN
while i < TEST_LEN:
    label = int(next(test_labels))

    j = 0
    while j < SIZE:
        image[j*SIZE:(j+1)*SIZE] = np.fromstring(next(test_images)[:-1], dtype=np.uint8)
        j += 1

    image -= ord(' ')
    image[image > 0] = 1
    image[image == 0] = -1

    guess_label = mode(labels[np.argsort(np.dot(images, image))[-K_CONSTANT:]])
    confusion_matrix[label, guess_label] += 1

    i += 1

print confusion_matrix
print np.divide(np.diag(confusion_matrix).astype(np.float), np.sum(confusion_matrix, axis=1))
