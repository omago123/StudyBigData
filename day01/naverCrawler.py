import os
import sys
import urllib.request
import urllib.parse
import datetime
import time
import json

client_id ='GWWUHPgV0uguJWvgsMFu'
client_secret = 'slKycSCDf4'


# url 접속 요청 후 응답리턴함수


def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header('X-Naver-Client-Secret', client_secret)

    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200:
            print(f"[{datetime.datetime.now()} ] Url Request Success")
            return res.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")


def getNaverSearch(node, srcText, start, display):
    base = 'https://openapi.naver.com/v1/search'
    node = f'/{node}.json'
    text = urllib.parse.quote(srcText) # url주세어 맞춰서 파싱
    parmeters=f'?query={text}&start={start}&diplay={display}' 

    url = base + node + parmeters
    resDecode  = getRequestUrl(url)

    if resDecode == None:
        return None
    else:
        return json.loads(resDecode)

def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate= pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt':cnt, 'title':title, 'description':description,
                        'org_link':org_link, 'link':link, 'pDate':pDate})

# 실행최초함수
def main():
    node = 'news'
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult= []
    jsonRes = getNaverSearch(node, srcText, 1, 50)

    total = jsonRes['total']

    while ((jsonRes != None) and (jsonRes['display'] != 0)):
        for post in jsonRes['items']:
            cnt +=1
            getPostData(post, jsonResult,cnt)
        
        start = jsonRes['start'] + jsonRes['display']
        jsonRes = getNaverSearch(node, srcText,start, 100)

    print(f'전체 검색 : {total} 건')

    # file output
    with open(f'./{srcText}_naver_{node}.json',mode='w',encoding='utf-8') as outfile:
        jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii=False)
        outfile.write(jsonFile)
    
    print(f'가져온 데이터 : {cnt} 건')
    print(f'{srcText}_naver_{node}.json SAVED')
    

if __name__ == '__main__':
    main()


