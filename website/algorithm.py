import numpy as np
import math
from scipy.optimize import LinearConstraint, milp, Bounds
from scipy.sparse import coo_array

def algo(ranks, nstud, ngroup):
    # nstud = 9
    # nrank = 3
    # ngroup = 3
    # gsize = 3
    min_g_size = nstud//ngroup
    max_g_size = math.ceil(nstud/ngroup)

    # these arrays are used again as parameters later
    arange = np.arange(ngroup * nstud)
    ones = np.ones(ngroup * nstud, dtype=np.uint8)
    bounds = Bounds(np.zeros_like(ranks), ones)

    # create constraint for student in one group
    A_i = np.repeat(np.arange(nstud), ngroup)
    A = coo_array((ones, (A_i, arange)))
    lb_ub = np.full(nstud, 1)
    students_in_one_group = LinearConstraint(A, lb_ub, lb_ub)

    # create constraint for group size
    A_i = np.tile(np.arange(ngroup), nstud)
    A = coo_array((ones, (A_i, arange)))
    lb = np.full(ngroup, min_g_size)
    ub = np.full(ngroup, max_g_size)
    group_size = LinearConstraint(A, lb, ub)

    # group_size
    constraints = {students_in_one_group, group_size}

    result = milp(ranks, bounds=bounds, integrality=ones, constraints=constraints)

    # print(A.dot(result.x))
    print(result)
    #print(result.x.reshape(nstud, ngroup))
    #print(ranks.reshape(nstud, ngroup))
    return result.x.reshape(nstud, ngroup)

if __name__ == '__main__':
    nstud = 21
    # nrank = 3
    ngroup = 5

    # ranks: C
    ranks = np.zeros((nstud * ngroup))
    # Generate a permutation of integers from 1-5 for each row
    for i in range(nstud):
        ranks[i*ngroup:i*ngroup+ngroup] = np.random.permutation(ngroup)
    
    print(algo(ranks, nstud, ngroup))

# import numpy as np
# from scipy.optimize import differential_evolution, LinearConstraint
# from scipy.sparse import coo_array

# nstud = 9
# nrank = 3
# ngroup = 3
# gsize = 3

# ranks = np.zeros((nstud * nrank), dtype=np.uint8)
# # Generate a permutation of integers from 1-5 for each row
# for i in range(nstud):
#     ranks[i*nrank:i*nrank+nrank] = np.random.permutation(nrank)

# #optimization function
# def match_score(groups):
#     return -groups.dot(ranks)

# bounds = [(0,1) for _ in range(nstud * ngroup)]

# # these arrays are used again as parameters later
# full = np.full((nstud * ngroup), 1)
# arange = np.arange(ngroup * nstud)

# # create constraint for student in one group
# A_i = np.repeat(np.arange(nstud), ngroup)
# A = coo_array((full, (A_i, arange)))
# lb_ub = np.full(nstud, 1)
# students_in_one_group = LinearConstraint(A, lb_ub, lb_ub)

# # create constraint for group size
# A_i = np.tile(np.arange(ngroup), nstud)
# A = coo_array((full, (A_i, arange)))
# lb_ub = np.full(ngroup, gsize)
# group_size = LinearConstraint(A, lb_ub, lb_ub)

# # group_size
# constraints = {students_in_one_group, group_size}

# result = differential_evolution(match_score, bounds, integrality=full, constraints=constraints)

# # print(A.dot(result.x))
# print(result)
# print(result.x.reshape(nstud, ngroup))
# print(ranks.reshape(nstud, ngroup))
