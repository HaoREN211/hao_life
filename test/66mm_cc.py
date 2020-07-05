# @Time    : 2020/7/4 23:47
# @Author  : REN Hao
# @FileName: 66mm_cc.py
# @Software: PyCharm

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re
import os
from app.tools import save_pic_from_url


# 判断当前共有多少张图片
def find_66mm_cc_page(inner_soup):
    page_pattern = re.compile("_([0-9]+)\.html")
    page_list = inner_soup.find(name="div", attrs={"class": "nav-links"})
    page_result = [x.get("href") for x in page_list.find_all(name="a")]

    inner_page = 0
    for i in page_result:
        current_page_result = page_pattern.findall(i)
        if current_page_result:
            inner_page = max(int(current_page_result[0]), inner_page)
    return inner_page


def get_all_page_link(inner_url, inner_page):
    inner_list_url = [inner_url]
    for inner_i in range(2, inner_page + 1):
        inner_list_url.append(inner_url[:-5] + "_" + str(inner_i) + ".html")
    return inner_list_url


def get_xiuren_pic(code):
    file_path = r"C:\Users\Hao\Documents\美图图库\66mm_cc"
    url = "http://www.66mm.cc/xiuren/*.html"
    url = url.replace("*", code)
    folder_name = url.replace("http://www.66mm.cc/", "").replace(".html", "").replace("/", "_")
    folder_path = os.path.join(file_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    soup = bs(urlopen(url), 'html.parser')
    page = find_66mm_cc_page(soup)

    list_url = get_all_page_link(url, page)

    for current_url in list_url:
        soup = bs(urlopen(current_url), 'html.parser')
        pic_content = soup.find(name="div", id="image_div")
        pic_content = pic_content.find_all(name="img")
        pic_content = [x.get("src") for x in pic_content]
        for current_pic in pic_content:
            file_name = current_pic.split("/")[-1]
            # file_type = file_name.split(".")[-1]
            # file_path = os.path.join(folder_path, str(number_pic)+"."+file_type)
            file_path = os.path.join(folder_path, file_name)
            save_pic_from_url(current_pic, file_path)


def get_url_pic(url):
    file_path = r"C:\Users\Hao\Documents\美图图库\66mm_cc"
    folder_name = url.replace("http://www.66mm.cc/", "").replace(".html", "").replace("/", "_")
    folder_path = os.path.join(file_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    soup = bs(urlopen(url), 'html.parser')
    page = find_66mm_cc_page(soup)

    list_url = get_all_page_link(url, page)

    for current_url in list_url:
        soup = bs(urlopen(current_url), 'html.parser')
        pic_content = soup.find(name="div", id="image_div")
        pic_content = pic_content.find_all(name="img")
        pic_content = [x.get("src") for x in pic_content]
        for current_pic in pic_content:
            file_name = current_pic.split("/")[-1]
            # file_type = file_name.split(".")[-1]
            # file_path = os.path.join(folder_path, str(number_pic)+"."+file_type)
            file_path = os.path.join(folder_path, file_name)
            save_pic_from_url(current_pic, file_path)


if __name__ == '__main__':
    get_xiuren_pic("178")
    get_url_pic("http://www.66mm.cc/taotu/20.html")
    get_url_pic("http://www.66mm.cc/youmi/184.html")

    taotu = "http://www.66mm.cc/youmi/*.html"

    for i in range(213, 500):
        current_taotu = taotu.replace("*", str(i))
        try:
            urlopen(current_taotu)
        except:
            print(current_taotu)
        else:
            get_url_pic(current_taotu)
