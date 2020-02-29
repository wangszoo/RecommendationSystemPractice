# coding = utf-8

# 加载和分割数据集

import random
import math
from metric import *

class Dataset():

    def __init__(self, fp):
        # fp: filepath
        self.data = self.loadData(fp)

    @timmer
    def loadData(self, fp):
        data = []
        for l in open(fp):
            data.append(tuple(map(int, l.strip().split('::')[:2])))
        
        return data
        
    @ timmer
    def splitData(self, M, k, seed=1):
        '''
        data: 加载所有(user, item)数据条目
        M: 划分的数目
        k: 本次是第几次划分
        seed: random的种子数，对于不同的k设置成一样的

        return: train, test
        '''
        # 数据集的划分
        test = []
        train = []
        random.seed(seed)
        for user, item in self.data:
            if random.randint(0,M) == k:
                test.append([user, item])
            else:
                train.append([user,item])
            
        # 处理程字典的形式
        def convert_dict(data):
            data_dict = {}
            for user, item in data:
                if user not in data_dict:
                    data_dict[user] = set()
                data_dict[user].add(item)

            data_dict = {k:list(data_dict[k]) for k in data_dict}

            return data_dict
            
        return convert_dict(train), convert_dict(test)

# if __name__ == '__main__':
#     data = Dataset(fp='../Dataset/ml-1m/ratings.dat')