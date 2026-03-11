import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64


def plot_coexpressed_genes(goi, coexpression_matrix):
    print("plot_coexpressed_genes function entered.")

    coexpressed_genes = coexpression_matrix[goi].drop(goi)

    print("coexpressed genes found. plotting.")

    fig, ax = plt.subplots()
    top_10 = coexpressed_genes.sort_values(ascending=False)[:10]

    ax.barh(top_10.index, top_10.to_list())
    ax.set_title(f"{goi} Coexpressed Genes")

    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches="tight", transparent=True, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64


def plot_pie(cell_info, variable):
    print("plot_pie function entered.")
    fig, ax = plt.subplots()

    class_distribution = cell_info[variable].value_counts()
    ax.pie(
        class_distribution.to_list(), labels=class_distribution.index, autopct="%1.1f%%"
    )

    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches="tight", transparent=True, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64
