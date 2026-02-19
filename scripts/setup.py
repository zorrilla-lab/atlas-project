from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

download_base = Path('./data')
abc_cache = AbcProjectCache.from_cache_dir(download_base)

datasets = ['Zhuang-ABCA-1', 'Zhuang-ABCA-2', 'Zhuang-ABCA-3', 'Zhuang-ABCA-4']

for d in datasets :
  abc_cache.get_directory_metadata(directory=d)
  abc_cache.get_directory_metadata(directory=f'{d}-CCF')
    
abc_cache.get_directory_metadata('WMB-taxonomy')

abc_cache.get_file_path(directory='Zhuang-ABCA-1', file_name='Zhuang-ABCA-1/log2')