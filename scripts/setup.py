from pathlib import Path
import pandas as pd
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache
import os
import anndata as ad
import scipy.sparse as sp
import argparse
import time

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--overwrite", action="store_true")
args = parser.parse_args()
print(f"Overwrite: {args.overwrite}")

# load data from abc_atlas
download_base = Path("./data")
abc_cache = AbcProjectCache.from_cache_dir(download_base)
abc_cache.get_directory_metadata("WMB-taxonomy")

# parse data
cluster_colors_path = Path(
    "data/metadata/WMB-taxonomy/20231215/views/cluster_to_cluster_annotation_membership_color.csv"
)
cluster_details_path = Path(
    "data/metadata/WMB-taxonomy/20231215/views/cluster_to_cluster_annotation_membership_pivoted.csv"
)
cluster_colors = pd.read_csv(cluster_colors_path)
cluster_details = pd.read_csv(cluster_details_path)

datasets = ["Zhuang-ABCA-1", "Zhuang-ABCA-2", "Zhuang-ABCA-3", "Zhuang-ABCA-4"]

for d in datasets:
    cells_path = Path(f"data/cells/{d}/{d}-cells.parquet")
    coexp_path = Path(f"data/coexp/{d}-coexp.parquet")
    presence_path = Path(f"data/presence/{d}-presence.npz")
    obs_path = Path(f"data/obs/{d}-obs.parquet")
    var_path = Path(f"data/var/{d}-var.parquet")

    # make directory if doesn't exist
    os.makedirs(cells_path.parent, exist_ok=True)
    os.makedirs(coexp_path.parent, exist_ok=True)
    os.makedirs(presence_path.parent, exist_ok=True)
    os.makedirs(obs_path.parent, exist_ok=True)
    os.makedirs(var_path.parent, exist_ok=True)

    # if setup has already been done, skip
    if (
        all(
            p.exists()
            for p in [cells_path, coexp_path, presence_path, obs_path, var_path]
        )
        and not args.overwrite
    ):
        continue

    abc_cache.get_directory_metadata(directory=d)
    abc_cache.get_directory_metadata(directory=f"{d}-CCF")
    abc_cache.get_file_path(directory=f"{d}", file_name=f"{d}/log2")

    metadata_path = Path(f"data/metadata/{d}/20241115/cell_metadata.csv")
    ccf_path = Path(f"data/metadata/{d}-CCF/20230830/ccf_coordinates.csv")
    metadata = pd.read_csv(metadata_path)
    ccf_df = pd.read_csv(ccf_path)

    df = (
        metadata.merge(cluster_details, on="cluster_alias")
        .merge(cluster_colors, on="cluster_alias")
        .merge(ccf_df, on="cell_label", suffixes=(None, "_ccf"))
    )
    df.set_index("cell_label").to_parquet(cells_path)

    em_path = Path(f"data/expression_matrices/{d}/20230830/{d}-log2.h5ad")
    em = ad.read_h5ad(em_path)
    em_matrix = sp.csc_matrix(em.X)

    presence = em_matrix > 0
    coexp = pd.DataFrame(
        (em_matrix.T @ em_matrix).toarray(),
        index=em.var["gene_symbol"],
        columns=em.var["gene_symbol"]
    )

    pd.Series(em.obs_names, name="cell_label").to_frame().to_parquet(obs_path)
    em.var[["gene_symbol"]].to_parquet(var_path)
    coexp.to_parquet(coexp_path)
    sp.save_npz(presence_path, presence)

    del em, em_matrix, presence, coexp
    print(f"done with {d}.")

finish = time.time()
print(f'setup done in {finish - start} seconds.')