import os
import requests
import json
import time

def upload_material(path, d_type):
    with open(path, 'rb') as f:
        response = requests.post(
            "http://172.24.4.20:10008/cms/api/file/upload",
            files={"file": f},
            data={"type": d_type}
        )

    response.raise_for_status()

    res = response.json()

    url = res["oss_url"]

    return url

def upload_with_retry(path, d_type, retries=2, delay=5):
    attempt = 0
    while attempt <= retries:
        try:
            url = upload_material(path, d_type)
            return url
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt > retries:
                print("Max retries exceeded.")
                return None
            time.sleep(delay)  # 等待后重试

def upload_entry(data): 
    response = requests.post(
            'http://172.24.4.20:10008/cms/api/material/upsert', 
            headers={'Content-Type': 'application/json'}, 
            data=json.dumps(data)
    )

    response.raise_for_status()

    res = response.json()
    return res


def upload_entry_with_retry(data, retries=2, delay=5):
    attempt = 0
    while attempt <= retries:
        try:
            res = upload_entry(data)
            return res
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt > retries:
                print("Max retries exceeded.")
                return None
            time.sleep(delay)  # 等待后重试


if __name__ == "__main__":
    #res = upload_material("Elisabeth_Beyer-《百万小丑》女变奏_Variation_from_Harle.mp4", 'img')
    #print(res)

    data = {'itemType': '视频', 'url': 'https://cn-material-bucket.oss-cn-shenzhen.aliyuncs.com/res/video/11_ee2e5eb080c8f2fd.mp4', 'country': '中国', 'language': '中文', 'title': 'Elisabeth Beyer-“百万小丑”女变奏 Variation from Harle', 'content': '"在这段精采的芭蕾舞蹈视频中，Elisabeth Beyer以其卓越的技巧 和深情的演绎，为观众呈现了名作“百万小丑”中的女变奏舞蹈。透过她的舞姿，感受每一个音符和动作背后的故 事，尽览芭蕾的优雅和力量。"', 'duration': 123, 'format': 'mp4', 'size': 28609, 'categoryLevel1': '3', 'categoryLevel2': '3', 'coverUrl': 'https://cn-material-bucket.oss-cn-shenzhen.aliyuncs.com/res/img/66_ee2e5eb080c8f2fd.jpg', 'publishId': '2000000020', 'publishName': '小马哥与他的朋友们', 'publishTime': 1722577628909, 'itemTime': 1722577628909, 'itemStatus': 1, 'province': '北京', 'city': ' 北京', 'source': '自产'}

    res = upload_entry_with_retry(data, retries=1, delay=1)
    print(res)

    print("something else")

