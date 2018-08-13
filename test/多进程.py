from concurrent.futures import ProcessPoolExecutor
import requests

# 线程执行的任务
def task(url):
    response = requests.get(url)
    return response

# 线程执行完回调函数
def done(future, *arge, **kwargs):
    # 获取到线程返回的数据
    response = future.result()
    print(response.status_code, response.content)

# 创建线程池
pool = ProcessPoolExecutor(7)
url_list = [
    'http://www.baidu.com',
    'http://www.baidu.com',
    'http://www.baidu.com',
    'http://www.baidu.com',
    'http://www.baidu.com',
    'http://www.baidu.com',
    'http://www.baidu.com',
    'http://www.baidu.com',
    'http://www.baidu.com',
]
for url in url_list:
    # 将任务添加到线程池
    v = pool.submit(task, url)
    # 添加线程任务执行结束后的回调函数
    v.add_done_callback(done)
# wait=True等待线程池的自线程执行完，再往下执行主线程
pool.shutdown(wait=True)
print('end')