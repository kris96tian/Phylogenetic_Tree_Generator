# Phylogenetic Tree Generator

This is a web application built with Flask that allows users to generate phylogenetic trees from distance matrices. It utilizes Python libraries like NumPy, Matplotlib, and SciPy for data manipulation, visualization, and hierarchical clustering.

[Visit the web app](https://clustering.pythonanywhere.com)


## Features
- **User Input**: Users can specify the number of rows and columns for the distance matrix, input the matrix data, provide taxa/node names, and select the desired linkage method.
- **Visualization**: The application generates a phylogenetic tree using the input data and displays it to the user.
- **Error Handling**: It performs input validation and provides appropriate error messages for invalid input.

## Linkage Methods
This application supports two linkage methods for hierarchical clustering:

### Single Linkage
Single linkage, also known as the nearest neighbor method, merges clusters based on the minimum distance between individual points in the clusters. It tends to produce elongated clusters and can be sensitive to outliers.

### UPGMA (Average Linkage)
UPGMA (Unweighted Pair Group Method with Arithmetic Mean) is a hierarchical clustering method that calculates the average distance between each pair of points in two clusters before merging them. It tends to produce more balanced clusters compared to single linkage.

## Dependencies
- Flask
- NumPy
- Matplotlib
- SciPy

