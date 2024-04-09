import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist
from biotite.sequence.phylo import neighbor_joining as nj
from biotite.sequence.graphics import plot_dendrogram
from Bio import Phylo

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    page_title="Phylogenetic Tree Builder",
    page_icon=":dna:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Clustering Methods:")

def ask_for_taxa(num_taxa):
    """
    asks user to enter names of the taxa.
    """
    taxa = []
    for i in range(num_taxa):
        taxon = st.text_input(f"Enter the name of taxa {i+1}: ")
        taxa.append(taxon)
    return taxa

def collect_distances(num_taxa):
    """
    asks the user to enter the distances between taxa.
    """
    distances = []
    for i in range(num_taxa):
        for j in range(i+1, num_taxa):
            distance = st.number_input(f"Enter the distance between taxa {i+1} and taxa {j+1}: ")
            distances.append(distance)
    return distances

def create_distance_matrix(num_taxa, distances):
    """
    build distance matrix from the user inputs.
    """
    distance_matrix = np.zeros((num_taxa, num_taxa))
    k = 0
    for i in range(num_taxa):
        for j in range(i+1, num_taxa):
            distance_matrix[i][j] = distances[k]
            distance_matrix[j][i] = distances[k]
            k += 1
    return distance_matrix

def ask_for_clustering_method():
    """
    asks the user to select a clustering method.
    """
    methods = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']
    method = st.selectbox("Select clustering method", methods)
    return method

def generate_dendrogram_plot(distance_matrix, labels, method):
    """
    Generates and displays a dendrogram plot for the given distance matrix and clustering method.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    condensed_distance = pdist(distance_matrix)
    linkage_result = sch.linkage(condensed_distance, method=method)
    dendrogram = sch.dendrogram(linkage_result, labels=labels)
    ax.set_title(f'{method.capitalize()} Dendrogram')
    ax.set_xlabel('Instances')
    ax.set_ylabel('Distance')
    st.pyplot(fig)

def plot_nj(distance_matrix, taxa_names):
    # Apply Neighbor-Joining algorithm
    tree = nj(distance_matrix)
   
    fig, ax = plt.subplots() 
    plot_dendrogram(ax, tree, orientation='left', use_distances=True, labels=taxa_names, label_size=10, color='black', show_distance=True)

    st.pyplot(fig)

def calculate_distance_matrix(sequences):
    n = len(sequences)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            diff_count = sum(1 for a, b in zip(sequences[i], sequences[j]) if a != b)
            distance_matrix[i][j] = distance_matrix[j][i] = diff_count
    return distance_matrix

def generate_max_par(distance_matrix, labels, method):
    """
    Generates and displays a dendrogram plot for the calculated edit distanzes
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    condensed_distance = pdist(distance_matrix)
    linkage_result = sch.linkage(condensed_distance, method=method)
    dendogram = sch.dendrogram(linkage_result, labels=labels)
    ax.set_title(f'Maximum Parsimony Tree')
    ax.set_xlabel('Instances')
    ax.set_ylabel('Distance')
    st.pyplot(fig)

def maximum_parsimony(sequences):
    # Calculate edit distance matrix
    distance_matrix = calculate_distance_matrix(sequences)

    generate_max_par(distance_matrix, labels=[f'S{i}' for i in range(1, len(sequences) + 1)], method='centroid')

def main():
    st.title("Phylogenetic Tree Builder")

    analysis_type = st.sidebar.selectbox("Select Method/Algorithm", ["Hierarchical Clustering", "Neighbor-Joining", "Maximum Parsimony"])

    if analysis_type == "Hierarchical Clustering":
        st.header("Hierarchical Clustering")
        st.markdown("Hierarchical clustering is a method of cluster analysis that builds a hierarchy of clusters. It starts by treating each data point as a single cluster and then repeatedly merges the closest pairs of clusters until all data points are in a single cluster. Methodes you can choose are 'single', 'complete', 'average' also known as UPGMA, 'weighted', 'centroid', 'median' and 'ward'.")
        num_taxa = st.number_input("Enter the number of taxa:", min_value=2, step=1, value=2)
        taxa = ask_for_taxa(num_taxa)
        distances = collect_distances(num_taxa)
        distance_matrix = create_distance_matrix(num_taxa, distances)
        clustering_method = ask_for_clustering_method()

        if st.button("Generate Dendrogram"):
            generate_dendrogram_plot(distance_matrix, taxa, clustering_method)

    elif analysis_type == "Neighbor-Joining":
        st.header("Neighbor-Joining")
        st.markdown("The Neighbor-Joining algorithm is a bottom-up (agglomerative) clustering method for the creation of phylogenetic trees. The correctness of the output tree topology is guaranteed as long as the distance matrix is 'nearly additive'.")
        num_taxa = st.number_input("Enter the number of taxa:", min_value=2, step=1, value=2)
        taxa_names = ask_for_taxa(num_taxa)
        distances = collect_distances(num_taxa)
        distance_matrix = create_distance_matrix(num_taxa, distances)

        if st.button("Generate Neighbor-Joining Tree"):
            plot_nj(distance_matrix, taxa_names)

    elif analysis_type == "Maximum Parsimony":
        st.header("Maximum Parsimony")
        st.markdown("Maximum Parsimony is a method used to infer phylogenetic trees by minimizing the total number of evolutionary changes required to explain observed sequence data. It assumes that the most parsimonious tree, i.e., the tree with the fewest evolutionary changes, is the most likely.")
        num_sequences = st.number_input("Enter the number of DNA sequences:", min_value=2, step=1, value=2)
        sequences = []
        for i in range(num_sequences):
            sequence = st.text_input(f"Enter DNA sequence {i+1}: ")
            sequences.append(sequence)

        if st.button("Construct Phylogenetic Tree"):
            distance_matrix = calculate_distance_matrix(sequences)
            generate_max_par(distance_matrix, labels=[f'S{i}' for i in range(1, len(sequences) + 1)], method='centroid')

if __name__ == "__main__":
    main()
