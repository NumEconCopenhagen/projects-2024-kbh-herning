from scipy import optimize
import sympy as sm

def define_symbols():
    # defining the symbols of the pricipal-agent model
    L = sm.symbols('L')
    M = sm.symbols('M')
    pi = sm.symbols('pi')
    L = sm.symbols('L')
    c_1 = sm.symbols('c_1')
    c_2 = sm.symbols('c_2')
    lam = sm.symbols('lambda')
    v_overline = sm.symbols(r'\overline{v}')
    v = sm.Function('v')
    return L, M, pi, L, c_1, c_2, lam, v_overline, v

def calculate_derivatives(c_1, c_2, v, M, pi, L, v_overline, lam):
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

def solve_ss(alpha, c):
    """ Example function. Solve for steady state k. 

    Args:
        c (float): costs
        alpha (float): parameter

    Returns:
        result (RootResults): the solution represented as a RootResults object.

    """ 
    
    # a. Objective function, depends on k (endogenous) and c (exogenous).
    f = lambda k: k**alpha - c
    obj = lambda kss: kss - f(kss)

    #. b. call root finder to find kss.
    result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
    
    return result