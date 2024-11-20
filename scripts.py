import numpy as np
import matplotlib.pyplot as plt


num_points = 32

class_one = np.random.rand(num_points, 2) * 5
class_two = np.random.rand(num_points, 2) * 5 + 5
class_three = np.random.rand(num_points, 2) * 5 + np.array([[5, 0]])
class_four = np.random.rand(num_points, 2) * 5 + np.array([[0, 5]])

plt.scatter(class_one[:, 0], class_one[:, 1], c='r')
plt.scatter(class_two[:, 0], class_two[:, 1], c='b')
plt.scatter(class_three[:, 0], class_three[:, 1], c='g')
plt.scatter(class_four[:, 0], class_four[:, 1], c='y')

plt.show()

