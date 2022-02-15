
import numpy as np
from glmsingle.utils.choose import choose as ch
from glmsingle.utils.isrowvector import isrowvector as isr


def normalisemax(m, dim=None):
    """Divide array by the max value along some dimension

    f = normalisemax(m,dim)

    <m> is a matrix
    <dim> (optional) is the dimension of <m> to operate upon.
    default to 1 if <m> is a row vector and to 0 otherwise.
    special case is 'global' which means operate globally.

    divide <m> by the max value along some dimension (or globally).

    example:
    (normalisemax([[1, 2, 3]])==[[1/3, 2/3, 1]]).all()
    """

    # input
    if dim is None:
        dim = ch(isr(m), 1, 0)
    if dim == 'global':
        return m / np.max(m)
    all_max = np.max(m, dim)
    return np.stack(
            [m[:, i] / thismax for i, thismax in enumerate(all_max)]
            ).T
