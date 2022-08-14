from round_winner import roundWinner
from numba import jit


@jit
def roundLeaders(arr):
  previous_winner = 0
  leaders = [0]
  for round in range(6):
    card, seat = roundWinner(arr, previous_winner, round)
    previous_winner = seat
    leaders.append(seat)
  return leaders[:-1]