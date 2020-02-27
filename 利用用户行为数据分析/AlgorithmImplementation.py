# coding = utf-8

import math
import random
from Metric import *
from tqdm import tqdm
import time

def UserRecommend(train, K, N, AlgorType='UserCF'):
    '''
    train: 训练数据集
    K: 取TopK相似用户数目
    N: 超参数，设置取TopN推荐物品数目
    return: GetRecommendation,推荐接口函数
    '''
    # 余弦相似度，时间复杂度O(|U|*|U|)
    # def UserSimilarity(train):
    #     W = dict()
    #     for u in train.keys():
    #         for v in train.keys():
    #             if u == v:
    #                 continue
    #             W[u][v] = len(train[u] & train[v])
    #             W[u][v] = math.sqrt(len(train[u]) * len(train[v]) * 1.0)

    #     return W

    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i in items:
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    # calculate co-rated items between users
    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u in users:
            if u not in N:
                N[u] = 0
            N[u] += 1
            if u not in C:
                C[u] = {}
            for v in users:
                if u == v:
                    continue
                
                if v not in C[u]:
                    C[u][v] = 0
                if AlgorType == 'UserCF':
                    C[u][v] += 1
                # 增加如热门产品的惩罚， User-IIf算法
                else:
                    C[u][v] += 1 / math.log(1 + len(users))

    # calculate finial similarity matrix C
    for u in C:
        for v in C[u]:
            C[u][v] /= math.sqrt(N[u] * N[v])

    sorted_user_sim = {k:list(sorted(v.items(), \
                              key=lambda x: x[1], reverse=True))\
                              for k, v in C.items()}
        
    def GetRecommendation(user):
        items = dict()
        interacted_items = set(train[user])
        for u, _ in sorted_user_sim[user][:K]:
            for item in train[u]:
                if item not in interacted_items:
                    # We should filter items user interacted before continue
                    if item not in items:
                        items[item] = 0 
                    items[item] += C[user][u]

        recs = list(sorted(items.items(), key=lambda x: x[1], reverse=True))[:N]
        
        return recs
    
    return GetRecommendation




