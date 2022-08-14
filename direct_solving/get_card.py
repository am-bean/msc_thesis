from numba import jit
import numpy as np


@jit
def getCard(arr, seat, round):
  return np.nonzero(arr[seat*6 + round + 1,:])[0]
