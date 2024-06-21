from scipy import optimize
import sympy as sm
import numpy as np

  
def define_symbols():
    # defining the symbols of the pricipal-agent model
    L = sm.symbols('L')
    M = sm.symbols('M')
    pi = sm.symbols('pi')
    c_1 = sm.symbols('c_1')
    c_2 = sm.symbols('c_2')
    lam = sm.symbols('lambda')
    v_overline = sm.symbols(r'\overline{v}')
    v = sm.Function('v')
    return L, M, pi, c_1, c_2, lam, v_overline, v

def calculate_derivatives(L, M, pi, c_1, c_2, lam, v_overline, v):
    # We define v differentiated with respect to respectively c_1 and c_2
    v_diff_c1 = sm.diff(v(c_1), c_1)
    v_diff_c2 = sm.diff(v(c_2), c_2)
    
    # equations
    principal = (M - (pi * L) - ((1 - pi) * c_1) - (pi * c_2))
    condition = pi * v(c_2) + (1 - pi) * v(c_1) - v_overline
    lagrange = principal + lam * condition
    
    # Find the partial derivatives
    Lc_1 = sm.Eq(0, sm.diff(lagrange, c_1))
    Lc_2 = sm.Eq(0, sm.diff(lagrange, c_2))
    Llam = sm.Eq(0, sm.diff(lagrange, lam))
    
    return principal, condition, lagrange, Lc_1, Lc_2, Llam, v_diff_c1, v_diff_c2

def solve_equations(Lc_1, Lc_2, Llam, v_diff_c1, v_diff_c2):
    # solve for v_diff_c1 and v_diff_c2 
    solution = sm.solve([Lc_1, Lc_2, Llam], (v_diff_c1, v_diff_c2))
    return solution 

class numerical_solution:
    
    def __init__(self):
        self.results = []

    def parameter(self, K, gamma, pi):
        M = 50
        L = 5
        rho = 0.3

        # Compute consumptions
        c1 = M - gamma
        c2 = M - gamma - L + K

        return M, L, pi, rho, c1, c2

    def principal_problem(self, x, pi):
        K, gamma = x
        M, L, pi, rho, c1, c2 = self.parameter(K, gamma, pi)
        return -(M - pi * L - (1 - pi) * c1 - pi * c2)

    def agent_utility(self, c, rho):
        return c**(1 - rho) / (1 - rho)

    def constraint(self, x, pi):
        K, gamma = x
        M, L, pi, rho, c1, c2 = self.parameter(K, gamma, pi)
        return pi * self.agent_utility(c2, rho) + (1 - pi) * self.agent_utility(c1, rho) - (pi * self.agent_utility(M - L, rho) + (1 - pi) * self.agent_utility(M, rho))

    def optimize_for_pi(self, pi_value):
        initial_guess_K_gamma = [2, 2]  # Initial guess for K and gamma

        # Define bounds for K and gamma
        bounds = [(0, None), (0, None)]  # K >= 0, gamma >= 0

        # Perform optimization with constraint
        result = optimize.minimize(self.principal_problem, initial_guess_K_gamma, args=(pi_value,),
                                   method='SLSQP', bounds=bounds,
                                   constraints={'type': 'ineq', 'fun': self.constraint, 'args': (pi_value,)},
                                   options={'maxiter': 1000})

        K, gamma = result.x
        return K, gamma, result.success

    def run_optimization(self):
        # Define a range of possible values for pi
        pi_values = np.linspace(0.1, 0.9, 9)  # e.g., 9 values from 0.1 to 0.9

        # Loop over all pi values and store results
        for pi_val in pi_values:
            K, gamma, success = self.optimize_for_pi(pi_val)
            if success:
                self.results.append((pi_val, K, gamma))
            else:
                self.results.append((pi_val, None, None))

        return self.results

    def print_results(self):
        print("Optimal values:")
        for res in self.results:
            pi_val, K, gamma = res
            if K is not None and gamma is not None:
                print(f"For pi = {pi_val:.2f}, K: {K:.2f}, gamma: {gamma:.2f}")
            else:
                print(f"For pi = {pi_val:.2f}, optimization did not converge.")


class further_analysis:
    
    def __init__(self):
        self.results = []
        self.e_values = []
        self.K_values = []
        self.gamma_values = []

    def parameter(self, K, gamma, e):
        M = 50
        L = 5
        rho = 0.3
        pi = 0.1
        pi_s = 0.5

        # Compute consumptions
        c1 = M - gamma
        c2 = M - gamma - L + K

        return M, L, e, rho, c1, c2, pi, pi_s

    def principal_problem(self, x, e):
        K, gamma = x
        M, L, e, rho, c1, c2, pi, pi_s = self.parameter(K, gamma, e)
        return -(M - pi * L - (1 - pi) * c1 - pi * c2)

    def agent_utility(self, c, rho):
        return c**(1 - rho) / (1 - rho)

    def constraint(self, x, e):
        K, gamma = x
        M, L, e, rho, c1, c2, pi, pi_s = self.parameter(K, gamma, e)
        return pi * self.agent_utility(c2, rho) + (1 - pi) * self.agent_utility(c1, rho) - e - (pi * self.agent_utility(M - L, rho) + (1 - pi) * self.agent_utility(M, rho))

    def constraint_ic(self, x, e):
        K, gamma = x
        M, L, e, rho, c1, c2, pi, pi_s = self.parameter(K, gamma, e)
        return (pi_s - pi)*(self.agent_utility(c1, rho)-self.agent_utility(c2, rho)) - e

    def optimize_for_e(self, e_value):
        initial_guess_K_gamma = [2, 2]  # Initial guess for K and gamma

        # Define bounds for K and gamma
        bounds = [(0, None), (0, None)]  # K >= 0, gamma >= 0

        # Perform optimization with constraint
        result = optimize.minimize(self.principal_problem, initial_guess_K_gamma, args=(e_value,),
                                   method='SLSQP', bounds=bounds,
                                   constraints=[{'type': 'ineq', 'fun': self.constraint, 'args': (e_value,)}, {'type': 'ineq', 'fun': self.constraint_ic, 'args': (e_value,)}],
                                   options={'maxiter': 1000})

        K, gamma = result.x
        return K, gamma, result.success

    def run_optimization(self):
        # Define a range of possible values for e
        e_values = np.linspace(0.01, 0.092, 30)  # e.g., 30 values from 0.01 to 0.1

        # Loop over all e values and store results
        for e_val in e_values:
            K, gamma, success = self.optimize_for_e(e_val)
            if success:
                self.results.append((e_val, K, gamma))
                self.e_values.append(e_val)
                self.K_values.append(K)
                self.gamma_values.append(gamma)
            else:
                self.results.append((e_val, None, None))

        return self.results

    def print_results(self):
        print("Optimal values:")
        for res in self.results:
            e_val, K, gamma = res
            if K is not None and gamma is not None:
                print(f"For e = {e_val:.2f}, K: {K:.2f}, gamma: {gamma:.2f}")
            else:
                print(f"For e = {e_val:.2f}, optimization did not converge.")

