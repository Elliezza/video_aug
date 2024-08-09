from upload import upload_with_retry, upload_entry_with_retry
from file_size import get_file_size, get_video_duration
from category import get_category
from publisher import get_publish_id
from download_2 import download_file_with_retry, remove_file
import time

def clean_up(path1, path2):
    remove_file(path1)
    remove_file(path2)

def process_entry(config):
    ori_name = config['publisherName']
    publishID, publishName = get_publish_id(ori_name)
    print(ori_name)
    print(config['updateAt'])
    print(publishID, publishName) 

    return "success"

def process_entry_2(config):
   
    video_download_url = config['url']
    cover_download_url = config['coverUrl']

    try:
        file_path = download_file_with_retry(video_download_url, './temp')
        cover_path = download_file_with_retry(cover_download_url, './temp')
        print(f"Files downloaded to: {file_path}, {cover_path}")
    except Exception as e:
        print(f"Failed to download file: {e}")
        return "Download Fail"

    video_url = file_path #upload_with_retry(file_path, "video")
    img_url = cover_path #upload_with_retry(cover_path, "img")
     

    if video_url == None or img_url == None:
        print(file_path)
        print("Fail to upload, skipping.....")
        return "Upload Fail"

    ori_cat = config['categoryLevel3New']
    cate1, cate2 = get_category(ori_cat)

    file_size = get_file_size(file_path)
    video_duration = config['duration'] #get_video_duration(file_path)

    ori_name = config['publisherName']
    publishID, publishName = get_publish_id(ori_name)
    
    video_entry = {
             "itemType":"视频",
             "url": video_url,
             "country":"中国",
             "language":"中文",
             "title": config['title'],
             "content": config['content'],
             "duration": video_duration,
             "format":"mp4",
             "size":file_size,
             "categoryLevel1": cate1,
             "categoryLevel2": cate2,
             "coverUrl":img_url,
             "publishId": publishID,
             "publishName": publishName, 
             "publishTime":int(time.time()*1000),
             "itemTime":int(time.time()*1000),
             "itemStatus":1,
             "province":"",
             "city":"",
             "source":" 渠道-1",
    }

    print(video_entry)
    #res = upload_entry_with_retry(video_entry)
    res = "test"

    clean_up(file_path, cover_path)
    return res
