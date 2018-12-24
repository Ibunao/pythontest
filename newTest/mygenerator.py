#!/usr/bin/env python3
# -*-coding:utf-8-*-
'''
测试生成器的send数据
'''
# def test():
#     i = 1
#     print('one line')
#     temp = yield i
#     i += 1
#     print('two line', temp)
#     yield i
#
# # 获取生成器
# gen = test()
#
# # one line
# next(gen)
#
# # 这个send的数据是发送给上一个yield点上进行接收的
# # two line haha
# gen.send('haha')

'''
测试 yeild from
'''
def htest():
    i = 1
    while i < 4:
        print('i的值', i)
        n = yield i
        print('n的值', n)
        if i == 3:
            return 100
        i += 1


def itest():
    val = yield from htest()
    print('val的值', val)

t = itest()

# i的值 1
t.send(None)

# n的值 haha
# i的值 2
t.send('haha')

# n的值 here
# i的值 3
t.send('here')

try:
    # n的值 hehe
    # val的值 100
    t.send('hehe')
except StopIteration as e:
    # 异常了 None
    print('异常了', e.value)