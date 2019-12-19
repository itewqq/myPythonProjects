import requests
import json
from urllib.parse import quote, unquote, urlencode

def getM3u8(Id,jie):
    url='http://newes.learning.xidian.edu.cn/live/getViewUrl'
    headers={
        'Accept': '*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'Cookie':$YOUR COOKIE$,
        'Host':'newes.learning.xidian.edu.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    params={
            'liveId':str(Id),
            'status':'2',
            'jie':str(jie),
            'isStudent':0
    }

    res=requests.get(url,headers=headers,params=params)
    infos=str(unquote(res.text,encoding='utf-8', errors='replace'))
    data=json.loads(infos[62:])
    if('mobile' in data['videoPath']):
        return data['videoPath']['mobile']
    else:
        return "NO mobile videoPath"

#print(getM3u8(10215903,2))

def getClassData():
    url='http://newes.learning.xidian.edu.cn/live/listSignleCourse'
    headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '38',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': $YOUR COOKIE$,
        'Host': 'newes.learning.xidian.edu.cn',
        'Origin': 'http://newes.learning.xidian.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data={
        'liveId': '10215903',
        'fid': '16820',
        'uId': '77194241'
    }
    res=requests.post(url,headers=headers,data=data)
    return json.loads(res.text)

if __name__=="__main__":
    with open('VideoUrls.txt','w') as f:
        data=getClassData()
        for cs in data:
            infos=str(cs['startTime']['month']+1)+' '+str(cs['startTime']['date'])+' '+str(cs['jie'])
            url=getM3u8(cs['id'],cs['jie'])
            print(infos)
            f.write(infos+'\n')
            f.write(url+'\n')
        
