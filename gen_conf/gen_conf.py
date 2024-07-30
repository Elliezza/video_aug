import json
from llm import call_llm

temp_subtitle = ''
temp_color = ''
temp_title = ''

def read_prompts(prompt_subtitle, prompt_color, prompt_title):
    global temp_subtitle
    global temp_color
    global temp_title

    with open(prompt_subtitle, 'r', encoding='utf-8') as file:
        temp_subtitle = file.read()
    with open(prompt_color, 'r', encoding='utf-8') as file:
        temp_color = file.read()
    with open(prompt_title, 'r', encoding='utf-8') as file:
        temp_title = file.read()

def update_prompt(template, replace_name):
    prompt = template.replace('$FILE_NAME', replace_name)
    return prompt

def gen_config(t):
    config = {
            "video_name": t,
            "background_color": call_llm(update_prompt(temp_color, t)),
            "output_directory": "output",
            "font_path":"font.ttf",
            "title":  json.loads(call_llm(update_prompt(temp_title, t))),
            "subtitle": call_llm(update_prompt(temp_subtitle, t))

            }
    return config


if __name__ == "__main__":
    config_out = "config.json"
    prompt_subtitle = "prompt.txt"
    prompt_color = "prompt_color.txt"
    prompt_title = "prompt_title.txt"

    read_prompts(prompt_subtitle, prompt_color, prompt_title)
    video_titles = [
    '【维密】【英】【横】【维密盘点】VSFS2018“新面孔”合集初次上秀表现力大对比_ ).mp4.(2).mp4',
    '【舞蹈】【横】【英】【芭蕾】油管两千万播放《胡桃夹子》糖果仙子之舞NinaKaptsova妮娜·卡普索娃.mp4.mp4',
    '【音乐现场】【英文】【横屏】《VivaLaVida》神级现场，万人合唱，大千世界由我主宰！.mp4',
    ]

    configs = []

    for t in video_titles:
        config = gen_config(t)
        configs.append(config)

    with open(config_out, 'w', encoding='utf-8') as file:
        json.dump(configs, file, ensure_ascii=False, indent=4)
