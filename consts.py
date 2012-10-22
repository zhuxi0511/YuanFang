#coding:utf-8
import random

YUANFANGREPLY = [
    ('大人真乃神人也', 5000),
    ('我觉得此事定有蹊跷', 5000),
    ('楼上是白痴', 500),
    ('我用快播看', 500),
    ('此事之后必定有大阴谋', 2000),
    ('大人我还没想好', 2000),
    ('大人都问我，你干什么吃的', 1000),
    ('大人，属下与此事无关', 1000),
    ('对呀，大人。卑职怎么就没想到呢', 1000),
    ('从我多年的办案经验判断，事情没有这么简单', 1000),
    ('正如大人所料……', 5000),
    ('没错，卑职也是这么想的。', 5000),
    ('明白了，彻底地明白了', 5000),
]

def roll():
    up = len(YUANFANGREPLY)
    while True:
        x = random.randint(0, up - 1)
        y = random.randint(0, 10000)
        if y < YUANFANGREPLY[x][1]:
            return YUANFANGREPLY[x][0]
