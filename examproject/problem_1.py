from types import SimpleNamespace
import numpy as np
from scipy import optimize

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

        # c. div
        par.eps = 1e-8 #tolerance 
        par.maxiter = 500 # iter
        par.kappa = 1 # 0.1