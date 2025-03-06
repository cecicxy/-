from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
if __name__=="__main__":
    #UA伪装
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    # 必要时设置请求频率限制
    #循环发送请求，获取所有url的article内容
    df=pd.read_csv('bazhuayu/data/crawler/url_title.csv',index_col=0)
    df['content']='' #增加一列content
    # list=[]
    def match_font_size(tag): #经过观察，文章内容的字体大小为15px或16px
        if tag.name != 'span':
            return False
        if tag.has_attr('style'):
            return 'font-size: 15px;' in tag['style'] or 'font-size: 16px;' in tag['style']
        return False
    
    for i in tqdm(range(len(df))):
        url=df['url'][i]
        page = requests.get(url, headers=headers).text
        soup = BeautifulSoup(page, 'html.parser')
        all = soup.findAll(match_font_size)
        string=''
        for j in all:
            if j.find('img'):
                continue
            if j.string==None:
                continue
            else:
                string=string+j.string
        # list.append(string)
        df.iloc[i,2]=string
    # list=pd.DataFrame(list)
    # list.to_csv('bazhuayu/data/crawler/string_list.csv')
    df.to_csv('bazhuayu/data/crawler/url_title_content.csv')


    ##test单个url

# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
# url='http://mp.weixin.qq.com/s?__biz=Mzk0MDAwMDkzMA==&mid=2247484011&idx=2&sn=63ebf4d2d79e86d45c63f05c980fe7f8&chksm=c2e911a6f59e98b07d98fc3f4a08b425a9d4628cb84e2d55f35b2a3917ecb92d0b3579a5c29b#r'
# page = requests.get(url, headers=headers).text
# with open('bazhuayu/data/crawler/test.html','w',encoding='utf-8') as f:
#     f.write(page)

# soup = BeautifulSoup(page, 'html.parser')
# # all = soup.findAll('span', style="font-size: 15px;")


# def match_font_size(tag):
#     if tag.name != 'span':
#         return False
#     if tag.has_attr('style'):
#         return 'font-size: 15px;' in tag['style'] or 'font-size: 16px;' in tag['style']
#     return False

# all = soup.findAll(match_font_size)
# string=''
# for j in all:
#     if j.find('img'):
#         continue
#     if j.string==None:
#         continue
#     string=string+j.string
# string=pd.DataFrame([string])
# string.to_csv('bazhuayu/data/crawler/string.csv')