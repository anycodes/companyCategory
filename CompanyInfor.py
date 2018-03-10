'''
爬虫，根据天眼查，传入公司名获得公司主营

时间：2018-3-10
作者：刘宇

V:1.0
'''

# 导入urllib相关模块，主要在CompanyInfor中使用
import urllib.request
import urllib.parse

# 导入re和lxml相关模块，主要在CompanyInfor中使用，主要用于数据提取
from lxml import etree
import re

# 导入ssl模块，并且关闭，原因是天眼查属于https
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import random
import time
import json
import socket

class CompanyInfor:
    '''
    主要是根据公司名称获得公司的经营范围
    查询网址https://www.tianyancha.com/
    '''

    def __init__(self):
        '''
        初始化headers，防止反爬
        '''
        User_Agent = [
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5",
            "MQQBrowser/25 (Linux; U; 2.3.3; zh-cn; HTC Desire S Build/GRI40;480*800)",
            "Mozilla/5.0 (Linux; U; Android 2.3.3; zh-cn; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (SymbianOS/9.3; U; Series60/3.2 NokiaE75-1 /110.48.125 Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8J2",
            "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/534.51.22 (KHTML, like Gecko) Version/5.1.1 Safari/534.51.22",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A5313e Safari/7534.48.3",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A5313e Safari/7534.48.3",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A5313e Safari/7534.48.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; SAMSUNG; OMNIA7)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; XBLWP7; ZuneWP7)",
            "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
            "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
            "Mozilla/4.0 (compatible; MSIE 60; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; TheWorld)"
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
            "Cookie":"aliyungf_tc=AQAAAF7GzyVoJQsA0zsM3WAREnqQffEo; csrfToken=bOEPztlVEptvzwtW4NStJcOb; jsid=SEM-BAIDU-CG-SY-001953; TYCID=d7baade0241c11e8aacb754c1d0bcbfa; undefined=d7baade0241c11e8aacb754c1d0bcbfa; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1520677148,1520677996,1520678161,1520678482; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1520678540; ssuid=7667301804; RTYCID=13b7d2796d4e4e738508f6dd8214533a; token=0dd670656fff40aa9888517b58de4176; _utm=8ff6e09744b24c9099606be616749ba5; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMDk5MzY5MSIsImlhdCI6MTUyMDY3ODUzNywiZXhwIjoxNTM2MjMwNTM3fQ.o4zeTZ8CG8MzSnGZHxELUKq80CQsqd6QTlJ5drcR6pRFKENnXSO6I7J3tiLdcXe7NI-COdbQWdZrZStkIgralA%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213500993691%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMDk5MzY5MSIsImlhdCI6MTUyMDY3ODUzNywiZXhwIjoxNTM2MjMwNTM3fQ.o4zeTZ8CG8MzSnGZHxELUKq80CQsqd6QTlJ5drcR6pRFKENnXSO6I7J3tiLdcXe7NI-COdbQWdZrZStkIgralA",
        }

    def get_ip(self):
        '''
        切换代理IP
        使用了迅代理：xdaili.cn
        :return:
        '''
        for i in range(1, 100):
            try:

                urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))

                url_attr = urllib.request.Request("",)
                ip_temp = urllib.request.urlopen(url_attr)
                ip = ip_temp.read().decode("utf-8")
                ip_acount = json.loads(ip)["RESULT"][0]

                port = str(ip_acount["port"])
                ip_add = str(ip_acount["ip"])
                main_ip = ip_add + ":" + port
                temp_url = "http://ip.chinaz.com/getip.aspx"
                proxy_support = urllib.request.ProxyHandler({'http': main_ip})
                opener = urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)
                socket.setdefaulttimeout(5)
                res = urllib.request.urlopen(temp_url).read().decode('utf-8')
                break
            except Exception as e:
                time.sleep(6)
                continue

    def getCompanyUrl(self,companyName):
        '''
        根据公司名称获得地址，可能在搜索结果有若干类似的公司，本处只取第一个结果默认为匹配程度最高的结果
        :param companyName: 公司名称
        :return: 第一个公司对应的url
        '''
        url = "https://www.tianyancha.com/search?key="
        while True:
            try:
                page_source = urllib.request.urlopen(urllib.request.Request(url=url + urllib.parse.quote(companyName), headers=self.headers)).read().decode("utf-8","ignore")
                temp_data = etree.HTML(page_source)
                company_url = temp_data.xpath("//div[@class='search_result_single search-2017 pb25 pt25 pl30 pr30 ']/div[2]/div[1]/a/@href")[0]
                break
            except:
                self.get_ip()
        return company_url


    def getCompanyInfor(self,companyUrl):
        '''
        根据公司的url获得公司的主要经营信息
        :param companyUrl: 公司的url
        :return: 公司的主要经营内容，字符串
        '''
        while True:
            try:
                company_page_source = urllib.request.urlopen(urllib.request.Request(url=companyUrl, headers=self.headers)).read().decode("utf-8")
                return_data = etree.HTML(company_page_source).xpath('//table[@class="table companyInfo-table f14"]/tbody/tr')[-1]
                temp = return_data.xpath("td")[-1]
                temp_td = temp.xpath('string(.)')
                break
            except:
                self.get_ip()
        return re.sub('（(.*?)）', "", temp_td[0:10] + temp_td.split(temp_td[0:10])[1])