# atlas-project

## Goal

The goal of this project is to recreate the functionality of the <a href="https://knowledge.brain-map.org/abcatlas">ABC atlas</a>, with some few customized actions for the Zorrilla lab. Actions include: 
* Filtering for brain regions (e.g. nucleus accumbens)
* Discovering coexpressed genes after selecting genes of interest
* Exploring what cell types are expressed

## Install
### Dependencies
* Docker

### Build
In your terminal, go to your preferred directory and clone the repo:
```git clone https://github.com/zorrilla-lab/atlas-project.git```

Install the package requirements:
```
cd atlas-project
docker compose up --build
```

## Resources

https://alleninstitute.github.io/abc_atlas_access/intro.html

MERSCOPE Dataset: Michael Kunst, Delissa McMillen, Jennie Close, Jazmin Campos, Madie Hupp, Naomi Martin, Jocelin Malone, Zoe Maltzer, Augustin Ruiz, Nasmil Valera Cuevas, Brian Long, Jack Waters, Hongkui Zeng. (2023). Whole Mouse Brain Transcriptomic Cell Type Atlas - MERSCOPE v1. [Dataset]. Available from https://doi.org/10.35077/g.610

Dataset:  A molecularly defined and spatially resolved cell atlas of the whole mouse brain [Dataset]. Available at Brain Image Library (BIL): https://doi.org/10.35077/act-bag
