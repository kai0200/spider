# -*- coding: utf-8 -*-
import requests
import sys
import time
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import code_spider



def get_html(url):
    response = requests.get(url)
    return response


if __name__ == '__main__':
    url = "https://www.cnblogs.com/#p2"

    start = time.time()
    html = get_html(url)
    end = time.time()

    print(end - start)

# vim: expandtab softtabstop=4 shiftwidth=4
