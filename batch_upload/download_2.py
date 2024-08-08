import requests
import os
from tqdm import tqdm
from time import sleep

def download_file_with_retry(url, save_dir, retries=3, delay=2):
    for attempt in range(retries):
        try:
            # Stream the response to handle large files
            with requests.get(url, stream=True) as response:
                response.raise_for_status()  # Ensure the request was successful

                # Extract the original file name from the URL
                filename = os.path.basename(url)
                save_path = os.path.join(save_dir, filename)

                # Get the total file size from headers (if available)
                total_size = int(response.headers.get('content-length', 0))

                # Write to file with progress
                with open(save_path, 'wb') as file, tqdm(
                    desc=filename,
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            bar.update(len(chunk))

                return save_path

        except requests.RequestException as e:
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                sleep(delay)  # Wait before retrying
            else:
                print("Max retries reached. Download failed.")
                raise e  # Re-raise the exception if out of retries

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed file: {file_path}")
    else:
        print(f"File not found: {file_path}")

# Example usage:
if __name__ == "__main__":
    url = "http://example.com/largefile.zip"
    save_dir = "./downloads"
    os.makedirs(save_dir, exist_ok=True)
    try:
        file_path = download_file_with_retry(url, save_dir)
        print(f"File downloaded to: {file_path}")
    except Exception as e:
        print(f"Failed to download file: {e}")

