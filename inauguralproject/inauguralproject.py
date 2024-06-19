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

    def utility_A(self,x1A,x2A):
        par = self.par
        return x1A**par.alpha*x2A**(1-par.alpha)

    def utility_B(self,x1B,x2B):
        par = self.par
        return x1B**par.beta*x2B**(1-par.beta)

    def demand_A(self,p1):
        par = self.par
        x1A = par.alpha * ((p1*par.w1A + par.w2A) / p1)
        # x1A = [par.alpha * ((price * par.w1A + par.w2A) / price) for price in p1]
        x2A = (1-par.alpha) * ((p1*par.w1A + par.w2A))
        #x2A = [(1-par.alpha) * ((price * par.w1A + par.w2A)) for price in p1]
        return x1A, x2A

        

    def demand_B(self,p1):
        par = self.par
        x1B = par.beta * ((p1*(1-par.w1A) + (1-par.w2A)) / p1)
        # x1B = [par.beta * ((price * (1-par.w1A) + (1-par.w2A)) / price) for price in p1]
        x2B = (1-par.beta) * ((p1*(1-par.w1A)+(1-par.w2A)))
        # x2B = [(1-par.beta) * ((price * (1-par.w1A) + (1-par.w2A))) for price in p1]
        return x1B, x2B

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2
    
    def excess_demand_x1(self, p1):

        par = self.par

        x1A, x2A  = self.demand_A(p1)
        x1B, x2B = self.demand_B(p1)

        #a. demand
        demand = x1A + x1B 

        #b. supply
        supply = 1 

        #c. excess demand
        excess_demand = demand - supply

        return excess_demand
    
    def excess_demand_x2(self, p1):

        x1A, x2A = self.demand_A(p1)
        x1B, x2B = self.demand_B(p1)

        #a. demand
        demand = x2A + x2B

        #b. supply
        supply = 1 

        #c. excess demand
        excess_demand = demand - supply

        return excess_demand
    
    #3.
    def find_equilibrium(self,p1_guess):
        
        par = self.par
        
        t=0
        p1 = p1_guess
        N = 2 # number of agents

        # loop
        while True:

            # 1. excess_demand
            z1 = self.excess_demand_x1(p1)

            # 2. stop coomand
            if np.abs(z1) < par.eps or t>=par.maxiter:
                print(f'{t:3d}: p1={p1:12.8f} -> exess demand -> {z1:14.8f}')
                break
            
            # 3. 
            if t<5 or t%25==0:
                print(f'{t:3d}: p1={p1:12.8f} -> exess demand -> {z1:14.8f}')

            elif t==5:
                print('     ...')

            # 4. 
            p1 = p1 + par.kappa*z1/N

            # 5. 
            t += 1 

        # Checjk if solution is found 
        if np.abs(z1) < par.eps:
            
            # store eguilibrium
            par.p1_star = p1 

            par.z1 = z1
            par.z2 = self.excess_demand_x2(par.p1_star)

            if not np.abs(par.z2) < par.eps: 
                print('the market for good 2 was not cleared')
                print(f'z2={par.z2}')
            
        else:
            print('solution was not found')

        
    
    def print_solution(self):

        par = self.par

        text = 'solution to market equilibrium:\n'
        text += f'p1 = {par.p1_star:5.3f}\n'
        text += 'p2 = 1\n'

        text += 'excess demand are:\n'
        text += f'z1 = {par.z1}\n'
        text += f'z2= {par.z2}'
        print(text)
    

    #4.a
    def find_best_choice_test(self,N,do_print=True): # ,do_print=True
        
        par = self.par
        # a. allocate numpy arrays
        shape_tuple = (N)
        #p1 = np.empty(shape_tuple)
        x1_values = np.empty(shape_tuple)
        x2_values = np.empty(shape_tuple)
        u_values = np.empty(shape_tuple)
    
        # b. start from guess of x1=x2=0
        x1_best = 0.01
        x2_best = 0.01
        u_best = self.utility_A(0.1,0.1)
    
        # c. loop through all possibilities
        for i in range(N):
        
            # p1[i] = (0.5 + 2*(i / N))
            # i. x1
            x1_values[i] = x1 = 1 - (par.beta * (((0.5 + 2*(i / N))*(1-par.w1A) + (1-par.w2A)) / (0.5 + 2*(i / N))))
        
            # ii. implied x2 by budget constraint
            x2_values[i] = x2 = 1 - (1-par.beta) * (((0.5 + 2*(i / N))*(1-par.w1A)+(1-par.w2A)))
            
            if x1_values[i] < 0 or x2_values[i] < 0:
                continue 

            # iii. utility    
            u_values[i] = self.utility_A(x1_values[i],x2_values[i])
        
            if u_values[i] >= u_best:    
                x1_best = x1_values[i]
                x2_best = x2_values[i] 
                u_best = u_values[i]
                p1 = (0.5 + 2*(i / N))
              

        return x1_best,x2_best,u_best,p1 #,x1_values,x2_values,u_values

    
    def find_best_choice_test_B(self): # ,do_print=True
        
        par = self.par
        p1_val = np.linspace(0.001, 10.000, 10000)
    
        # c. loop through all possibilities
        for p1 in p1_val:

            x1B,x2B = self.demand_B(p1)

            x1 = 1-x1B
            x2 = 1-x2B
            u_A_opt = self.utility_A(0.01,0.01)
            p1_opt = 0
            u_A = self.utility_A()

            if u_A(par.x1,par.x2) > u_A_opt:
                u_A_opt = u_A(x1,x2)
                p1_opt = p1


        return u_A_opt,p1_opt

    #4.b loop
    def find_best_choice_test_B_1(self): 
        par = self.par
        p1_val = np.linspace(0.001, 10.000, 100000)
        
        # Initialize variables to store the optimal utility and price
        u_A_opt = 0 
        p1_opt = 0
        
        # Loop through all possibilities of p1
        for p1 in p1_val:
            # Calculate demand for good B given p1
            x1B, x2B = self.demand_B(p1)
            
            # Calculate x1 and x2 for agent A
            x1 = 1 - x1B
            x2 = 1 - x2B
            
            # Calculate utility for agent A given x1 and x2
            u_A = self.utility_A(x1, x2)
            
            # Update optimal utility and price if current utility is higher
            if u_A > u_A_opt:
                u_A_opt = u_A
                p1_opt = p1

        return x1, x2, u_A_opt, p1_opt
    

    # 4.b using solver 
    def find_best_choice_any_price(self):
        par = self.par
        
        # Objective function to minimize (negative utility)
        def objective(p1):
            x1B, x2B = self.demand_B(p1)
            x1A, x2A = 1 - x1B, 1 - x2B
            return -self.utility_A(x1A, x2A)
        
        # Initial guess for p1
        p1_guess = 1.0
        
        # Use scipy.optimize.minimize to find the optimal p1
        result = optimize.minimize(objective, p1_guess, bounds=[(1e-8, None)], tol=par.eps)
        
        if result.success:
            optimal_p1 = result.x[0]
            x1B, x2B = self.demand_B(optimal_p1)
            x1A, x2A = 1 - x1B, 1 - x2B
            uA = self.utility_A(x1A, x2A)
            return x1A, x2A, uA, optimal_p1
        else:
            raise RuntimeError("Optimization failed to find a solution")

    
    def opgave_5_A(self): 
        par = self.par
        x1A_val = np.linspace(0.0, 1.0, 76)
        x2A_val = np.linspace(0.0, 1.0, 76)

        # Initialize variables to store the optimal utility and price
        u_A_opt = 0 
        x1A_opt = 0
        x2A_opt = 0
        u_B_initial = self.utility_B(1-par.w1A,1-par.w2A)
        
        # Loop through all possibilities of p1
        for x1A in x1A_val:
            for x2A in x2A_val:
                # Calculate demand for good B given p1
            
                # Calculate x1 and x2 for agent A
                x1B = 1 - x1A
                x2B = 1 - x2A
            
                # Calculate utility for agent A given x1 and x2
                u_A = self.utility_A(x1A,x2A)
                u_B = self.utility_B(x1B,x2B)
            
                # Update optimal utility and price if current utility is higher
                if u_A > u_A_opt and u_B >= u_B_initial:
                    u_A_opt = u_A
                    x1A_opt = x1A
                    x2A_opt = x2A

        return u_A_opt, x1A_opt, x2A_opt
    

    def opgave_5_B(self): 
        par = self.par
        x1A_val = np.linspace(0.0, 1.0, 5000)
        x2A_val = np.linspace(0.0, 1.0, 5000)

        # Initialize variables to store the optimal utility and price
        u_A_opt = 0 
        x1A_opt = 0
        x2A_opt = 0
        u_B_initial = self.utility_B(1-par.w1A,1-par.w2A)
        
        # Loop through all possibilities of p1
        for x1A in x1A_val:
            for x2A in x2A_val:
                # Calculate demand for good B given p1
            
                # Calculate x1 and x2 for agent A
                x1B = 1 - x1A
                x2B = 1 - x2A
            
                # Calculate utility for agent A given x1 and x2
                u_A = self.utility_A(x1A,x2A)
                u_B = self.utility_B(x1B,x2B)
            
                # Update optimal utility and price if current utility is higher
                if u_A > u_A_opt and u_B >= u_B_initial:
                    u_A_opt = u_A
                    x1A_opt = x1A
                    x2A_opt = x2A

        return u_A_opt, x1A_opt, x2A_opt
    
    # 5.b
    def opgave_5_B_solver(self):
        par = self.par

        # Initial utility for B at the initial endowment
        u_B_initial = self.utility_B(1 - par.w1A, 1 - par.w2A)
        
        # Objective function to minimize (negative utility of A)
        def objective(x):
            x1A, x2A = x
            return -self.utility_A(x1A, x2A)

        # Constraint: B's utility must be at least as high as the initial utility
        def constraint(x):
            x1A, x2A = x
            x1B = 1 - x1A
            x2B = 1 - x2A
            return self.utility_B(x1B, x2B) - u_B_initial

        # Initial guess for x1A and x2A
        x0 = [0.5, 0.5]
        
        # Bounds for x1A and x2A (between 0 and 1)
        bounds = [(0, 1), (0, 1)]
        
        # Constraint dictionary
        con = {'type': 'ineq', 'fun': constraint}

        # Use scipy.optimize.minimize to find the optimal allocation
        result = optimize.minimize(objective, x0, bounds=bounds, constraints=[con], tol=par.eps)
        
        if result.success:
            x1A_opt, x2A_opt = result.x
            u_A_opt = self.utility_A(x1A_opt, x2A_opt)
            return u_A_opt, x1A_opt, x2A_opt
        else:
            raise RuntimeError("Optimization failed to find a solution")

    def opgave_6_A(self): 
        par = self.par
        x1A_val = np.linspace(0.0, 1.0, 5000)
        x2A_val = np.linspace(0.0, 1.0, 5000)

        # Initialize variables to store the optimal utility and price
        u_A_initial = self.utility_A(par.w1A,par.w2A) 
        x1A_opt = 0
        x2A_opt = 0
        u_B_initial = self.utility_B(1-par.w1A,1-par.w2A)
        u_initial = u_A_initial + u_B_initial
        
        # Loop through all possibilities of p1
        for x1A in x1A_val:
            for x2A in x2A_val:
                # Calculate demand for good B given p1
            
                # Calculate x1 and x2 for agent A
                x1B = 1 - x1A
                x2B = 1 - x2A
            
                # Calculate utility for agent A given x1 and x2
                u_A = self.utility_A(x1A,x2A)
                u_B = self.utility_B(x1B,x2B)
                social_u = u_A + u_B
            
                # Update optimal utility and price if current utility is higher
                if  social_u > u_initial:
                    x1A_opt = x1A
                    x2A_opt = x2A
                    u_initial = social_u

        return x1A_opt, x2A_opt