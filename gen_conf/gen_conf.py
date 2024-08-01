import json
from llm import call_llm
import random

temp_subtitle = ''
temp_color = ''
temp_title = ''

colors = ["#A6CF85", "#E6526F", "#6B477C", "#E94F6F", "#FF6F4F", "#F8C471", "#9AE3A1", "#7DC6C6", "#5C9BCC", "#A76B8D", "#D77F9D", "#FF8C6C", "#6EC6D8"]

max_n = len(colors) - 1


def random_color():
    color = colors[random.randint(0, max_n)]
    print(color)
    return color

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
            "background_color": random_color(),
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
            "【舞蹈】【横】【英】【1M】Woomin-Jang编舞《Nice-For-What》.mp4.mp4",
"【舞蹈】【横】【英】【1M基础】Isabelle编舞Nice-For-What.mp4.mp4",
"【舞蹈】【横】【英】《巴赫的最后一天》堪称为世界上最美芭蕾！舞者PolinaSemionova-太美了必须分享给大家！.mp4.mp4",
"【舞蹈】【横】【英】【王炸组合】In-Two---Antonio-Casalinho---Madison-Penney.mp4.mp4",
"【舞蹈】【横】【英】【王炸组合】La-Fille-Mal-Gardee-PDD-关不住的女儿大双---Madison-Penney---Antonio-Casalinho.mp4.mp4",
"【舞蹈】【横】【英】【王炸组合】Le-Corsaire-PDD-海盗大双---Madison-Penney---Antonio-Casalinho.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Amber-Skaggs--Madison-Penney-and-Jaycee-Wilkins--Trio---YAGP-2014.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Reina-Stamm---AreYouThere---YAGP-2016-NYC.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Reina-Stamm---Going-Home-Contemporary-Solo-2017.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Reina-Stamm---Reverance---Jump-Phoenix---HD.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Reina-Stamm，Ryan-Williams---Satrry-Night---YAGP-2017.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Reina-Stamm---Springs-Awakening---YAGP-2017-NYC-Finals.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Remie-Goins--“Body-Language”（踩点舒适！.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】Remie-Goins---With-a-Sparrow---YAGP-NYC-Finals.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】天才少女Madison-Penney---Sayuris.mp4.mp4",
"【舞蹈】【横】【英】【现代芭蕾】天才少女Madison-Penney---Speed-Limit.mp4.mp4",
"【舞蹈】【横】【英】经典芭蕾舞剧《葛蓓莉亚》一幕变奏｜这段表演太轻盈灵动了，小姑娘的身材一看就是芭蕾的好苗子！.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】11岁Martha-Savin---YAGP-2019-Hope-Award-Winner.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】4k-洛桑大奖选手Antonio-Casalinho堂吉诃德三幕大双人舞.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Elisabeth-Beyer-“百万小丑”女变奏-Variation-from-Harle.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Madison-Penney---Giselle-吉赛尔女变奏---YAGP-2017.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Reina-Stamm---Don-Quixote-Kitri-堂吉诃德女变奏---YAGP-2016-NYC.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Reina-Stamm---Giselle---Act-1-Variation-吉赛尔女变奏.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Reina-Stamm---Kitri-Act-1-Variation-堂吉诃德女变奏--IBC-2015.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Reina-Stamm----La-Esmeralda-Variation-艾斯米拉达变奏.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Reina-Stamm---La-Fille-Mal-Gardee-关不住的女儿女变奏---IBC-2014.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Reina-Stamm，Ryan-Williams---Satanella-Pas-De-Deux.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Reina-Stamm---Swanilda-Variation-葛蓓利亚女变奏.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Remie-Goins---La-Fille-Mal-Gardee--YAGP-2019.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】Remie-Goins---Medora-Variation---YAGP-2018.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾_圣诞特辑】《胡桃夹子》糖果仙子之舞.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】天才少女Madison-Penney-The-Grey-Of-The-Sky--YAGP-2019.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】天才少女Madison-Penney--堂吉诃德婚礼女变奏---WBC-2015.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】我见过最美的《绿宝石》西西里变奏独舞-Clairemarie-Osta.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】油管两千万播放《胡桃夹子》糖果仙子之舞---Nina-Kaptsova妮娜·卡普索娃.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】王炸组合！Madison-Penney---Antonio-Casalinho---古典大双--YAGP-2019-NYC-Finals.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾舞】YAGP-2019美国青年大奖赛--西雅图半决赛Tillie-Vassar.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】艾斯美拉达女变奏---Elisabeth-Beyer.mp4.mp4",
"【舞蹈】【横】【英】【芭蕾】诡异的人偶之舞-Maria-Eichwald-斯图加特芭蕾舞团.mp4.mp4",
"【舞蹈】【横】【英】【防弹少年团】《Butter》官方练习室公开！.mp4.mp4"
    ]

    configs = []

    for t in video_titles:
        config = gen_config(t)
        configs.append(config)

    with open(config_out, 'w', encoding='utf-8') as file:
        json.dump(configs, file, ensure_ascii=False, indent=4)
