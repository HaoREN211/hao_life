# @Time    : 2020/7/4 21:57
# @Author  : REN Hao
# @FileName: scrapy.py
# @Software: PyCharm

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
import re
import os

PIC_PATH = R"C:\Users\Hao\Documents\美图图库\24meitu"


# 根据网站要求添加header，不然网站会报404错误
def get_header(inner_url):
    return {
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
        "Referer": inner_url,
        "Connection": "keep-alive",
        "Host": "ba.xinxiangtan.com:90"}


# 判断当前共有多少张图片
def get_total_page(inner_soup):
    inner_total_page = 0
    pattern = re.compile("共([0-9]+)页")
    for i in inner_soup.findAll(name="a"):
        match_result = pattern.findall(str(i))
        if match_result:
            return int(match_result[0])
    return inner_total_page


# 根据网页链接获取当前文件名
def get_folder_name_by_url(inner_url):
    return str(inner_url.split("/")[-1]).split("-")[0]


# 根据文档名获取文档的路径
def get_folder_path(inner_folder_name):
    inner_current_path = os.path.join(PIC_PATH, inner_folder_name)
    if not os.path.exists(inner_current_path):
        os.makedirs(inner_current_path)
    return inner_current_path


def get_all_img(code):
    url = "http://www.24meitu.com.cn/article/"+code+"-1.html"
    url_name = get_folder_name_by_url(url)
    current_path = get_folder_path(url_name)
    url_temple = url.replace("-1", "-*")

    total_page = get_total_page(bs(urlopen(url), 'html.parser'))

    for i in range(total_page):
        current_i = i + 1
        current_url = url_temple.replace("*", str(current_i))
        print(current_url)

        current_data = urlopen(current_url)
        current_soup = bs(current_data, 'html.parser')

        target_div = current_soup.find(name="div", id="content")
        target_img = target_div.find(name="img").get("src")
        target_img_type = target_img.split(".")[-1]
        print("--- " + target_img)

        reg = Request(target_img, headers=get_header(current_url))
        img_content = urlopen(reg).read()

        file_path = os.path.join(current_path, str(current_i) + "." + target_img_type)
        print("--- " + file_path)
        f = open(file_path, 'wb+')
        f.write(img_content)
        f.close()


if __name__ == '__main__':
    get_all_img("1230d95")
