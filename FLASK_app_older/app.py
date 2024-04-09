from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rows = request.form.get('rows')
        cols = request.form.get('cols')
        matrix_str = request.form.get('matrix')
        taxa_str = request.form.get('taxa')
        linkage_method = request.form.get('linkage_method')
        try:
            rows = int(rows)
            cols = int(cols)
            matrix = np.array([list(map(float, row.split(','))) for row in matrix_str.split('\n') if row.strip()])
            taxa = [taxon.strip() for taxon in taxa_str.split(',') if taxon.strip()]
            if matrix.shape != (rows, cols):
                return render_template('index.html', error='Matrix dimensions do not match specified rows and columns.')
            if len(taxa) != rows:
                return render_template('index.html', error='Number of taxa does not match the number of rows in the matrix.')
            fig, ax = plt.subplots(figsize=(6, 8))
            Z = linkage(matrix, linkage_method)
            dendrogram(Z, labels=taxa, orientation='top', ax=ax)
            plt.tight_layout()

            # Save the plot image to a BytesIO object
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)

            # Encode the image data to base64
            img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

            return render_template('index.html', tree_image=img_data)
        except ValueError:
            return render_template('index.html', error='Invalid input. Please check the matrix format and taxa names.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
