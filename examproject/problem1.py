import numpy as np
from types import SimpleNamespace
from scipy import optimize
from scipy.optimize import fsolve
from scipy.optimize import minimize_scalar

class ProductionEconomyClass:
    def __init__(self):
        self.par = SimpleNamespace()

        # Parameters initialization
        self.par.A = 1.0
        self.par.gamma = 0.5
        self.par.alpha = 0.3
        self.par.nu = 1.0
        self.par.epsilon = 2.0
        self.par.tau = 0.0
        self.par.T = 0.0
        self.par.kappa = 0.1

    def utility(self, c1, c2, l):
        """utility for consumer"""
        par = self.par
        return np.log(c1 ** par.alpha * c2 ** (1 - par.alpha)) - par.nu * l**(1 + par.epsilon) / (1 + par.epsilon)

    def consumer(self, p_1, p_2, w):
        """maximize utility for consumer"""
        par = self.par

        # Calculate profit terms pi_1 and pi_2
        pi_1 = ((1 - par.gamma) / par.gamma) * w * ((p_1 * par.A * par.gamma) / w) ** (1 / (1 - par.gamma))
        pi_2 = ((1 - par.gamma) / par.gamma) * w * ((p_2 * par.A * par.gamma) / w) ** (1 / (1 - par.gamma))

        def obj(l):
            c1 = par.alpha * (w * l + par.T + pi_1 + pi_2) / p_1
            c2 = (1 - par.alpha) * (w * l + par.T + pi_1 + pi_2) / (p_2 + par.tau)  # Corrected line
            return -self.utility(c1, c2, l)

        # Optimize labor supply
        res = optimize.minimize_scalar(obj, bounds=(0, 1), method='bounded')
        l_star_c = res.x
        c1_star_c = par.alpha * (w * l_star_c + par.T + pi_1 + pi_2) / p_1
        c2_star_c = (1 - par.alpha) * (w * l_star_c + par.T + pi_1 + pi_2) / (p_2 + par.tau)
        
        return c1_star_c, c2_star_c, l_star_c
    
    def print_consumer(self):
        """print consumer results"""
        w = 1.0
        for p_1 in [0.5, 1, 1.5]:
            for p_2 in [0.5, 1, 1.5]:
                c1, c2, l = self.consumer(p_1, p_2, w)
                print(f'p_1 = {p_1:.2f}, p_2 = {p_2:.2f} -> c1 = {c1:.2f}, c2 = {c2:.2f}, l = {l:.2f}') 

    def firm_1(self, p_1, w):
        """maximize profit for firm 1"""
        par = self.par

        l_star_f1 = ((p_1 * par.A * par.gamma) / w) ** (1 / (1 - par.gamma))
        y_star_f1 = par.A * (l_star_f1) ** par.gamma
        pi_star_f1 = ((1 - par.gamma) / par.gamma) * w * ((p_1 * par.A * par.gamma) / w) ** (1 / (1 - par.gamma))

        return l_star_f1, y_star_f1, pi_star_f1

    def firm_2(self, p_2, w):
        """maximize profit for firm 2"""
        par = self.par

        l_star_f2 = ((p_2 * par.A * par.gamma) / w) ** (1 / (1 - par.gamma))
        y_star_f2 = par.A * (l_star_f2) ** par.gamma
        pi_star_f2 = ((1 - par.gamma) / par.gamma) * w * ((p_2 * par.A * par.gamma) / w) ** (1 / (1 - par.gamma))

        return l_star_f2, y_star_f2, pi_star_f2  

    def print_firm(self):
        """print firm results"""
        w = 1.0
        for p_1 in [0.5, 1, 1.5]:
            l_star_f1, y_star_f1, pi_star_f1 = self.firm_1(p_1, w)
            print(f'p_1 = {p_1:.2f} -> l_star_f1 = {l_star_f1:.2f}, y_star_f1 = {y_star_f1:.2f}, pi_stat_f1 = {pi_star_f1:.2f}')

        for p_2 in [0.5, 1, 1.5]:
            l_star_f2, y_star_f2, pi_star_f2 = self.firm_2(p_2, w)
            print(f'p_2 = {p_2:.2f} -> l_star_f2 = {l_star_f2:.2f}, y_star_f2 = {y_star_f2:.2f}, pi_stat_f2 = {pi_star_f2:.2f}')

    def market_clearing(self):
        # Check market clearing conditions
        par = self.par 
        w = 1  # Numeraire

        # Price ranges
        p1_range = np.linspace(0.1, 2.0, 10)
        p2_range = np.linspace(0.1, 2.0, 10)

        market_clearing_results = []

        for p1 in p1_range:
            for p2 in p2_range:
                c1_star_c, c2_star_c, l_star_c = self.consumer(p1, p2, w)
                l_star_f1, y_star_f1, pi_star_f1 = self.firm_1(p1, w)
                l_star_f2, y_star_f2, pi_star_f2 = self.firm_2(p2, w)
                
                # Market clearing conditions
                market_clearing_y1 = np.isclose(y_star_f1, c1_star_c)
                market_clearing_y2 = np.isclose(y_star_f2, c2_star_c)
                
                market_clearing_results.append((p1, p2, market_clearing_y1, market_clearing_y2))

        # Display results
        print("p1\tp2\tMarket Clearing for Good 1\tMarket Clearing for Good 2")
        for result in market_clearing_results:
            p1, p2, market_clearing_y1, market_clearing_y2 = result
            print(f"{p1:.2f}\t{p2:.2f}\t{market_clearing_y1}\t\t\t{market_clearing_y2}")

    def equilibrium(self):
        # Find equilibrium prices
        par = self.par 
        w = 1

        # Market clearing conditions
        def equlibrium(prices):
            p_1, p_2 = prices
            c1_star_c, c2_star_c, l_star_c = self.consumer(p_1, p_2, w)
            l_star_f1, y_star_f1, pi_star_f1 = self.firm_1(p_1, w)
            l_star_f2, y_star_f2, pi_star_f2 = self.firm_2(p_2, w)
            
            # Market clearing conditions
            market_clearing_y1 = y_star_f1 - c1_star_c
            market_clearing_y2 = y_star_f2 - c2_star_c
            
            return [market_clearing_y1, market_clearing_y2]

        # Initial guess for prices
        initial_guess = [0.1, 0.1]

        # Solve for equilibrium prices
        equilibrium_prices = fsolve(equlibrium, initial_guess)
        p1_eq, p2_eq = equilibrium_prices
        print(f"Equilibrium price for good 1: {p1_eq}")
        print(f"Equilibrium price for good 2: {p2_eq}")
    
    def check_specific_prices(self):
        w = 1.0
        p1_vals = np.linspace(0.9759308856158176, 0.9759308856158176, 1)
        p2_vals = np.linspace(1.4907590521266094, 1.4907590521266094, 1)

        for p_1 in p1_vals:
            for p_2 in p2_vals:
                c1_star_c, c2_star_c, l_star_c = self.consumer(p_1, p_2, w)
                l_star_f1, y_star_f1, pi_star_f1 = self.firm_1(p_1, w)
                l_star_f2, y_star_f2, pi_star_f2 = self.firm_2(p_2, w)
                l_sum = l_star_f1 + l_star_f2
                clear_market_1 = c1_star_c - y_star_f1
                clear_market_2 = c2_star_c - y_star_f2
                clear_labor_market = l_star_c - l_sum

                if clear_market_1 < 0.09 and clear_market_2 < 0.09 and clear_labor_market < 0.09:
                    print(f'p_1 = {p_1:.4f}, p_2 = {p_2:.4f} -> clear_market_1 = {clear_market_1:.10f} -> clear_market_2 = {clear_market_2:.10f} -> clear_labor_market = {clear_labor_market:.10f}')

    
    def social_planner(self):
        par = self.par
        w = 1.0
        
        def social_welfare(tau, par):
            p1 = 1
            p2 = 1
            # Calculate c2_star_c within the social_welfare function
            c1_star_c, c2_star_c, l_star_c = self.consumer(p1, p2, w)
            T = tau * c2_star_c  # Update T based on c2_star_c
            l_star_f1, y_star_f1, pi_star_f1 = self.firm_1(p1, w)
            l_star_f2, y_star_f2, pi_star_f2 = self.firm_2(p1, w)
            u = np.log(c1_star_c**par.alpha * c2_star_c**(1 - par.alpha)) - par.nu * l_star_c**(1 + par.epsilon) / (1 + par.epsilon)
            return -(u - par.kappa * y_star_f2)  # Negate for minimization
        
        # Initial guess for c2 to estimate T
        par.tau = 0.1
        par.T = 0.1 * 0.5
        l_star_f1, y_star_f1, pi_star_f1 = self.firm_1(1, w)
        l_star_f2, y_star_f2, pi_star_f2 = self.firm_2(1, w)
        c1_star_c, c2_star_c, l_star_c = self.consumer(1, 1, w)
        u = np.log(c1_star_c**par.alpha * c2_star_c**(1 - par.alpha)) - par.nu * l_star_c**(1 + par.epsilon) / (1 + par.epsilon)

        # Optimize tau to maximize social welfare
        result = minimize_scalar(lambda tau: social_welfare(tau, par), bounds=(0, 1), method='bounded')
        optimal_tau = result.x

        # Calculate T based on optimal tau
        par.tau = optimal_tau
        par.T = optimal_tau * c2_star_c
        l_star_f1, y_star_f1, pi_star_f1 = self.firm_1(1, w)
        l_star_f2, y_star_f2, pi_star_f2 = self.firm_2(1, w)
        c1_star_c, c2_star_c, l_star_c = self.consumer(1, 1, w)
        u = np.log(c1_star_c**par.alpha * c2_star_c**(1 - par.alpha)) - par.nu * l_star_c**(1 + par.epsilon) / (1 + par.epsilon)
        optimal_T = optimal_tau * c2_star_c

        print(f"Optimal tau: {optimal_tau}")
        print(f"Optimal T: {optimal_T}")
            
