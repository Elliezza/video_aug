import cv2
import numpy as np
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import json, argparse

def create_solid_color_image(color_code, size=(720, 1280), output_path='solid_color.png'):
    """
    创建一个纯色背景图像。
    """
    if isinstance(color_code, str):
        color_code = color_code.lstrip('#')
        color_code = tuple(int(color_code[i:i+2], 16) for i in (0, 2, 4))

    image = Image.new("RGB", size, color_code)
    image.save(output_path)
    return output_path

def add_background_and_subtitle(video_path, background_color_code, output_path, title_text, subtitle_text, font_path):
    cap = cv2.VideoCapture(video_path)
    background_image_path = create_solid_color_image(background_color_code)
    background = cv2.imread(background_image_path)
    bg_height, bg_width = 1280, 720
    background = cv2.resize(background, (bg_width, bg_height))

    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = min(bg_width / video_width, bg_height / video_height)
    new_width = int(video_width * scale)
    new_height = int(video_height * scale)
    x_offset = (bg_width - new_width) // 2
    y_offset = (bg_height - new_height) // 2

    title_offset = max(0, y_offset - 200)
    subtitle_offset = min(y_offset + new_height + 100, bg_height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (bg_width, bg_height))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    subtitles = subtitle_text.split('&')
    subtitle_duration = (duration - 10) / len(subtitles)

    font_title = ImageFont.truetype(font_path, 50)
    font_subtitle = ImageFont.truetype(font_path, 36)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_time = current_frame / fps
        resized_frame = cv2.resize(frame, (new_width, new_height))
        combined_frame = background.copy()
        combined_frame[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized_frame

        # Add title
        title_frame = add_text_to_frame(combined_frame, title_text, font_title, (bg_width, 150), title_offset)

        # Add subtitles
        if current_time < duration :
            segment_index = int(current_time / subtitle_duration)
        else:
            segment_index = len(subtitles) - 1

        current_subtitle = subtitles[segment_index]
        combined_frame = add_subtitles(title_frame, current_subtitle, font_subtitle, bg_width, bg_height, subtitle_offset)
        out.write(combined_frame)

    cap.release()
    out.release()

def add_text_to_frame(frame, text, font, size, offset):
    """
    在图像上添加文本。
    """
    frame_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(frame_pil)
    
    y = offset
    for line in text:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (size[0] - text_width) // 2
        draw.text((text_x, y), line, font=font, fill=(255, 255, 255))
        y += bbox[3] - bbox[1] + 5

    return np.array(frame_pil)

def add_subtitles(frame, subtitle_text, font, bg_width, bg_height, offset):
    """
    在图像上添加字幕。
    """
    frame_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(frame_pil)
    lines = subtitle_text.split('^')
   
    y = offset
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (bg_width - text_width) // 2
        draw.text((text_x, y), line, font=font, fill=(255, 255, 255))
        y += bbox[3] - bbox[1] + 5  # Add some space between lines

    return np.array(frame_pil)

def extract_audio(video_path, audio_path):
    command = f"ffmpeg/bin/ffmpeg.exe -i {video_path} -q:a 0 -map a {audio_path}"
    subprocess.call(command, shell=True)

def combine_video_audio(video_path, audio_path, output_path):
    command = f"ffmpeg/bin/ffmpeg.exe -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}"
    subprocess.call(command, shell=True)

def process_videos(video_dir, video_filename, background_color_code, output_dir, title_text, subtitle_text, font_path):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
       
    if video_filename.endswith(('.mp4', '.mov', '.avi')):
        video_path = os.path.join(video_dir, video_filename)
        temp_video_path = os.path.join(output_dir, 'temp_' + video_filename)
        audio_path = os.path.join(output_dir, 'audio_' + video_filename + '.aac')
        output_path = os.path.join(output_dir, 'processed_' + video_filename)

        extract_audio(video_path, audio_path)
        add_background_and_subtitle(video_path, background_color_code, temp_video_path, title_text, subtitle_text, font_path)
        combine_video_audio(temp_video_path, audio_path, output_path)

        os.remove(temp_video_path)
        os.remove(audio_path)

def load_config(config_file):
    """Load the configuration from a JSON file."""
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description='Process videos.')
    parser.add_argument('-c', '--config_file', type=str, default='config.json', help='Path to the JSON configuration file')
    parser.add_argument('-v', '--video_directory', type=str, default='./test_input', help='Path to the video files') 
    args = parser.parse_args()
    config_file = args.config_file
    video_directory = args.video_directory
    # Load all configurations from the provided file
    configs = load_config(config_file)

    for config in configs:
        # Extract information from configuration
        video_name = config.get('video_name', './')
        background_color = config.get('background_color', '#e6526f')
        output_directory = config.get('output_directory', './')
        title = config.get('title', ['《Viva La Vida》', '(西班牙语：生命万岁)'])
        subtitle = config.get('subtitle', '')
        font_path = config.get('font_path','font.ttf')  # Replace with the path to your TTF font file

        # Print the extracted information (or use it as needed)
        print(f"视频目录: {video_directory}")
        print(f"视频名称: {video_name}")
        print(f"背景颜色: {background_color}")
        print(f"输出目录: {output_directory}")
        print(f"标题: {title}")
        print(f"字幕: {subtitle}")
   
        process_videos(video_directory, video_name, background_color, output_directory, title, subtitle, font_path)

