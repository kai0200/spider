# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# 创建会话对象
session = requests.Session()

# 假设你已经有一个登录表单的 URL
login_url = 'https://example.com/login'
# 以及登录所需的表单数据
login_data = {
    'username': 'your_username',
    'password': 'your_password'
}

# 发送登录请求
login_response = session.post(login_url, data=login_data)

# 检查登录是否成功（这里假设登录成功会重定向到主页）
if login_response.status_code == 200 or login_response.status_code == 302:
    # 尝试访问一个需要登录才能访问的页面
    protected_url = 'https://example.com/protected'
    response = session.get(protected_url)

    # 检查响应状态码和内容
    if response.status_code == 200:
        # 进一步解析响应内容，检查是否包含登录状态的线索
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假设登录成功后页面会有特定的元素或文本
        if 'Welcome, your_username!' in response.text:
            print("登录成功")
        else:
            # 检查是否有重定向到登录页面的迹象（例如状态码302或响应中的特定内容）
            if 'Login' in soup.title.string or 'login' in response.url.lower():
                print("登录失败，重定向到登录页面")
            else:
                print("登录状态不确定，需要进一步分析")
    else:
        print(f"访问受保护页面失败，状态码：{response.status_code}")
else:
    print("登录请求失败，状态码：", login_response.status_code)

# vim: expandtab softtabstop=4 shiftwidth=4
