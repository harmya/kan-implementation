from flask import Flask, render_template, jsonify, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
import matplotlib
matplotlib.use('agg')


app = Flask(__name__)

def process_data(data):
    labels = {
        "red": [],
        "blue": [],
        "green": [],
        "gold": []
    }

    num_points = 0

    all_x = []
    all_y = []

    for val in data:
        color = val.get("color")
        if color in labels:
            num_points += 1
            x, y = val["x"], val["y"]
            labels[color].append([x, y])
            all_x.append(x)
            all_y.append(y)
    
    if all_x and all_y:
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
    else:
        min_x, max_x, min_y, max_y = 0, 1, 0, 1

    def scale_point(point):
        scaled_x = 10 * (point[0] - min_x) / (max_x - min_x) if max_x != min_x else 0
        scaled_y = 10 * (point[1] - min_y) / (max_y - min_y) if max_y != min_y else 0
        return [scaled_x, scaled_y]

    for color in labels:
        if len(labels[color]) != 0:
            labels[color] = np.array([scale_point(pt) for pt in labels[color]])
        else:
            labels[color] = np.array([[21, 21]])
    
    return labels["red"], labels["blue"], labels["green"], labels["gold"], num_points


def make_meshgrid():
    x = np.linspace(-1, 11, 60)
    y = np.linspace(-1, 11, 60)
    xx, yy = np.meshgrid(x, y)
    return xx, yy

import numpy as np

def classify_meshgrid(xx, yy, center_one, center_two, center_three, center_four, num_points, k=3):
    grid = np.c_[xx.ravel(), yy.ravel()]
    output = []
    for point in grid:
        distance_one = np.linalg.norm(point - center_one, axis=1)
        distance_one = np.c_[distance_one, np.ones(len(center_one))]
        
        distance_two = np.linalg.norm(point - center_two, axis=1)
        distance_two = np.c_[distance_two, np.ones(len(center_two)) * 2]

        distance_three = np.linalg.norm(point - center_three, axis=1)
        distance_three = np.c_[distance_three, np.ones(len(center_three)) * 3]

        distance_four = np.linalg.norm(point - center_four, axis=1)
        distance_four = np.c_[distance_four, np.ones(len(center_four)) * 4]

        distance = np.concatenate([distance_one, distance_two, distance_three, distance_four])

        if point[0] > 390 and point[1] > 390:
            print(distance)
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


@app.route("/")
def index():
    return render_template("graph.html")

@app.route("/plot", methods=["POST"])
def plot():
    center_one, center_two, center_three, center_four, num_points = process_data(request.get_json())
    
    plt.figure(figsize=(5, 5))
    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    
    if len(center_one) != 0:
        plt.scatter(center_one[:, 0], center_one[:, 1], c='r', label='Center 1')
    if len(center_two) != 0:
        plt.scatter(center_two[:, 0], center_two[:, 1], c='b', label='Center 2')
    if len(center_three) != 0:
        plt.scatter(center_three[:, 0], center_three[:, 1], c='g', label='Center 3')
    if len(center_four) != 0:
        plt.scatter(center_four[:, 0], center_four[:, 1], c='y', label='Center 4')
    
    xx, yy = make_meshgrid()
    labels = classify_meshgrid(xx, yy, center_one, center_two, center_three, center_four, num_points, k=5)
    plt.contourf(xx, yy, labels, alpha=0.5, cmap='viridis')
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_data = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()

    plt.savefig('static/plot.png')
    return jsonify({"img_data": img_data})

if __name__ == "__main__":
    app.run(debug=True)
