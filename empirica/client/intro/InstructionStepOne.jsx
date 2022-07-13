import React from "react";

import { Centered } from "meteor/empirica:core";

export default class InstructionStepOne extends React.Component {
  render() {
    const { hasPrev, hasNext, onNext, onPrev, game } = this.props;

    return (
      <Centered className="with-topper">
        <div className="instructions">
          <h1 className={"bp3-heading"}>Instructions</h1>
          <p>
            In this experiment, you will play an online card game based on the
            game Spades. The game involves two teams of two competing to take as 
            many tricks as possible. You will play the game several times with
            different AI partners. The rules of the game are explained below:
          </p>
          <h3>
            <u>What are playing cards:</u>
          </h3>
          <p>
            This game involves playing cards of four suits (kinds): diamonds, 
            hearts, clubs, and spades. Each card also 
            has a rank (number) which is ordered from low to high: 9, 10, 
            Jack, Queen, King, Ace. There is one copy of each rank for each 
            suit.
          </p>
          <p>
            The cards shown below are the Jack of Diamonds, Queen of
            Hearts, King of Clubs, and Ace of Spades respectively.
          </p>

          <div className="intro-grid">
              <img src="cards/jack_of_diamonds.svg" alt="Jack of Diamonds" />
              <img src="cards/queen_of_hearts.svg" alt="Queen of Hearts" />
              <img src="cards/king_of_clubs.svg" alt="King of Clubs" />
              <img src="cards/ace_of_spades.svg" alt="Ace of Spades" />
          </div>
          
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
          <div><img src="instructions/player_hand.png" alt="Example Hand"/></div>
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
          <div><img src="instructions/partners.png" alt="Example Hand"/></div>
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
          <div><img src="instructions/scoring.png" alt="Example Hand"/></div>

          <h3>
            If at any point you need to review the rules, click "About" in the top corner
          </h3>
          <p className="action-step">
            <button type="button" onClick={onPrev} disabled={!hasPrev}>
              Previous
            </button>
            <button type="button" onClick={onNext} disabled={!hasNext}>
              Next
            </button>
          </p>
        </div>
      </Centered>
    );
  }
}
