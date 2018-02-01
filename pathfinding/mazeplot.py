import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys

img = mpimg.imread(sys.argv[1], format='png')

test = []

x = img.shape[0]
y = img.shape[1]

for i in range(x):
	test.append([])
	for j in range(y):
		test[i].append(img[i][j][0])

plt.imshow(test)
plt.show()