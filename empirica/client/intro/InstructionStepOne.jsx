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
            Hearts, King of Clubs, and Ace of Spades respectively. They can be identified 
            by the markings in the corner of the cards as well as the images
            in the center.
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
          <p>
            Each of four players is randomly dealt (given) six cards, one quarter of the deck, to be
            their hand. These cards are theirs to use, and are secret from the other
            players. Partners are `seated` opposite each other, with seats often labelled 
            using compass directions, so that North/South and East/West are the partnerships.
          </p>
          <p>
            Play proceeds in `tricks`, a round of the table in which each player
            plays one card from their hand. To start the game, East will go first. The 
            first player in a trick may play any card in their hand to `lead` the trick. 
            After this, other players take turns proceeding clockwise e.g. (East, 
            South, West, North). When possible, new cards played must be the same suit as the 
            first card `led` in the trick. If a player cannot play a card of the same
            suit, they may play any card in their hand. Once each player has played a card,
            one player wins the trick, scoring a point, and the played cards are discarded. 
            The winner gets to lead the next trick using the remaining cards in their hand.
          </p>
          <p>
            The winner of a trick is the person who played the highest card matching the 
            suit which was led. However, there is one exception. If a spade card has been 
            played, it `trumps` any other suit, and always wins. If more than one spade was
            played, the highest one wins.
          </p>

          <h3>
            <u>Scoring:</u>
          </h3>
          <p>
            At the end of the game, each partnership scores one point per trick taken. This 
            will be between 0-6 tricks. Over several games, the team with the most cumulative
            points wins. Since you and your partner share the same score, it is important to 
            consider how your actions influence each other.
          </p>

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
