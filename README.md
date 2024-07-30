# 使用方法

提供[config.json](config.json)文件
```
python process_video.py -c config.json -v ./test_input
```
# config文件生成 - [gen_conf](./gen_conf)
使用modelhub大模型服务生成视频标题，简介，适合的背景颜色

提供视频名称列表（目前hardcode）
提供示例prompt文件
```
    prompt_subtitle = "prompt.txt"
    prompt_color = "prompt_color.txt"
    prompt_title = "prompt_title.txt"
```

```
python gen_conf.py
```
