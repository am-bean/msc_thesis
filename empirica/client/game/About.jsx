import React from "react";

export default class About extends React.Component {
  render() {
    return <div>
    <h3>
    <u>How to play:</u>
  </h3>
  <ul>
  <li>
    You will be randomly dealt (given) six cards for your hand.
    These cards are yours to use, and are secret from the other
    players.
  </li>
  </ul>
  <div><img src="instructions/player_hand.png" alt="Example Hand" class="center"/></div>
  <ul>
  <li>
    Your partner is seated opposite from you, and the seats are labelled 
    using compass directions, so that North/South and East/West are the partnerships.
  </li>
  <br/>
  <li>
    To start the game, East will go first. East will play any card from their hand to 'lead'.
  </li>
  <br/>
  <li>
    The other players then take turns proceeding clockwise e.g. (East, 
    South, West, North) playing a card. When possible, you must play 
    the same suit as the first card `led` in the trick. 
  </li>
  <br/>
  <li> 
    If you cannot play a card of the same suit, you may play any card in your hand.
  </li>
  </ul>
  <div><img src="instructions/partners.png" alt="Example Hand" class="center"/></div>
  <h3>
    <u>Scoring:</u>
  </h3>
  <ul>
  <li>
    Once everyone has played a card, the highest card played wins and scores a point. 
  </li>
  <br/>
  <li>
    Only cards which match the original suit which was led can be counted for the highest card. 
  </li>
  <br/>
  <li> 
    EXCEPT, if you play a spade card, it `trumps` any other suit, and always wins. (If more than one spade was
    played, the highest one wins.)
  </li>
  <br/>
  <li>
    The winner gets to lead the next trick using the remaining cards in their hand.
  </li>
  </ul>
  <div><img src="instructions/scoring.png" alt="Example Hand" class="center"/></div>
  </div>
  }
}