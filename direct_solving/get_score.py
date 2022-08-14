from round_winner import roundWinner
import numpy as np
from numba import jit


@jit
def getScore(obs, hands, targetSeat):
  previous_winner = 0
  winners = [0]
  for round in range(6):
    card, winner = roundWinner(obs, previous_winner, round)
    previous_winner = winner
    winners.append(winner)
  winners = winners[1:]
  score = sum((np.array(winners)%2) == (targetSeat%2))
  return score