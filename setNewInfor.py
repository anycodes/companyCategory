'''
主要用于建立train，通过11467.com的分类，获得主要经营内容，根据经营内容来存入到不同的文件夹下，作为train集合

时间：2018-3-10
作者：刘宇

V:1.0
'''

import urllib.request
from lxml import etree
import re
import time
import json
import socket


def get_ip():
    '''
    切换代理IP
    使用了迅代理：xdaili.cn
    :return:
    '''
    for i in range(1, 100):
        try:

            urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))

            url_attr = urllib.request.Request(
                "",
                headers=headers)
            ip_temp = urllib.request.urlopen(url_attr)
            ip = ip_temp.read().decode("utf-8")
            print(ip)
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
            print('This ip is ok : ', res)
            break
        except Exception as e:
            time.sleep(6)
            continue


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Cookie": "Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1520662786,1520662921; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1520663684; ASPSESSIONIDSSABBARR=GNNICHJBFBCNCDDKKDHKAAJJ",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

re_dict = {
    "C000001":"549",
    "C000002":"563",
    "C000003":"645",
    "C000004":"578",
    "C000005":"1",
    "C000006":"36",
    "C000007":"62",
    "C000008":"779",
    "C000009":"813",
    "C000010":"836",
    "C000011":"860",
    "C000012":"748",
    "C000013":"625",
    "C000014":"757",
    "C000015":"774",
    "C000017":"893",
    "C000018":"877",
    "C000020":"914",
}

get_ip()
total_count = 0
for key,value in re_dict.items():
    total = 1
    for page_num in range(1, 6):
        url = "http://b2b.11467.com/search/" + str(value) + "-" + str(page_num) + ".htm"
        list_page_source = urllib.request.urlopen(urllib.request.Request(url=url, headers=headers)).read().decode("utf-8")
        list_temp_data = re.findall('<li><div class="f_r cologo">(.*?)</li>',list_page_source)
        for eve in list_temp_data:
            try:
                company_url = "http:" + re.findall('<h4><a href="(.*?)"',eve)[0]
                content_data = etree.HTML(urllib.request.urlopen(urllib.request.Request(url=company_url, headers=headers)).read().decode("utf-8")).xpath("//table[@class='codl']/tr")
                total_count = total_count + 1
                if total_count % 20 == 0:
                    get_ip()
                    total_count = 0
                for eve_tr in content_data:
                    temp = eve_tr.xpath("td[1]")[0]
                    if "经营范围" in temp.xpath("string(.)"):
                        temp_tr = eve_tr.xpath("td[2]")[0]
                        content = re.sub('（(.*?)）', "", temp_tr.xpath("string(.)"))
                        content = re.sub('【(.*?)】', "", content)
                        content = re.sub('\((.*?)\)', "", content)
                        with open("Sample/" + str(key) + "/" + str(total) + ".txt","w") as f:
                            f.write(content.strip())
                        print("total data:",key,page_num,total)
                        total = total + 1
                        break
            except:
                total_count = 0
                get_ip()
