from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib
import requests
from subprocess import call


class crawler(object):
    def getsource(self, url):
        html = requests.get(url)
        return html.text

    def getMusic(self, html):
        soup = BeautifulSoup(html, "html.parser")
        projectLine = soup.find_all("span", {"class": "projectLine"})
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        header = 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        length = len(projectLine)
        for i in range(5, 10):
            each = projectLine[i]
            text = each.a.text
            print i
            if 'ZIP' in text:
                index = text.index('M')
                num = int(text[0:index])
                if num < 100:
                    url = each.a.get("href")
                    print text + "  " + url
                    call(["wget --header ", header, url])
                    # response = requests.get(url,headers=headers)
                    # with open("zip/" + str(i) + ".zip", "wb") as handle:
                    #     for data in response.iter_content():
                    #         handle.write(data)


if __name__ == '__main__':
    url = 'http://www.cambridge-mt.com/ms-mtk.htm'
    music = crawler()
    html = music.getsource(url)
    music.getMusic(html)
