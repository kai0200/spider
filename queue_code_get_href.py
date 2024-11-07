# -*- coding: utf-8 -*-
import queue
import code_spider
import time
import threading


def do_craw(url_queue: queue.Queue, html_queue: queue.Queue):
    while True:
        url = url_queue.get()
        html = code_spider.get_text(url)
        html_queue.put(html)
        print(threading.current_thread().name, f"code {url}",
              "url_queue=size:", url_queue.qsize())


def do_parse(html_queue: queue.Queue, fout):
    while True:
        html = html_queue.get()
        results = code_spider.parse(html)
        for result in results:
            print(str(result) + "\n")
            fout.write(str(result) + '\n')
            print(threading.current_thread().name, f"results.size", len(results),
                  "html_queue.size=", html_queue.qsize())


if __name__ == '__main__':
    url_queue = queue.Queue()
    html_queue = queue.Queue()

    for url in code_spider.urls:
        url_queue.put(url)

    for idx in range(4):
        t = threading.Thread(target=do_craw, args=(url_queue, html_queue),
                             name=f"code-{idx}")
        t.start()

    fout = open("02.data.txt", 'w')

    for idx in range(2):
        t = threading.Thread(target=do_parse, args=(html_queue, fout),
                             name=f"parse{idx}")
        t.start()
# vim: expandtab softtabstop=4 shiftwidth=4
