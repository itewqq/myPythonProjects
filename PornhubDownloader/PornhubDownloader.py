import requests
import execjs
import os
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import sys

requests.packages.urllib3.disable_warnings()

# url0='https://www.pornhub.com/view_video.php?viewkey=ph5c33b5039e33c'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': 'www.pornhub.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

class Url_mp4():
    def __init__(self,url,filename="defualt.mp4"):
        self.url=url
        download_path = os.getcwd() +r"\download/"
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        self.filename=download_path+filename

    def Schedule(self, a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 1
        print("  " + "%.2f%% File Has been retrieved :%ld TotalFileSize:%ld" % (per, a * b, c) + '\r')

    def download(self):
            try:
                print("\"" + self.filename+ "\"" + "Download Started...")
                urlretrieve(self.url, self.filename, reporthook=self.Schedule)
                print("\"" + self.filename + "\"" + "Downloaded Finished!")
            except Exception as e:
                print(e)


def main():
    url0=sys.argv[1]
    html = requests.get(url=url0, headers=headers, verify=False)
    soup = BeautifulSoup(html.text)
    scripts = soup.findAll("script", type='text/javascript')
    urls = {}
    bestUrl = ""

    for script in scripts:
        if (str(script).find("loadScriptUniqueId.push") != -1):
            jscodestr = str(script)
            jscode = jscodestr[len('<script type="text/javascript">'):jscodestr.find("loadScriptUniqueId")]
            ctx = execjs.compile(jscode)
            dataDictName = 'flashvars_' + "".join(
                [jscodestr[jscodestr.find("var flashvars_") + len("var flashvars_") + x] for x in
                 range(len("194884621"))])
            data = ctx.eval(dataDictName)
            for vid in data['mediaDefinitions']:
                if vid['format'] == 'mp4':
                    urls[int(vid['quality'])] = vid['videoUrl']
            bestUrl = urls[max(urls.keys())]
            break

    downloader = Url_mp4(url=bestUrl)
    downloader.download()

if __name__ == "__main__":
    main()
