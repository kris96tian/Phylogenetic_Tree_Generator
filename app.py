from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist
from biotite.sequence.phylo import neighbor_joining as nj
from biotite.sequence.graphics import plot_dendrogram
import io
import base64

app = Flask(__name__)

def create_distance_matrix(num_taxa, distances):
    distance_matrix = np.zeros((num_taxa, num_taxa))
    k = 0
    for i in range(num_taxa):
        for j in range(i + 1, num_taxa):
            distance_matrix[i][j] = distances[k]
            distance_matrix[j][i] = distances[k]
            k += 1
    return distance_matrix

def generate_dendrogram_plot(distance_matrix, labels, method):
    fig, ax = plt.subplots(figsize=(10, 5))
    condensed_distance = pdist(distance_matrix)
    linkage_result = sch.linkage(condensed_distance, method=method)
    sch.dendrogram(linkage_result, labels=labels, ax=ax)
    ax.set_title(f'{method.capitalize()} Dendrogram')
    ax.set_xlabel('Instances')
    ax.set_ylabel('Distance')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

def plot_nj(distance_matrix, taxa_names):
    tree = nj(distance_matrix)
    fig, ax = plt.subplots()
    plot_dendrogram(ax, tree, orientation='left', use_distances=True, labels=taxa_names, label_size=10, color='black', show_distance=True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

def calculate_distance_matrix(sequences):
    n = len(sequences)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            diff_count = sum(1 for a, b in zip(sequences[i], sequences[j]) if a != b)
            distance_matrix[i][j] = distance_matrix[j][i] = diff_count
    return distance_matrix

def generate_max_par(distance_matrix, labels, method):
    fig, ax = plt.subplots(figsize=(10, 5))
    condensed_distance = pdist(distance_matrix)
    linkage_result = sch.linkage(condensed_distance, method=method)
    sch.dendrogram(linkage_result, labels=labels, ax=ax)
    ax.set_title('Maximum Parsimony Tree')
    ax.set_xlabel('Instances')
    ax.set_ylabel('Distance')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hierarchical_clustering', methods=['GET', 'POST'])
def hierarchical_clustering():
    if request.method == 'POST':
        num_taxa = int(request.form['num_taxa'])
        taxa = [request.form[f'taxon_{i}'] for i in range(num_taxa)]
        distances = [float(request.form[f'distance_{i}_{j}']) for i in range(num_taxa) for j in range(i + 1, num_taxa)]
        distance_matrix = create_distance_matrix(num_taxa, distances)
        method = request.form['method']
        plot_url = generate_dendrogram_plot(distance_matrix, taxa, method)
        return render_template('result.html', plot_url=plot_url)
    return render_template('hierarchical_clustering.html')

@app.route('/neighbor_joining', methods=['GET', 'POST'])
def neighbor_joining():
    if request.method == 'POST':
        num_taxa = int(request.form['num_taxa'])
        taxa_names = [request.form[f'taxon_{i}'] for i in range(num_taxa)]
        distances = [float(request.form[f'distance_{i}_{j}']) for i in range(num_taxa) for j in range(i + 1, num_taxa)]
        distance_matrix = create_distance_matrix(num_taxa, distances)
        plot_url = plot_nj(distance_matrix, taxa_names)
        return render_template('result.html', plot_url=plot_url)
    return render_template('neighbor_joining.html')

@app.route('/maximum_parsimony', methods=['GET', 'POST'])
def maximum_parsimony():
    if request.method == 'POST':
        num_sequences = int(request.form['num_sequences'])
        sequences = [request.form[f'sequence_{i}'] for i in range(num_sequences)]
        distance_matrix = calculate_distance_matrix(sequences)
        plot_url = generate_max_par(distance_matrix, labels=[f'S{i + 1}' for i in range(num_sequences)], method='centroid')
        return render_template('result.html', plot_url=plot_url)
    return render_template('maximum_parsimony.html')

if __name__ == '__main__':
    app.run(debug=True)
