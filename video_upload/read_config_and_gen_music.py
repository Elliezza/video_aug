import os
import json, argparse
from file_size import *
from upload import *
import time
import subprocess

publish_name = [
{"id": "2000000022", "name": "慢悠悠的老张"},
{"id": "2000000023", "name": "风中的小猪猪"},
{"id": "2000000024", "name": "笑笑的疯狂旅行"},
{"id": "2000000025", "name": "小胖墩与大海"},
{"id": "2000000026", "name": "风中飘扬的叶子"},
{"id": "2000000027", "name": "轻舞飞扬的乐乐"},
{"id": "2000000028", "name": "叮当猫的世界"},
{"id": "2000000029", "name": "漫步在云端的喵"},
{"id": "2000000030", "name": "小林大世界"},
{"id": "2000000031", "name": "喜欢喝茶的李小姐"}
]

def select_name(rounds, choice):
    if rounds < 20:
        rounds += 1
    else:
        rounds = 0
        choice += 1
    return rounds, choice

def convert_video(input_file, output_file):
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            print(f"Removed temporary file: {output_file}")
        except OSError as e:
            print(f"Error removing temporary file: {e}")

    ffmpeg_path = "../ffmpeg/bin/ffmpeg.exe"
    command = [ffmpeg_path, '-i', input_file, '-c:v', 'libx264', output_file]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file} to {output_file}: {e}")



def load_config(config_file):
    """Load the configuration from a JSON file."""
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process videos.')
    parser.add_argument('-c', '--config_file', type=str, default='upload_content.json', help='Path to the JSON configuration file')
    parser.add_argument('-v', '--video_directory', type=str, default='./test_input', help='Path to the video files')
    parser.add_argument('-p', '--pic_directory', type=str, help='Path to the video screenshot files')

    args = parser.parse_args()
    config_file = args.config_file
    video_directory = args.video_directory
    if args.pic_directory:
        pic_directory = args.pic_directory
    else:
        pic_directory = video_directory

    configs = load_config(config_file)

    print(f"视频目录: {video_directory}")
    print(f"截图目录: {pic_directory}")

    rounds, choice = 0, 0
    for config in configs:
        file_title = config.get('file_title')
        title = config.get('title')
        content = config.get('content')
        # Print the extracted information (or use it as needed)
        print(f"视频名称: {file_title}")

        file_path = os.path.join(video_directory, file_title)
        screenshot_path = os.path.join(pic_directory, os.path.splitext(file_title)[0]+'.jpg')
        if os.path.exists(file_path) and os.path.exists(screenshot_path):
            print("File exists")
            continue
        else:
            print("No File found, skipping")
            #print(f"视频名称: {file_title}")
            print("-------------ERROR--------------")
            continue 

        print("Continue to work")

        #convert_video(file_path,"temp.mp4")
        #video_url = upload_with_retry("temp.mp4", "video")
        #img_url = upload_with_retry(screenshot_path, "img")
        video_url = upload_with_retry(file_path, "video")
        img_url = upload_with_retry(screenshot_path, "img")

        if video_url == None or img_url == None:
            print(file_path)
            print("Fail to upload, skipping.....")
            continue

        #video_url = "https://cn-material-bucket.oss-cn-shenzhen.aliyuncs.com/res/video/11_ee2e5eb080c8f2fd.mp4"
        #img_url = "https://cn-material-bucket.oss-cn-shenzhen.aliyuncs.com/res/img/66_ee2e5eb080c8f2fd.jpg"
        #file_size = get_file_size("temp.mp4")
        #video_duration = get_video_duration("temp.mp4")
        file_size = get_file_size(file_path)
        video_duration = get_video_duration(file_path)
        
        print(file_size)
        print(video_duration)


        rounds, choice = select_name(rounds, choice)

        video_entry = {
    "itemType":"视频",
    "url": video_url,
    "country":"中国",
    "language":"中文",
    "title": title,
    "content": "",
    "duration": video_duration,
    "format":"mp4", 
    "size":file_size,
    "categoryLevel1":"2", 
    "categoryLevel2":"2",
    "coverUrl":img_url,
    "publishId": publish_name[choice]['id'],
    "publishName": publish_name[choice]['name'],
    "publishTime":int(time.time()*1000),
    "itemTime":int(time.time()*1000),
    "itemStatus":1,
    "province":"北京",
    "city":"北京", 
    "source":"自产",

    }
        print(video_entry)
        res = upload_entry_with_retry(video_entry)
        print(res)
                
                
                


