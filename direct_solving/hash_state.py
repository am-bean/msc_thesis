from numba import jit


@jit
def hashState(obs, hands):
  stringa = ''
  stringb = ''
  for i in obs.flatten():
    stringa += str(int(i))
  for i in hands.flatten():
    stringb += str(int(i))
  return stringa+stringb