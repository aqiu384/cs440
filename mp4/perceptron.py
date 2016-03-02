import numpy as np
import matplotlib.pyplot as plt

SIZE = 28
TRAINING_LEN = 5000
TEST_LEN = 1000
IMAGE_TYPE = np.float
LAPLACE_K = 1

np.set_printoptions(precision=8, linewidth=200)
confusion_matrix = np.zeros((10, 10), dtype=np.uint16)

images = np.zeros((TRAINING_LEN, SIZE ** 2 + 1), dtype=np.uint8)
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

perceptrons = np.zeros((10, SIZE ** 2 + 1))

DECAY = float(1000)
EPOCHS = 100

accuracy = np.empty(EPOCHS)
np.random.seed(0)

for epoch in xrange(EPOCHS):
    alpha = DECAY / (DECAY + epoch)
    correct_labels = TRAINING_LEN

    for i in np.random.permutation(TRAINING_LEN):
        image = images[i]
        label = labels[i]

        guess_label = np.argmax(np.dot(perceptrons, image))

        if label != guess_label:
            correct_labels -= 1
            perceptrons[label] += alpha * image
            perceptrons[guess_label] -= alpha * image

    accuracy[epoch] = correct_labels
    print correct_labels

test_images = open('./digitdata/testimages')
test_labels = open('./digitdata/testlabels')

plt.plot(accuracy / TRAINING_LEN)

i = 0

while i < TEST_LEN:
    label = int(next(test_labels))

    j = 0
    while j < SIZE:
        image[j*SIZE:(j+1)*SIZE] = np.fromstring(next(test_images)[:-1], dtype=np.uint8)
        j += 1

    image -= ord(' ')
    image[image > 0] = 1

    guess_label = np.argmax(np.dot(perceptrons, image))
    confusion_matrix[label, guess_label] += 1

    i += 1

print confusion_matrix
print np.divide(np.diag(confusion_matrix).astype(np.float), np.sum(confusion_matrix, axis=1))

plt.show()