import argparse
import json
import os
from llm import call_llm


temp_title=''
temp_content=''

def load_config(config_file):
    """Load the configuration from a JSON file."""
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def update_prompt(template, replace_name):
    prompt = template.replace('$FILE_NAME', replace_name)
    return prompt

def gen_config(t,outfile):
    config = {
            "file_title": outfile,
            "title":  call_llm(update_prompt(temp_title, t)),
            "content":  call_llm(update_prompt(temp_content, t)),
            }
    return config

def read_prompts(prompt_content, prompt_title):
    global temp_title
    global temp_content

    with open(prompt_title, 'r', encoding='utf-8') as file:
        temp_title = file.read()
    with open(prompt_content, 'r', encoding='utf-8') as file:
        temp_content = file.read()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process videos.')
    parser.add_argument('-c', '--config_file', type=str, default='config.json', help='Path to the JSON configuration file')
    args = parser.parse_args()
    config_file = args.config_file
    configs = load_config(config_file)

    upload_content = "upload_content.json"
    prompt_content = "prompt_content.txt"
    prompt_title = "prompt_content_title.txt"

    read_prompts(prompt_content, prompt_title)
    upload_content_configs = []

    for config in configs:
        # Extract information from configuration
        video_name = config.get('video_name', './')
        outfile = config.get('file_title', video_name).replace(" ", "")
        new_config = gen_config(video_name, outfile)

        upload_content_configs.append(new_config)

        with open(upload_content, 'w', encoding='utf-8') as file:
            json.dump(upload_content_configs, file, ensure_ascii=False, indent=4)

