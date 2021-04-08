#coding=utf-8
'''
    FileName      ：sohuCrawler.py
    Author        ：@zch0423
    Date          ：Apr 6, 2021
    Description   ：
    爬取sohu财经新闻
    目标链接 https://www.sohu.com/c/8/1463
'''
import csv
import json
import time
import requests
from requests.api import head

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Host": "v2.sohu.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip",
    "Connection": "keep-alive",
}


def getNews(page: int = 1, size: int=20):
    '''
    Description:
    请求链接，获取json文件
    ---
    Params:
    page, int default 1, 页码
    size, int default 20, 一次返回新闻数
    ---
    Returns:
    data, list, 每个元素包含了新闻的字典信息
    '''
    _ = int(time.time())
    url = f"https://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1463&page={page}&size={size}&_={_}"
    r = requests.get(url, headers=HEADERS)
    return json.loads(r.text)


def data2csv(data: list, filename: "str | None"=None):
    '''
    Description:
    将字段导出到csv文件
    ---
    Params:
    data, json解析列表
    filename, 导出路径, 如不指定则用时间戳导出
    ---
    Returns:
    '''
    if filename is None:
        filename = time.strftime("%Y%m%d-%H%Msohu.csv", time.localtime())
    keys = ["id", "title", "publicTime",
            "authorName", "mobileTitle", "originalSource"]
    output = []
    for each in data:
        output.append([each[k] for k in keys])
    with open(filename, "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(keys)
        csv_writer.writerows(output)


if __name__ == "__main__":
    data2csv(getNews(page=1, size=50))
