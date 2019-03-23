import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('60deg.png')

rows, cols, ch = img.shape

# src = np.float32([[300 // 2, 1920 // 2], [918 // 2, 1051 // 2], [548 // 2, 480 // 2], [1674 // 2, 1058 // 2]])
#
# dst = np.float32([[580 // 2, 1920 // 2], [580 // 2, 434 // 2], [580 // 2, 434 // 2], [354, 1920 // 2]])

src = np.float32([[300 // 2, 1920 // 2], [918 // 2, 1051 // 2], [1674 // 2, 1058 // 2], [2260 // 2, 1920 // 2]]) * 2

dst = np.float32([[980 // 2, 1920 // 2], [980 // 2, 367 // 2], [1580 // 2, 367 // 2], [1580 // 2, 1920 // 2]]) * 2

M = cv2.getPerspectiveTransform(src, dst)

transformed = cv2.warpPerspective(img, M, (cols, rows))

# cv2.imshow("hi", transformed)
# cv2.waitKey(0)

plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(transformed)
plt.show()

