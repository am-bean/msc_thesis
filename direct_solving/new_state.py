from numba import jit
import numpy as np

from round_winner import roundWinner

@jit
def newState(obs, hands, action, seat):
  round = 6 - len(np.nonzero(hands[seat,:])[0])
  new_obs = obs.copy()
  new_obs[seat*6 + round + 1][int(action)] = 1
  new_hands = hands.copy()
  new_hands[seat, int(action)] = 0
  cards_this_round = 0
  for i in range(4):
    card = np.nonzero(new_obs[i*6 + round + 1,:])[0]
    cards_this_round = cards_this_round + len(card)
    if cards_this_round == 4:
      _, new_seat = roundWinner(new_obs, (seat+1)%4, round)
    else:
      new_seat = (seat+1)%4
  try:
    assert(new_obs.sum(axis=1).max() <= 1)
    assert(new_obs.sum(axis=1).min() >= 0)
    assert(new_hands.sum() + 1 == hands.sum())
  except:
    print('newState failure')
    print('obs:')
    print(obs)
    print('action')
    print(action)
    print('seat:')
    print(seat)
    print('round:')
    print(round)
    print('hand:')
    print(hands[seat,:])
    print('new_hand')
    print(new_hands[seat,:])
    print('new_obs:')
    print(new_obs)
    assert False
  return new_obs, new_hands, new_seat