import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def make_data(num_points=8):
    center_one = np.random.rand(num_points,2) * 5
    center_two = np.random.rand(num_points,2) * 5 + 5
    center_three = np.random.rand(num_points,2) * 5 + np.array([[5, 0]])
    center_four = np.random.rand(num_points,2) * 5 + np.array([[0, 5]])

    return center_one, center_two, center_three, center_four

def make_meshgrid():
    x = np.linspace(-1, 11, 60)
    y = np.linspace(-1, 11, 60)
    xx, yy = np.meshgrid(x, y)
    return xx, yy

def classify_meshgrid(xx, yy, center_one, center_two, center_three, center_four, k=3, num_points=8):
    grid = np.c_[xx.ravel(), yy.ravel()]
    output = []
    for point in grid:
        distance_one = np.linalg.norm(point - center_one, axis=1)
        distance_one = np.c_[distance_one, np.ones(num_points)]
        
        distance_two = np.linalg.norm(point - center_two, axis=1)
        distance_two = np.c_[distance_two, np.ones(num_points) * 2]

        distance_three = np.linalg.norm(point - center_three, axis=1)
        distance_three = np.c_[distance_three, np.ones(num_points) * 3]

        distance_four = np.linalg.norm(point - center_four, axis=1)
        distance_four = np.c_[distance_four, np.ones(num_points) * 4]

        distance = np.concatenate([distance_one, distance_two, distance_three, distance_four])
        
        sorted_index = np.argsort(distance[:, 0])
        distance = distance[sorted_index]

        k_nearest = distance[:k, :]

        distances = k_nearest[:, 0]
        labels = k_nearest[:, 1]

        unique_labels, counts = np.unique(labels, return_counts=True)
        max_votes = np.max(counts)

        labels_with_max_votes = unique_labels[counts == max_votes]

        winner = None

        if len(labels_with_max_votes) == 1:
            winner = labels_with_max_votes[0]
        else:
            mask = np.isin(labels, labels_with_max_votes)
            tied_labels = k_nearest[mask]
            winner = tied_labels[np.argmin(tied_labels[:, 0])][1]

        output.append(winner)

    return np.array(output).reshape(xx.shape)

def plot_knn():
    num_points = 32
    xx, yy = make_meshgrid()
    center_one, center_two, center_three, center_four = make_data(num_points)
    
    plt.scatter(center_one[:, 0], center_one[:, 1], c='r', label='Center 1')
    plt.scatter(center_two[:, 0], center_two[:, 1], c='b', label='Center 2')
    plt.scatter(center_three[:, 0], center_three[:, 1], c='g', label='Center 3')
    plt.scatter(center_four[:, 0], center_four[:, 1], c='y', label='Center 4')
    
    labels = classify_meshgrid(xx, yy, center_one, center_two, center_three, center_four, k=7, num_points=num_points)
    plt.contourf(xx, yy, labels, alpha=0.2, cmap='viridis')
    plt.title('K-NN Classification')
    
    plt.show()

plot_knn()