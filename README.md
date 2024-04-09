# Phylogenetic Tree Builder

Phylogenetic Tree Builder is a Python application built using Streamlit. It provides functionalities for constructing phylogenetic trees using various clustering methods and algorithms.

## Features

- **Hierarchical Clustering**: Perform hierarchical clustering analysis with different methods such as single, complete, average (UPGMA), weighted, centroid, median, and ward.
- **Neighbor-Joining**: Generate Neighbor-Joining trees, a bottom-up clustering method for creating phylogenetic trees.
- **Maximum Parsimony**: Infer phylogenetic trees by minimizing the total number of evolutionary changes required to explain observed sequence data.

## Usage

1. **Select Method/Algorithm**: Choose the desired clustering method or algorithm from the sidebar menu.
2. **Input Data**: Provide the required data based on the selected method:
   - For Hierarchical Clustering: Enter the number of taxa, taxa names, distances, and select a clustering method.
   - For Neighbor-Joining: Enter the number of taxa, taxa names, and distances.
   - For Maximum Parsimony: Enter the number of DNA sequences and input the sequences.
3. **Perform Analysis**: Click on the corresponding button to perform the analysis.
4. **Explore Results**: Explore the generated dendrogram plots, Neighbor-Joining trees, or Maximum Parsimony trees.

## Clustering Methods

- **Hierarchical Clustering**: Hierarchical clustering is a method of cluster analysis that builds a hierarchy of clusters by merging the closest pairs of clusters.
- **Neighbor-Joining**: The Neighbor-Joining algorithm is a bottom-up (agglomerative) clustering method for creating phylogenetic trees.
- **Maximum Parsimony**: Maximum Parsimony minimizes the total number of evolutionary changes required to explain observed sequence data.

## Technologies Used

- **Streamlit**: Used for building the user interface and hosting the application.
- **Python Libraries**: Including NumPy, Matplotlib, SciPy, Biotite, and BioPython for performing phylogenetic analysis and visualization.

## Contributing

Contributions are welcome! If you'd like to contribute to the Phylogenetic Tree Builder by adding new features, fixing bugs, or improving documentation, please open an issue or submit a pull request.

