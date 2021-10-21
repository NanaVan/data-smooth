#!/usr/bin/env python3
# −*− coding:utf-8 −*−

import numpy as np
import sys
import scipy.special as sp
from scipy import sparse
from scipy.sparse.linalg import spsolve

def interpolation(v, u):
    '''
    interpolate points into an array base on the mean of interval of x-coordiante
    used for the situation:
    the interval of x-coordinate is not equal, especially wide scale range of x-coordinate.
    ---
    v:      array of x coordinate
    u:      array of y coordinate corresponding to v
    ---
    v_complete: array of interpolated x coordinate
    u_complete: array of interpolated y coordinate
    weight:     array help to distinguish original data points and interpolated points, 1.0 for original data points while 0.0 for interpolated points 
    '''
    v_complete, u_complete, weight = np.array([v[0]]), np.array([u[0]]), np.array([1.])
    v_diff = np.diff(v)
    v_diff_mean = np.mean(np.unique(v_diff))
    for i in range(len(v_diff)):
        if v_diff[i] > v_diff_mean:
            weight = np.concatenate((weight, np.zeros(int(v_diff[i]//v_diff_mean))))
            v_complete = np.concatenate((v_complete, v_complete[-1] + np.arange(1, v_diff[i]//v_diff_mean+1) * v_diff_mean))
            u_complete = np.concatenate((u_complete, u_complete[-1] * np.ones(int(v_diff[i]//v_diff_mean))))
        weight = np.concatenate((weight, np.array([1.])))
        v_complete = np.concatenate((v_complete, np.array([v[i+1]])))
        u_complete = np.concatenate((u_complete, np.array([u[i+1]])))
    return v_complete, u_complete, weight

def diff_sparse(v, n=1):
    '''
    caculate n-th discrete difference of sparse matrix
    ---
    v:      sparse matrix, (L, L)
    n:      number of times values are differences, default 1
    ---
    return  n-th differences, (L, L-n)
    '''
    while n > 0:
        v = v.tocsr()[:,1:] - v.tocsr()[:,:-1]
        n -= 1
    return v


class SIGSMOOTH():
    '''
    implement the signal smooth
    '''
    def __init__(self, data):
        self.data = data

    def PLS_expect(self, l, w, n=2):
        '''
        penalized least squares (PLS) expect mode
        @ E. T. Whittaker, Proc. Edinburgh Math. Soc., 41(1923), 63-75.
        @ P. H. C. Eilers, Anal. Chem. 75(2003), 3631-3636.
        ---
        l:          parameter for smoothness
        w:          weight array of data
        n:          order for smoothness, default 2
        ---
        return
        z:          smoothed line
        '''
        L = len(self.data)
        if len(w) != L:
            raise ValueError("Invalid length of weight array! The length must be same as data.")
            sys.exit()
        D = diff_sparse(sparse.eye(L), n)
        D = l * D.dot(D.transpose())
        W = sparse.spdiags(w, 0, L, L)
        Z = W + D
        z = spsolve(Z, w*self.data)
        return z

    def PLS_interpolation(self, x, l, n=2):
        '''
        penalized least squares (PLS) interpolation mode
        used for interval of x-coordinate is not equal
        ---
        x:          array of x-coordinate corresponding to data
        l:          parameter for smoothness
        n:          order for smoothness, default 2
        ---
        return
        z:          smoothed line
        '''
        _, y_modified, w = interpolation(x, self.data)
        L = len(y_modified)
        D = diff_sparse(sparse.eye(L), n)
        D = l * D.dot(D.transpose())
        W = sparse.spdiags(w, 0, L, L)
        Z = W + D
        z = spsolve(Z, w*y_modified) * w
        z = z[z!=0]
        return z 
