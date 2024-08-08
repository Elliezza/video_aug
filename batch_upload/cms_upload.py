from upload import upload_with_retry, upload_entry_with_retry
from file_size import get_file_size, get_video_duration
from category import get_category
from publisher import get_publish_id
from download import download_file_with_retry

def process_entry(config):
   
    video_download_url = config['url']
    cover_download_url = config['coverUrl']

    try:
        file_path = download_file_with_retry(video_download_url, './temp')
        cover_path = download_file_with_retry(cover_download_url, './temp')
        print(f"Files downloaded to: {file_path}, {cover_path}")
    except Exception as e:
        print(f"Failed to download file: {e}")
        return "Download Fail"

    video_url = upload_with_retry(file_path, "video")
    img_url = upload_with_retry(cover_path, "img")

    if video_url == None or img_url == None:
        print(file_path)
        print("Fail to upload, skipping.....")
        continue

    ori_cat = config['categoryLevel3New']
    cate1, cate2 = get_category(ori_cat)

    file_size = get_file_size(file_path)
    video_duration = config['duration'] #get_video_duration(file_path)

    publishID, publishName = get_publish_id(ori_cat)

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
        res = upload_entry_with_retry(video_entry)

        return res
