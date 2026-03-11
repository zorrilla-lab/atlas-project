from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from scripts.visualize import plot_coexpressed_genes, plot_pie
import scripts.cache as cache
import time

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/update_visualization", methods=["POST"])
def update_visualization():
    start = time.time()
    goi = request.json.get("gene")
    dataset = request.json.get("dataset")

    print(f"gene and dataset received.")
    
    cells = cache.get_cells(dataset)
    em = cache.get_em(dataset)
    goi_idx = cache.get_gene_to_idx(goi, dataset)
    
    goi_rows = em['presence'][:, goi_idx].nonzero()[0]
    goi_cells = set(em['obs_names'][goi_rows])
    cell_info = cells[cells.index.isin(goi_cells)]

    coexp_path = plot_coexpressed_genes(goi, em['coexpression'])
    class_path = plot_pie(cell_info, "class")
    subclass_path = plot_pie(cell_info, "subclass")
    supertype_path = plot_pie(cell_info, "supertype")

    finish = time.time()
    print(f"done plotting in {finish - start} seconds.")

    return jsonify(
        {
            "coexp": coexp_path,
            "class": class_path,
            "subclass": subclass_path,
            "supertype": supertype_path,
        }
    )
