import numpy as np


def construct_stim_matrices(m, prenumlag=0, postnumlag=0, wantwrap=0):
    """construc stimulus matrices from design matrix m

    Args:

        m ([2d matrix]): is a 2D matrix, each row of which is a stimulus
            sequence (i.e. a vector that is all zeros except for ones
            indicating the onset of a given stimulus (fractional values
            are also okay))

        prenumlag (bool or int, optional): Defaults to False. number of
            stimulus points in the past

        postnumlag (bool or int, optional): Defaults to False. number of
            stimulus points in the future

        wantwrap (bool, optional): Defaults to False. whether to wrap
            around
    Returns:
        [2d matrix]: a stimulus matrix of dimensions
            size(m,2) x ((prenumlag+postnumlag+1)*size(m,1)).
            this is a horizontal concatenation of the stimulus
            matrix for the first stimulus sequence, the stimulus
            matrix for the second stimulus sequence, and so on.
            this function is useful for fitting finite impulse
            response (FIR) models.
    """

    # make sure m is numpy
    m = np.asarray(m)

    # get out early
    if prenumlag or postnumlag:
        nconds, nvols = m.shape

        # do it
        num = prenumlag + postnumlag + 1
        f = np.zeros((nvols, num*nconds))
        for p in range(nconds):
            i = p + 1
            thiscol = (i - 1) * num + np.array(range(num))
            f[:, thiscol] = construct_stim_matrix(
                m[p, :], prenumlag, postnumlag, wantwrap
            )

    else:
        f = m.T
        return f
    return f


def construct_stim_matrix(v, prenumlag, postnumlag, wantwrap=0):
    """Construct stimulus matrix from design vector

    Args:

        v ([1d vector]): v is the stimulus sequence represented as a vector

        prenumlag ([int]): this is the number of stimulus points in the past

        postnumlag ([int]): this is the number of stimulus points in the future

        wantwrap (int, optional): Defaults to 0. whether to wrap around


    Returns:
        [2d array]: return a stimulus matrix of dimensions
            length(v) x (prenumlag+postnumlag+1)
            where each column represents the stimulus at
            a particular time lag.
    """
    v = np.asarray(v)
    total = prenumlag + postnumlag + 1
    f = np.zeros((len(v), total))
    for p in range(total):
        i = p + 1
        temp = -prenumlag + (i - 1)
        if temp >= 0:
            f[temp:, p] = v[: len(v) - temp]
    return f
