import math
from algImplement import userRecommend, itemRecommend
from metric import *
from dataset import *

class Experiment():
    
    def __init__(self, M, K, N, fp='../Dataset/ml-1m/ratings.dat', rt='UserCF'):
        ''' 
        M: 进行多少次实验
        K: TopK相似用户个数
        N: TopN推荐物品的个数
        '''

        self.M = M
        self.K = K
        self.N = N
        self.rt = rt
        self.fp = fp
        
    @timmer
    def worker(self, train, test, rt):

        if self.rt == 'UserCF' or self.rt == 'UserIIF':
            getRecommendation = userRecommend(train, self.K, self.N, self.rt)
        else:
            getRecommendation = itemRecommend(train, self.K, self.N, self.rt)
        metric = Metric(train, test, getRecommendation)

        return metric.eval()

    @timmer
    def run(self):
        metrics = {'Precision': 0, 'Recall': 0, 
                    'Coverage': 0, 'Popularity': 0}
        dataset = Dataset(self.fp)
        # for ii in range(self.M):
        for ii in range(2):
            train, test = dataset.splitData(self.M, ii)
            print('Experiment {}:'.format(ii))
            metric = self.worker(train, test, self.rt)
            metrics = {k: metrics[k]+metric[k] for k in metrics}
        # metrics = {k: metrics[k] / self.M for k in metrics}
        metrics = {k: metrics[k] / 2 for k in metrics}
        print('Average Result (M={}, K={}, N={}): {}'.format(\
                            self.M, self.K, self.N, metrics))

if __name__ == "__main__":
    M, N = 8,10
    K = 10
    # 基于用户的协同滤波
    # random_exp_cf = Experiment(M, K, N, rt='UserCF')
    # random_exp_cf.run()
    # random_exp_iif = Experiment(M, K, N, rt='UserIIF')
    # random_exp_iif.run()

    # 基于物品的协同滤波
    # random_exp_cf = Experiment(M, K, N, rt='ItemCF')
    # random_exp_cf.run()
    random_exp_cf = Experiment(M, K, N, rt='ItemIUF')
    random_exp_cf.run()
    # random_exp_cf = Experiment(M, K, N, rt='ItemCF_norm')
    # random_exp_cf.run()