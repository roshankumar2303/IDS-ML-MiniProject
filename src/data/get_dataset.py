from download_file import download

url = 'https://cloudstor.aarnet.edu.au/plus/s/ds5zW91vdgjEj9i/download?path=%2FProcessed_datasets%2FProcessed_Windows_dataset&files=windows10_dataset.csv'
target_file_name = 'data/external/ton-iot-windows-10.csv'

download(url, target_file_name)