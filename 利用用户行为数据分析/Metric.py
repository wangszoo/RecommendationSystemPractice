# coding = utf-8

# 基于用户行为的推荐，协同滤波

import random
import math
import time
class Metric:

    def __init__(self, train, test, GetRecommendation):
        self.train = train
        self.test = test
        self.GetRecommendation = GetRecommendation
        self.recs = self.getRec()

    # 为每个用户推荐
    def getRec(self):
        recs = {}
        for user in self.test:
            rank = self.GetRecommendation(user)
            recs[user] = rank

        return recs

    # Recall and Precision
    def Recall(self):
        hit = 0
        all = 0
        for user in self.test:
            tu = self.test[user]
            rank = self.recs[user]
            for item, _ in rank:
                if item in tu:
                    hit += 1
            all += len(tu)

        return hit / (all * 1.0)

    def Precision(self):
        hit = 0
        all = 0
        for user in self.train.keys():
            tu = self.test[user]
            rank = self.recs[user]
            for item, _ in rank:
                if item in tu:
                    hit += 1
            all += NameError
        
        return hit / (all * 1.0)

    # 覆盖率
    def Coverage(self):
        recommend_items = set()
        all_items = set()
        for user in self.test:
            for item in self.train[user].keys:
                all_items.add(item)
            rank = self.recs[user]
            for item, _ in rank:
                recommend_items.add(item)

        return len(recommend_items) / (len(all_items) * 1.0)

    # 新颖度
    def Popularity(self):
        item_popularity = dict()
        # 统计训练集中的物品的流行度
        for user, items in self.train.items():
            for item in items.keys():
                if item in item.keys():
                    item_popularity[item] = 0
                item_popularity[item] += 1
        
        ret = 0
        n = 0
        for user in self.train.keys():
            rank = self.recs[user]
            for item, _ in rank:
                # 取对数，因为流行度满足长尾分布，取对数后，流行度更加稳定
                ret += math.log(1 + item_popularity[item])
                n += 1
        
        ret /= n * 1.0
        return ret

    def eval(self):
        metric = {'Precision': self.Precision(),
                  'Recall': self.Recall(),
                  'Coverage': self.Coverage(),
                  'Popularity': self.Popularity()}
        
        print(metric)

        return metric


# 定义装饰起，监控运行时间
# https://github.com/Magic-Bubble/RecommendSystemPractice/blob/master/Chapter2
def timmer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        stop_time = time.time()
        print('Func %s, run time: %s' % (func.__name__, stop_time - start_time))
        return res
    
    return wrapper