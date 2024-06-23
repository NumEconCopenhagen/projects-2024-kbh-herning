import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2024)

X = rng.uniform(size=(50,2))
y = rng.uniform(size=(2,))

####Question1

def find_A(X, y):
    valid_points = X[(X[:, 0] > y[0]) & (X[:, 1] > y[1])]
    if len(valid_points) == 0:
        return np.nan, np.nan
    distances = np.sqrt(np.sum((valid_points-y)**2, axis=1))
    return valid_points[np.argmin(distances)]

def find_B(X, y):
    valid_points = X[(X[:, 0] > y[0]) & (X[:, 1] < y[1])]
    if len(valid_points) == 0:
        return np.nan, np.nan
    distances = np.sqrt(np.sum((valid_points-y)**2, axis=1)) 
    return valid_points[np.argmin(distances)]

def find_C(X, y):
    valid_points = X[(X[:, 0] < y[0]) & (X[:, 1] < y[1])]
    if len(valid_points) == 0:
        return np.nan, np.nan
    distances = np.sqrt(np.sum((valid_points-y)**2, axis=1))
    return valid_points[np.argmin(distances)]

def find_D(X, y):
    valid_points = X[(X[:, 0] < y[0]) & (X[:, 1] > y[1])]
    if len(valid_points) == 0:
        return np.nan, np.nan
    distances = np.sqrt(np.sum((valid_points-y)**2, axis=1))
    return valid_points[np.argmin(distances)]

# Finding points A, B, C, and D
A = find_A(X, y)
B = find_B(X, y)
C = find_C(X, y)
D = find_D(X, y)

def plot_points_and_triangles(X, y, A, B, C, D):
    plt.figure(figsize=(8, 8))
    plt.scatter(X[:, 0], X[:, 1], color='blue', label='Points in X')
    plt.scatter(y[0], y[1], color='red', label='Point y')
    
    if not np.isnan(A[0]):
        plt.scatter(A[0], A[1], color='green', label='Point A')
    if not np.isnan(B[0]):
        plt.scatter(B[0], B[1], color='orange', label='Point B')
    if not np.isnan(C[0]):
        plt.scatter(C[0], C[1], color='purple', label='Point C')
    if not np.isnan(D[0]):
        plt.scatter(D[0], D[1], color='brown', label='Point D')
    
    if not np.isnan(A[0]) and not np.isnan(B[0]) and not np.isnan(C[0]):
        plt.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color='green', label='Triangle ABC')
    if not np.isnan(C[0]) and not np.isnan(D[0]) and not np.isnan(A[0]):
        plt.plot([C[0], D[0], A[0], C[0]], [C[1], D[1], A[1], C[1]], color='orange', label='Triangle CDA')
    
    plt.legend()
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.title('Points and Triangles in the Unit Square')
    plt.grid(True)
    plt.show()

#plot_points_and_triangles(X, y, A, B, C, D)


####Question2

def barycentric_coordinates(A, B, C, y):
    denom = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
    r1 = ((B[1] - C[1]) * (y[0] - C[0]) + (C[0] - B[0]) * (y[1] - C[1])) / denom
    r2 = ((C[1] - A[1]) * (y[0] - C[0]) + (A[0] - C[0]) * (y[1] - C[1])) / denom
    r3 = 1 - r1 - r2
    return r1, r2, r3


def calculate_barycentric_coordinates(A, B, C, D, y):
    results = {}
    r_ABC = r_CDA = None
    if not np.isnan(A[0]) and not np.isnan(B[0]) and not np.isnan(C[0]):
        r_ABC_1, r_ABC_2, r_ABC_3 = barycentric_coordinates(A, B, C, y)
        results['ABC'] = (r_ABC_1, r_ABC_2, r_ABC_3)
        print(f'Barycentric coordinates in triangle ABC: r1 = {r_ABC_1:.4f}, r2 = {r_ABC_2:.4f}, r3 = {r_ABC_3:.4f}')
        r_ABC = (r_ABC_1, r_ABC_2, r_ABC_3)
    if not np.isnan(C[0]) and not np.isnan(D[0]) and not np.isnan(A[0]):
        r_CDA_1, r_CDA_2, r_CDA_3 = barycentric_coordinates(C, D, A, y)
        results['CDA'] = (r_CDA_1, r_CDA_2, r_CDA_3)
        print(f'Barycentric coordinates in triangle CDA: r1 = {r_CDA_1:.4f}, r2 = {r_CDA_2:.4f}, r3 = {r_CDA_3:.4f}')
        r_CDA = (r_CDA_1, r_CDA_2, r_CDA_3)
    return results, r_ABC, r_CDA


####Question3

