#coding=utf-8
'''
    FileName      ：szseCrawler.py
    Author        ：@zch0423
    Date          ：Apr 8, 2021
    Description   ：
    深交所上市公司公告爬虫
    http://www.szse.cn/disclosure/notice/company/index.html
    爬取标题，链接和时间导出csv
'''
import re
import csv
import requests
from bs4 import BeautifulSoup
from requests.api import head

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Host": "www.szse.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip",
    "Connection": "keep-alive",
}


def getAnn(url="http://www.szse.cn/disclosure/notice/company/index.html"):
    '''
    Description:
    get announcement
    ---
    Params:
    url, str, default 第一页
    ---
    Returns:
    response.text
    '''
    r = requests.get(url, headers=HEADERS)
    r.encoding = "utf-8"
    return r.text


def data2csv(text, outfile="szse.csv"):
    '''
    Description:
    解析请求文本，导出到csv文件
    ---
    Params:
    text, response.text
    outfile, str, 导出文件名
    ---
    Returns:
    '''
    f = open(outfile, "a")
    csv_writer = csv.writer(f)
    csv_writer.writerow(["title", "time", "url"])
    soup = BeautifulSoup(text, "lxml")
    pattern = r"curHref = '(.*?)';\s*//var curTitle = '(.*?)';"
    for each in soup.find_all("div", class_="title"):
        s = re.search(pattern, each.script.string)
        title = s.group(2)
        url = "http://www.szse.cn/disclosure/notice/company/"+s.group(1)[1:]
        time = each.span.string.strip()
        csv_writer.writerow([title, time, url])
    f.close()


if __name__ == "__main__":
    data2csv(getAnn(), outfile="szse.csv")
