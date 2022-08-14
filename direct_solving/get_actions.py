from round_leaders import roundLeaders
from get_card import getCard

from numba import jit
import numpy as np


@jit
def getActions(obs, hands, seat):
  hand = hands[seat,:]
  round = 6 - len(np.nonzero(hand)[0])
  leaders = roundLeaders(obs)
  if round == 6:
    empty = [0]
    empty.remove(0)
    print('round 6')
    return np.array(empty)
  lead = leaders[round]
  if seat == lead:
    return np.nonzero(hand)[0]
  else:
    lead_card = getCard(obs, lead, round)
    handCards = np.nonzero(hand)[0]
    same_suit = handCards[(handCards//6) == (lead_card//6)]
    if same_suit.sum() > 0:
      return same_suit
    else:
      return np.nonzero(hand)[0]
