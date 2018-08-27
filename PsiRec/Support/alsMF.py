import copy
import numpy as np
import evaluation

def cp_als_completion(X, r=100, maxiter=25, Freg_para=0.25, validation=0):
    """ CP_ALS Compute a CP decomposition of a Tensor (and recover it).
    ---------
     :param  'X' - Matrix with Missing data
     :param  'r' - Rank of the tensor
     :param 'maxiters' - Maximum number of iterations
    ---------
     :return
        'X' - Recovered Matrix.
    ---------
    """

    data = copy.copy(X)
    num_rows = X.shape[0]
    num_cols = X.shape[1]

    # Set up and error checking on initial guess for U.
    U = range(2)
    U[0] = []
    U[1] = np.random.random([num_cols, r])
    # Set up for iterations - initializing U and the fit.
    print('\nMC_ALS:')

    # Save hadamard product of each U[n].T*U[n]
    UtU = np.zeros([2, r, r])
    UtU[1, :, :] = np.dot(U[1].T, U[1])

    for iter in range(1, maxiter + 1):
        for n in range(2):
            tempU = U[-1 * (n - 1)]
            if n == 0:
                Unew = X.dot(tempU)
            else:
                Unew = (X.T).dot(tempU)
            y = Freg_para * np.eye(tempU.shape[1]) + UtU[-1 * (n - 1), :, :]
            Unew = Unew.dot(np.linalg.inv(y))
            U[n] = Unew
            UtU[n, :, :] = np.dot(U[n].T, U[n])

        P = np.dot(U[0], U[1].T)

        if iter % 5 == 0:
            print 'als matrix factorization iteration times: ', iter
        if validation:
            if iter%5==0 and iter!=0 and iter>=25:
                print 'vailidation results in the iteration: ', iter
                evaluation.test_model_all(P)

    return P


def MF(train_R, args):
    Rec = cp_als_completion(train_R, r=args.latent_factors, maxiter=args.train_epoch,
                                Freg_para=args.lambda_value, validation=args.validation)
    return Rec