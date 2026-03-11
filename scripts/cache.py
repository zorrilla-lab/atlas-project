from pathlib import Path
import anndata as ad
import pandas as pd
import scipy.sparse as sp

em_cache = {}
cells_cache = {}
gene_to_idx = {}


def get_em(dataset):
    if dataset not in em_cache:
        coexp = pd.read_parquet(f'data/coexp/{dataset}-coexp.parquet')
        presence = sp.load_npz(f'data/presence/{dataset}-presence.npz')
        obs_names = pd.read_parquet(f'data/obs/{dataset}-obs.parquet')
        gene_symbols = pd.read_parquet(f'data/var/{dataset}-var.parquet')

        em_cache[dataset] = {'coexpression': coexp, 'presence': presence, 'obs_names': obs_names}
        gene_to_idx[dataset] = {symbol: i for i, symbol in enumerate(gene_symbols)}
    return em_cache[dataset]


def get_cells(dataset):
    if dataset not in cells_cache:
        print(f"loading {dataset} into cache...")
        cells_path = Path(f"data/cells/{dataset}/{dataset}-cells.parquet")
        cells_cache[dataset] = pd.read_parquet(
            cells_path,
            columns=["class", "subclass", "supertype"],
            engine="pyarrow",
        )
    return cells_cache[dataset]


def get_gene_to_idx(goi, dataset):
    return gene_to_idx[dataset][goi]
