import math
from AlgorithmImplementation import UserRecommend
from Metric import *
from Dataset import *

class Experiment():
    
    def __init__(self, M, K, N, fp='/Users/wangzhou/Documents/code/RecommendedSystem/Dataset/ml-1m/ratings.dat', rt='UserCF'):
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
    def worker(self, train, test):
        getRecommendation = UserRecommend(train, self.K, self.N, AlgorType='UserCF')
        metric = Metric(train, test, getRecommendation)

        return metric.eval()

    @timmer
    def run(self):
        metrics = {'Precision': 0, 'Recall': 0, 
                    'Coverage': 0, 'Popularity': 0}
        dataset = Dataset(self.fp)
        for ii in range(self.M):
            train, test = dataset.splitData(self.M, ii)
            print('Experiment {}:'.format(ii))
            metric = self.worker(train, test)
            metrics = {k: metrics[k]+metric[k] for k in metrics}
        metrics = {k: metrics[k] / self.M for k in metrics}
        print('Average Result (M={}, K={}, N={}): {}'.format(\
                            self.M, self.K, self.N, metrics))

if __name__ == "__main__":
    M, N = 9,10
    K = 80
    random_exp_cf = Experiment(M, K, N, rt='UserCF')
    random_exp_cf.run()
    # random_exp_iif = Experiment(M, K, N, rt='UserIIF')