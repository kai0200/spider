# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup

urls = [
    #f'https://code.sohuno.com/groups/mail-inactive?page={page}'
    #f'https://code.sohuno.com/groups/passport?page={page}'
    #f'https://code.sohuno.com/groups/VipMail?page={page}'
    #f'https://code.sohuno.com/groups/freemail?page={page}'
    f'https://code.sohuno.com/groups/mail?page={page}'
    for page in range(1, 8 + 1)
]


def get_text(url):
    # 创建一个 Session 对象来维护会话状态
    session = requests.Session()

    # 从 Chrome 浏览器中获取的 cookies（这里需要手动复制并填充）
    cookies_dict = {
        'OUTFOX_SEARCH_USER_ID_NCOO': '1815196188.3313549',
        '_gitlab_session': '759e135cb35afe71f44d0c429ea9038e',
        't': '1730282060537'
        # ... 添加更多 cookies
    }

    # 将 cookies 添加到 Session 对象中
    for cookie_name, cookie_value in cookies_dict.items():
        session.cookies.set(cookie_name, cookie_value)

    try:
        response = session.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        # 捕获所有requests库抛出的异常
        #print(f"请求失败: {e}")
        return  # 退出函数


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="project")
    return [link["href"] for link in links]


def parse_li(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("li", class_="last")
    return [link["href"] for link in links]



if __name__ == '__main__':
    for result in parse(get_text(urls[2])):
        print(result)

# vim: expandtab softtabstop=4 shiftwidth=4
