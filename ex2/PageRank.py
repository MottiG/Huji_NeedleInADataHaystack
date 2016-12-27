import numpy as np
np.set_printoptions(precision=5)


def rank(mat, beta, S):

    print('Initial M:\n', mat)

    n = mat.shape[0]
    if beta != 1:  # in case of teleports
        temp = np.zeros(mat.shape)
        temp[S, :] = 1/S.shape[0]
        mat = beta * mat + (1 - beta) * temp
        print('Normalized M:\n', mat)

    r = np.ones((n, 1)) / n  # initial r to with 1/N
    print('Inital r:', r.T)

    close_enough = False
    while not close_enough:
        new_r = mat.dot(r)
        close_enough = np.linalg.norm(new_r - r) < e
        r = new_r

    print('Final r:', r.T)


if __name__ == '__main__':

    e = 0.01  # epsilon
    b = 0.85  # beta
    s = np.array([2])  # set of pages to teleport, where pages start from 0
    M = np.array([[1, 1, 0],
                  [1, 0, 1],
                  [1, 1, 1]])
    M = M / M.sum(axis=0)

    rank(M, b, s)