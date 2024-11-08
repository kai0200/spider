# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from typing import Dict
import trace
import time

# 缺省值
url = "https://code.sohuno.com/?page=5"

cookies_dict = {
    'OUTFOX_SEARCH_USER_ID_NCOO': '1815196188.3313549',
    '_gitlab_session': '759e135cb35afe71f44d0c429ea9038e',
    't': '1730282060537'
}

headers = {
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://sso.sohu-inc.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

def get_html(url: str, cookies_dict: Dict[str, str]):
    """
    使用setcookie方式, 需要cookie的值。
    解析url地址，返回html的内容
    return: html
    """
    session = requests.Session()
    # 将 cookies 添加到 Session 对象中
    for cookie_name, cookie_value in cookies_dict.items():
        session.cookies.set(cookie_name, cookie_value)

    try:
        response = session.get(url, headers=headers)
        return response.text
    except requests.exceptions.RequestException as e:
        # 捕获所有requests库抛出的异常
        print(f"请求失败: {e}")
        return  # 遇到return直接退出函数


def parse_html_lastpage(html: str):
    """
    获取code网页总共的页数
    return num: int
    """
    soup = BeautifulSoup(html, "html.parser")
    tag_set = soup.find_all('li', class_="last") # find_all后返回的是个一个集合
    for li_tag in tag_set: # 所以需要一个for循环进行处理
        a_tag = li_tag.find('a') # 实际上只有一个值标示最后page数量
    href = a_tag['href']
    page = href.split('=')[1]
    return int(page)


def parse_html_project(html: str):
    """
    获取网页上全部的项目名称
    return: []
    """
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all('a', class_="project")
    return [tag['href'] for tag in tags]


def make_urls(num: int):
    urls = [
        f"https://code.sohuno.com/?page={page}"
        for page in range(1, num + 1)
    ]
    return urls


if __name__ == '__main__':
    url = "https://code.sohuno.com/?page=2"

    # 这里每次使用需要更新
    cookies_dict = {
        'OUTFOX_SEARCH_USER_ID_NCOO': '1815196188.3313549',
        '_gitlab_session': '759e135cb35afe71f44d0c429ea9038e',
        't': '1730282060537'
    }



    # 生成列表页，通过网页读取合计多少页
    html = get_html(url, cookies_dict)
    page_num = parse_html_lastpage(html)
    urls = make_urls(page_num)
    # #测试取得登录后网页内容
    #page_num = parse_html_lastpage(html)
    #print(f"合计总页数：{page_num}")

    # 单线程方式运行
    start = time.time()
    for url in urls:
        # 这个过程会耗时
        projects = parse_html_project(get_html(url, cookies_dict))
        for p in projects:
            print(p)
    end = time.time()
    print(f"Time: {end - start}")

    # 创建 Trace 对象，跟踪每一行代码
    #tracer = trace.Trace(trace=True, count=False)
    #tracer.run('get_html(str(url[1]), cookies_dict)')

    # 获取html里project内容
    #project_list = parse_html_project(html)
    #print(project_list[3])
    #print(len(project_list))
# vim: expandtab softtabstop=4 shiftwidth=4
