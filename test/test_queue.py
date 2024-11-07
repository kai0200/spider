#!/usr/local/bin/python3
# test_code_spider.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import code_spider
import queue
import threading

# 从url_queue 读取解析出html后写入html_queue
def urlq_to_htmlq(url_queue, html_queue):
    while True:
        url = url_queue.get()
        print(f"处理数据: {url}")
        html = code_spider.get_text(url)
        html_queue.put(html)
        print(f"增加到html_queue size: ", len(html))
        #print("url_queue.size= ", url_queue.qsize(), "html_queue.size= ", html_queue.qsize())
        print(threading.current_thread().name, f"code1111 {url}",
                        "url_queue=size:", url_queue.qsize(), html_queue.qsize())
        url_queue.task_done()  # 标记任务完成


def do_parse(html_queue, fout):
    while not html_queue.empty():
    #while True:
        html = html_queue.get()
        results = code_spider.parse(html)
        for result in results:
            with open("02.data.txt", 'a') as fout:
                fout.write(str(result) + "\n")
        print(threading.current_thread().name, f"Parse-2222 {url}",
                        "html_queue=size:", html_queue.qsize())
        html_queue.task_done()  # 标记任务完成


if __name__ == '__main__':

    url_queue = queue.Queue()
    html_queue = queue.Queue()
    urls = code_spider.urls
    for url in urls:
        url_queue.put(url)

    for idx in range(4):
        t = threading.Thread(target=urlq_to_htmlq, args=(url_queue, html_queue),
                             name=f"idx-{idx}")
        t.start()

    sleep(5)
    #  url1 = 'https://code.sohuno.com/groups/mail-inactive?page=1'
    #  url2 = 'https://code.sohuno.com/groups/mail-inactive?page=2'
#
    #  html1 = code_spider.get_text(url1)
    #  href1 = code_spider.parse(html1)
    #  print(href1)

    for idx in range(2):
        t = threading.Thread(target=do_parse, args=(url_queue, html_queue),
                             name=f"idx-{idx}")
        t.start()

