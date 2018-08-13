import asyncio
# 参考廖雪峰教程  https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432090954004980bd351f2cd4cc18c9e6c06d855c498000
# 把一个generator标记为coroutine类型
@asyncio.coroutine
def func1():
    print('before...func1......')
    # yield from语法可以让我们方便地调用另一个generator
    yield from asyncio.sleep(5)
    print('end...func1......')


tasks = [func1(), func1()]
# 获取EventLoop
loop = asyncio.get_event_loop()
# 把coroutine扔到EventLoop中执行
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()