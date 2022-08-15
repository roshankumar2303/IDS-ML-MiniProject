import requests
from tqdm import tqdm

def download(url: str, target_file_name: str):
    res = requests.get(url, stream=True)
    total_size = int(res.headers.get("content-length", 0))

    print('\nDownloading to {}'.format(target_file_name))
    with open(target_file_name, "wb") as target_file, tqdm(
        desc="PROGRESS".format(target_file_name),
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for chunk in res.iter_content(chunk_size=1024):
            chunk_size = target_file.write(chunk)
            progress_bar.update(chunk_size)
    print('\n', end="")