import requests
import os
from time import sleep

def download_file(url, save_dir):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    filename = os.path.basename(url)
    save_path = os.path.join(save_dir, filename)

    with open(save_path, 'wb') as file:
        file.write(response.content)

    return save_path


def download_file_with_retry(url, save_dir, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure the request was successful

            # Extract the original file name from the URL
            filename = os.path.basename(url)
            save_path = os.path.join(save_dir, filename)

            with open(save_path, 'wb') as file:
                file.write(response.content)

            return save_path
        
        except requests.RequestException as e:
            if attempt < retries - 1:
                sleep(delay)  # Wait before retrying
            else:
                raise e  # Re-raise the exception if out of retries

