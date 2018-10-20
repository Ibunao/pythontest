#!/usr/local/bin python3
# -*-coding:utf-8-*-
import redis
import time
# 链接redis
conn = redis.Redis(host='127.0.0.1',port=6609,db=0)

# 一周的秒数
ONE_WEEK_IN_SECONDS = 7 * 86400
# 没个赞增加的积分数
VOTE_SCORE = 432

def article_vote(conn, user, article):
    '''
    投票函数
    :param conn:  redis资源
    :param user:  用户 user:id
    :param article:  文章 article:id
    :return:
    '''
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    # 如果创建文章的时间，如果已经一星期之前的，则不能再点赞
    if conn.zscore('time:', article) < cutoff:
        return
    # 获取文章id
    article_id = article.partition(':')[-1]
    # 如果没有投票，记录对此文章投票的人，并增加积分
    if conn.sadd('voted:'+article_id, user):
        # 增加此文章的积分数
        conn.zincrby('score:', article, VOTE_SCORE)
        # 增加文章的点赞数
        conn.hincrby(article, 'votes', 1)

def post_article(conn, user, title, article_id):
    '''
    创建文章
    :param conn:  redis资源
    :param user:  用户 user:id
    :param title: 题目
    :param article_id: 文章id
    :return:
    '''
    voted = 'voted:' + article_id
    # 把作者添加到此文章的点赞栏
    conn.sadd(voted, user)
    # 一星期后释放此文章的点赞人
    conn.expire(voted, ONE_WEEK_IN_SECONDS)
    now = time.time()
    article = 'article:' + article_id
    # 存储文章信息
    conn.hmset(article, {
        'title' : title,
        'poster': user,
        'time' : now,
        'votes' : 1,
    })
    # 存储此文章的分值
    conn.zadd('score:', article, now + VOTE_SCORE)
    # 存储此文章的时间
    conn.zadd('time:', article, now)

ARTICELS_PER_PAGE = 25
def get_articles(conn, page, order = 'score:'):
    '''
    根据分值或创建时间获取文章
    :param conn: redis资源
    :param page: 页码
    :param order: 根据哪个有序集合获取数据，默认是分值score:
    :return: 文章信息列表
    '''
    # 计算开始
    start = (page - 1)*ARTICELS_PER_PAGE
    # 计算结尾
    end = start + ARTICELS_PER_PAGE - 1
    # 获取分值排序后的 start位到end位之间的数据
    ids = conn.zrevrange(order, start, end)
    # 存储符合的文章
    articles = []
    for id in ids:
        # 获取该文章的信息
        article_data = conn.hgetall(id)
        article_data['id'] = id
        articles.append(article_data)
    return articles

def add_remove_grouops(conn, article_id, to_add = [], to_remove = []):
    '''
    把文章添加／移除到某些组
    :param conn: redis资源
    :param article_id: 文章id
    :param to_add:  要添加的组列表
    :param to_remove: 要删除的组列表
    :return:
    '''
    article = 'article:' + article_id
    # 要添加到的组
    for group in to_add:
        conn.sadd('group:' + group, article)
    # 要移除的组
    for group in to_remove:
        conn.srem('group:' + group, article)

def get_group_articles(conn, group, page, order = 'score:'):
    '''
    获取组内指定页的文章
    :param conn: redis资源
    :param group: 组id
    :param page: 页码
    :param order: 根据哪个排序 分值score: 或 时间time:
    :return: 文章列表
    '''
    # 存储组文章排序的key
    key = order + group
    # 查看是否已经存在，避免频繁的计算
    if not conn.exists(key):
        # 获取 集合'group:' + group 与 有序集合 order 的交集并将结果集存储在新的有序集合 key 中
        # 集合 'group:' + group 中值对应的分值为1
        # aggregate = 'max' 表示取交集中分值较大的分值
        conn.zinterstore(key,
            ['group:' + group, order],
            aggregate = 'max'
        )
        conn.expire(key, 60)
    # 获取文章
    return get_articles(conn, page, key)

if __name__ == '__main__':
    print('main')
