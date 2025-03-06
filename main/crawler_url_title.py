from bs4 import BeautifulSoup
import requests
import json
import csv
import pandas as pd
import time
if __name__=="__main__":
    #UA伪装
   

    #指定url,主体url
    url= "https://mp.weixin.qq.com/mp/appmsgalbum"
    # url="https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=Mzk0MDAwMDkzMA==&album_id=1833917547901943816&count=10&begin_msgid=2247532556&begin_itemidx=1&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=&__biz=Mzk0MDAwMDkzMA%3D%3D&appmsg_token=&x5=0&f=json"
    #处理url携带的参数
params = {
    'action': 'getalbum',  #album是合集
    '__biz': 'Mzk0MDAwMDkzMA==',
    'album_id': "1833917547901943816",
    'count': 10,
    # 'is_reverse': 1, # 为倒叙也就是从第一篇文章开始
    'begin_msgid':2247532556,
    'begin_itemidx':1,
    'uin': '',
    'key': '',
    'pass_ticket': '',
    'wxtoken': '',
    'devicetype': '',
    'clientversion': '',
    '__biz': 'Mzk0MDAwMDkzMA%3D%3D',
    'appmsg_token': '',
    'x5': 0,
    'f': 'json'}

# 设置请求频率限制
MAX_REQUESTS_PER_MINUTE = 10
REQUEST_INTERVAL = 60 / MAX_REQUESTS_PER_MINUTE

# 设置请求头
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}


# 循环发送请求，获取所有相册内容

def get_album(url, params, headers, last_msgid, result,idx=1):
    params['begin_msgid'] = last_msgid
    print(params['begin_msgid'])
    params['begin_itemidx'] = idx
    # print(url)
    # time.sleep(REQUEST_INTERVAL)
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'article_list' not in data['getalbum_resp'].keys(): #如果爬取的里面没有article_list，就用下一个idx，因为同一个msgid可能有多个idx，但据观察，idx最多为3
            if int(idx) > 3:
                return result
            idx = str(int(idx)+1) #idx不管是str还是int都可以+1
        else:
            album = data['getalbum_resp']['article_list']
            if len(album) == 0: #如果相册为空，就说明已经爬取完毕
                return result
            for i in album:
                # 获取url和title
                url2 = i['url']
                title = i['title']
                result.append({'url': url2, 'title': title})

                # 控制请求频率
            last_msgid = album[-1]['msgid']  # 获取最后一张图片的消息ID，用于下一次请求
            idx = album[-1]['itemidx']
    return result+get_album(url, params, headers, last_msgid, [],idx)

result = get_album(url, params, headers, 2247532556, [],1)
# 保存到csv文件中
df=pd.DataFrame(result)
df.to_csv('data/crawler/url_title.csv')
# with open('url_title_new.csv', 'a', newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f, fieldnames=['url', 'title'])
#     writer.writerow({'url': url2, 'title': title})