f = lambda x: x[0]*x[1]
F = np.array([f(x) for x in X])

def approximation(A, B, C, D, r_ABC_1, r_ABC_2, r_ABC_3, r_CDA_1, r_CDA_2, r_CDA_3):
    """**Algorithm:**"""
    """
    1. Compute $A$, $B$, $C$, and $D$. If not possible return `NaN`.
    2. If $y$ is inside the triangle $ABC$ return $r^{ABC}_1 f(A) + r^{ABC}_2 f(B) + r^{ABC}_3 f(C)$.
    3. If $y$ is inside the triangle $CDA$ return $r^{CDA}_1 f(C) + r^{CDA}_2 f(D) + r^{CDA}_3 f(A)$.
    4. Return `NaN`."""
    
    if not np.isnan(A[0]) and not np.isnan(B[0]) and not np.isnan(C[0]) and r_ABC_1 >= 0 and r_ABC_1 <= 1 and r_ABC_2 >= 0 and r_ABC_2 <= 1 and r_ABC_3 >= 0 and r_ABC_3 <= 1:
        return r_ABC_1 * f(A) + r_ABC_2 * f(B) + r_ABC_3 * f(C)
    elif not np.isnan(C[0]) and not np.isnan(D[0]) and not np.isnan(A[0]) and r_CDA_1 >= 0 and r_CDA_2 >= 0 and r_CDA_3 >= 0 and r_CDA_1 <= 1 and r_CDA_2 <= 1 and r_CDA_3 <= 1:
        return r_CDA_1 * f(C) + r_CDA_2 * f(D) + r_CDA_3 * f(A)
    else:
        return np.nan

def run_approximation(A, B, C, D, r_ABC_1, r_ABC_2, r_ABC_3, r_CDA_1, r_CDA_2, r_CDA_3, y):
    approximation_y = approximation(A, B, C, D, r_ABC_1, r_ABC_2, r_ABC_3, r_CDA_1, r_CDA_2, r_CDA_3)
    true_y = f(y)
    print(f'Approximation of f(y): {approximation_y}')
    print(f'True value of f(y): {true_y}')
    return approximation_y, true_y


####Question4

Y = [(0.2,0.2),(0.8,0.2),(0.8,0.8),(0.8,0.2),(0.5,0.5)]


def q3_y1(X, Y):
    results = []

    for i in range(len(Y)):
        A_1 = find_A(X, Y[i])
        B_1 = find_B(X, Y[i])
        C_1 = find_C(X, Y[i])
        D_1 = find_D(X, Y[i])

        if not np.isnan(A_1[0]) and not np.isnan(B_1[0]) and not np.isnan(C_1[0]):
            r_ABC_1, r_ABC_2, r_ABC_3 = barycentric_coordinates(A_1, B_1, C_1, Y[i])

        if not np.isnan(C_1[0]) and not np.isnan(D_1[0]) and not np.isnan(A_1[0]):
            r_CDA_1, r_CDA_2, r_CDA_3 = barycentric_coordinates(C_1, D_1, A_1, Y[i])

        if not np.isnan(A_1[0]) and not np.isnan(B_1[0]) and not np.isnan(C_1[0]) and r_ABC_1 >= 0 and r_ABC_1 <= 1 and r_ABC_2 >= 0 and r_ABC_2 <= 1 and r_ABC_3 >= 0 and r_ABC_3 <= 1:
            approximation_y_1 = r_ABC_1 * f(A_1) + r_ABC_2 * f(B_1) + r_ABC_3 * f(C_1)
            true_y_1 = f(Y[i])
            print(f'Approximation of f(Y[{i}]): {approximation_y_1}')
            print(f'True value of f(Y[{i}]): {true_y_1}')
            results.append(approximation_y_1)
            continue

        elif not np.isnan(C_1[0]) and not np.isnan(D_1[0]) and not np.isnan(A_1[0]) and r_CDA_1 >= 0 and r_CDA_2 >= 0 and r_CDA_3 >= 0 and r_CDA_1 <= 1 and r_CDA_2 <= 1 and r_CDA_3 <= 1:
            approximation_y_1 = r_CDA_1 * f(C_1) + r_CDA_2 * f(D_1) + r_CDA_3 * f(A_1)
            true_y_1 = f(Y[i])
            print(f'Approximation of f(Y[{i}]): {approximation_y_1}')
            print(f'True value of f(Y[{i}]): {true_y_1}')
            results.append(approximation_y_1)
            continue

        else:
            true_y_1 = f(Y[i])
            print(f'No valid triangle found for Y[{i}].')
            print(f'True value of f(Y[{i}]): {true_y_1}')

    return results if results else np.nan