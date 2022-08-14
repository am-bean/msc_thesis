from numba import jit
from get_card import getCard


@jit
def roundWinner(arr, lead_seat, round):
  lead_card = getCard(arr, lead_seat, round)
  winning_card = lead_card
  winning_seat = lead_seat
  for player in range(4):
    new_card = getCard(arr, player, round)
    try:
      if (new_card//6) == (winning_card//6):
        if new_card > winning_card:
          winning_card = new_card
          winning_seat = player
      elif (new_card // 6) == 0:
          winning_card = new_card
          winning_seat = player
    except:
      print(arr)
      print(player)
      print(round)
      print(new_card)
      assert False
  return winning_card, winning_seat