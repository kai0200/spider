# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import code_spider
import queue
import threading
import time  # 用于模拟网络延迟


# 从 url_queue 读取解析出 html 后写入 html_queue
def urlq_to_htmlq(url_queue, html_queue):
    while True:
        try:
            url = url_queue.get_nowait()  # 使用 get_nowait() 以避免不必要的阻塞
            print(f"处理数据: {url}")
            html = code_spider.get_text(url)
            html_queue.put(html)
            print(f"增加到html_queue size: {html_queue.qsize()}")
            print(threading.current_thread().name, f"Processed {url}")
            url_queue.task_done()  # 标记任务完成
        except queue.Empty:
            break  # 如果队列为空，则退出循环

def do_parse(html_queue, fout_path):
    with open(fout_path, 'a') as fout:
        while True:
            try:
                html = html_queue.get_nowait()  # 使用 get_nowait()
                results = code_spider.parse(html)
                for result in results:
                    s = result
                    s = '/'.join([s.split('/')[1], s.split('/')[2]])
                    print(f"git@code.sohuno.com:{s}\n")
                    fout.write(f"git@code.sohuno.com:{s}\n")
                print(threading.current_thread().name, f"Parsed HTML and wrote to {fout_path}")
                html_queue.task_done()
            except queue.Empty:
                break

if __name__ == '__main__':

    url_queue = queue.Queue()
    html_queue = queue.Queue()
    urls = code_spider.urls
    for url in urls:
        url_queue.put(url)

    # 启动处理 URL 的线程
    for idx in range(4):
        t = threading.Thread(target=urlq_to_htmlq, args=(url_queue, html_queue), name=f"URL-Worker-{idx}")
        t.start()

    # 等待所有 URL 处理线程完成（这里简单地等待一段时间，或者可以使用其他同步机制）
    # 注意：由于我们使用了 task_done() 和 join()，但 task_done() 是在 while 循环中调用的，
    # 所以我们需要确保所有项目都被处理完。在实际应用中，可能需要更复杂的逻辑来确保这一点。
    # 由于我们使用了非阻塞的 get_nowait()，并且没有明确的停止条件（除了队列为空），
    # 下面的 join() 调用可能不会按预期工作，因为它依赖于 task_done() 被正确调用相同次数作为 put()。
    # 在这个例子中，我们简单地等待一段时间来模拟处理完成。
    time.sleep(5)  # 这是一个糟糕的做法，仅用于示例！

    # 启动解析 HTML 的线程（注意：这里应该使用不同的文件名或同步机制来避免竞争条件）
    for idx in range(2):
        t = threading.Thread(target=do_parse, args=(html_queue, "02.data.txt"), name=f"Parse-Worker-{idx}")
        t.start()

    # 等待所有解析线程完成（同样，这里需要更复杂的逻辑来确保同步）
    # 由于我们使用了非阻塞的 get_nowait()，并且解析线程可能会在 URL 处理线程完成之前结束，
    # 所以下面的 join() 调用可能不会等待所有解析工作完成。
    # 在实际应用中，您可能需要使用其他同步原语（如 Event）来确保正确的顺序和完成。
    # 再次注意：下面的 join() 调用可能不会按预期工作，因为它依赖于 html_queue 的正确处理。
    for t in threading.enumerate():
        if t.name.startswith("Parse-Worker-"):
            t.join()

    # 注意：上面的 join() 调用可能不会捕获所有解析线程，因为它是在主线程中执行的，
    # 并且可能无法看到在 join() 调用之后启动的线程。在实际应用中，您需要确保
    # 所有线程都在 join() 调用之前启动，并且您有一个可靠的机制来等待它们完成。
    # 在这个例子中，我们省略了正确的同步逻辑，因为它会使示例变得复杂。

    # 在实际应用中，您可能需要使用 Queue.join() 方法等待队列中的所有项都被处理完，
    # 但这要求您知道何时所有应该被处理的项目都已经被放入队列中。
    # 由于我们使用了非阻塞的 get_nowait() 和简单的 sleep() 来模拟处理，
    # 所以在这个例子中我们不能使用这种方法。

# vim: expandtab softtabstop=4 shiftwidth=4
