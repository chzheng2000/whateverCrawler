#coding=utf-8
'''
    FileName      ：sinaCrawler.py
    Author        ：@zch0423
    Date          ：Apr 6, 2021
    Description   ：
    爬取新浪滚动新闻
    访问链接为https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1
'''
import csv
import time
import json
import random
import requests

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Host": "feed.mix.sina.com.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip",
    "Connection": "keep-alive",
}


def getNews(page:int =1, lid:int = 2509):
    '''
    Description:
    请求链接获取json
    ---
    Params:
    page, int default 1, 页数
    lid, int default 2509, 类别
    2509，全部/ 2510，国内/ 2511，国际/ 2669，社会/ 
    2512，体育/ 2513，娱乐/ 2514，军事/ 2515，科技/ 
    2516，财经/ 2517，股市/ 2518，美股/
    ---
    Returns:
    data, dict, 包含50条新闻的json信息
    '''
    if lid!=2669 and (lid<2509 or lid>2518):
        lid = 2509  # 默认选取全部
    r = random.random()
    _ = int(time.time())
    url = f"https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={lid}&num=50&page={page}&r={r:.16f}&_={_}"
    r = requests.get(url, headers=HEADERS)
    return json.loads(r.text)["result"]["data"]


def data2csv(data, filename: "str | None" =None):
    ''' 
    Description:
    将json文件导出到csv
    ---
    Params:
    data, dict, json数据
    filename, str default None, 指定导出文件名，若没有则以当前时间作为导出文件名
    ---
    Returns:
    '''
    if filename is None:
        filename = time.strftime("%Y%m%d_%H%Msina.csv", time.localtime())
    # 导出字段
    keys = ["oid", "hqChart", "title", "ctime", "lids", "url", "intro", "wapurl"]
    output = []
    for row in data:
        temp = [row[k] for k in keys]
        # 股票代码信息
        s = json.loads(temp[1])
        temp[1] = s["stockMarket"]+"-"+s["stockCode"]
        output.append(temp)
    with open(filename, "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(keys)
        csv_writer.writerows(output)


if __name__ == "__main__":
    # data2csv(getNews(lid=2516))  # 财经新闻
    data2csv(getNews(lid=2517))  # 股市新闻
