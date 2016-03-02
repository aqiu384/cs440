import numpy as np
import matplotlib.pyplot as plt
import cv2

sprites = cv2.imread('sprites/pacman_sprite.png', cv2.IMREAD_GRAYSCALE )

plt.imshow(sprites[163:179, 253:268], 'gray')
plt.show()