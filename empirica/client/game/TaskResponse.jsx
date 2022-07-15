import { Position, Toaster } from "@blueprintjs/core";
import React from "react";

const WarningToaster = Toaster.create({
  className: "warning-toaster",
  position: Position.TOP,
});

//timed button
const TimedButton = (props) => {
  const { onClick, remainingSeconds, stage, cardDetails, disabled} = props;

  return (
    <input type="image" 
    className="card-button"
    id='buttonname'
    src={`/cards/${cardDetails["rank"]}_of_${cardDetails["suit"]}.svg`}
    alt={`${cardDetails["rank"]} of ${cardDetails["suit"]}`}
    onClick={evt => {onClick(evt, cardDetails)}}
    disabled={disabled}
    >

    </input>
    );
};


export default class TaskResponse extends React.Component {

  encodeCard(card) {
    const suitValues = {spades: 0, clubs: 1, diamonds: 2, hearts: 3};
    const rankValues = {9: 0, 10: 1, jack: 2, queen: 3, king: 4, ace: 5};
    return suitValues[card['suit']]*6 + rankValues[card['rank']];
  }

  getName = (seat, game) => {
    const name = game.players.filter((p) => p.get("seat") == seat)[0].get("name")
    return name
  }

  handleSubmit = (event, cardDetails) => {
    event.preventDefault();
    
    const { player, round, stage } = this.props;
    const playersTurn =  ((player.get("seat") === round.get("winner")) || (round.get(`submitted-${player.get("follows")}`)))

    if (!playersTurn){
      WarningToaster.show({ message: "Currently waiting on the bots to play"});
      return;
    }
    if (player.stage.submitted){
      WarningToaster.show({ message: "Currently waiting on the bots to play"});
      return;
    }
    if (playersTurn && (player.get("seat") !== round.get("winner"))){
      const leadSuit = stage.get(`played-${round.get("winner")}`)['suit']
      const hasSuit = player.round.get("hand").some((item) => {return item['suit'] === leadSuit;})
      const followedSuit = cardDetails['suit'] == leadSuit
      if (hasSuit && !followedSuit){
        WarningToaster.show({ message: "You must follow suit when possible."});
        return;
      }
    }
    if (playersTurn && (!player.stage.submitted)){
      stage.set(`played-${player.get("seat")}`, cardDetails);
      round.set(`played-${player.get("seat")}`, cardDetails);
      let hand = player.round.get("hand").filter((item) => {return item !== cardDetails;});
      player.round.set("hand", hand);
      player.stage.submit();
      
      const agent_mapping = {East: 0, South: 1, West: 2, North: 3}
      let stageIndex = round.get('current-stage');
      const cumObs = round.get('cumulative-obs')
      console.log(`Human play: ${cardDetails}`)
      if (cardDetails) {
        let obsIndex = agent_mapping[player.get("seat")]*6*24 + this.encodeCard(cardDetails) + (stageIndex)*24;
        console.log(obsIndex)
        if (!isNaN(obsIndex)) {cumObs[obsIndex] = 1;}
      }
      
      round.set('cumulative-obs', cumObs);
      round.set(`submitted-${player.get("seat")}`, true);
      return;
    }
  };

  handleNext = (event) => {
    event.preventDefault();
    const { player, stage, round } = this.props;
    round.set(`submitted-${player.get("seat")}`, true);
    player.stage.submit();
    return;

  };

  renderResult() {
    const { game, player, round, stage } = this.props;
    const winner = ((round.get("winner") === player.get("seat")) || (round.get("winner") === player.get("partner")));
    const opponent = game.players.filter((p) => {return p.get("seat") === player.get("follows");})[0]

    

    return (
      <div className="result">
        {winner ? (
          <div className="alert alert-error">
            <div className="alert-content">
              <strong>Outcome</strong> Your team won the trick
            </div>
          </div>
        ) : (
          <div className="alert">
            <div className="alert-content">
              <strong>Outcome</strong> The opposing team won the trick
            </div>
          </div>
        )}
        <div className="result-score">
        <div className="result-item">
            <div className="result-entry label">Played Lead</div>
            <div className="result-entry value">
              {this.getName(round.get("lead"), game)} {round.get("lead") === player.get("seat") ? "(You)" : ""} {round.get("lead") === player.get("partner") ? "(Partner)" : ""} 
            </div>
          </div>
          <div className="result-item">
            <div className="result-entry label">Winning Player</div>
            <div className="result-entry value">
              {this.getName(round.get("winner"),game)} {round.get("winner") === player.get("seat") ? "(You)" : ""} {round.get("winner") === player.get("partner") ? "(Partner)" : ""} 
            </div>
          </div>
          <div className="result-item last-item">
            <div className="result-entry label">Cumulative Score</div>
            <div className="result-entry value">
              {player.round.get("score")} - {opponent.round.get("score")}
            </div>
          </div>
        </div>
        <div className="next-button-box">
        <input type="button" 
              className="next-button" 
              onClick={this.handleNext}
              value="Next"
        ></input>
        </div>
      </div>
    );
  }

  renderGameResult() {
    const { game, player, round, stage } = this.props;
    const opponent = game.players.filter((p) => {return p.get("seat") === player.get("follows");})[0]
    const winner = player.round.get("score") > opponent.round.get("score") ;
    const tie = player.round.get("score") === opponent.round.get("score");

    return (
      <div className="result">
        {winner ? (
          <div className="alert alert-error">
            <div className="alert-content">
              <strong>Outcome</strong> Your team won the game!
            </div>
          </div>
        ) : tie ? (
          <div className="alert alert-neutral">
            <div className="alert-content">
              <strong>Outcome</strong> The game resulted in a tie.
            </div>
          </div>
        ) : (
          <div className="alert">
            <div className="alert-content">
              <strong>Outcome</strong> Your team was defeated!
            </div>
          </div>
        )}
        <div className="result-final-score">
          <div className="result-final-item">
            <div className="result-final-entry label">Cumulative Score</div>
            <div className="result-final-entry value">
              {player.round.get("score")} - {opponent.round.get("score")}
            </div>
          </div>
        </div>
        <div className="next-button-box">
        <input type="button" 
              className="next-button" 
              onClick={this.handleNext}
              value="Start Next Game"
        ></input>
        </div>
      </div>
    );
  }


  renderHand = (playerHand, isDisabled) => {
    const { player, stage } = this.props;
    return(
      playerHand.map((val, i) => <TimedButton
        stage={stage}
        player={player}
        onClick={this.handleSubmit}
        cardDetails = {val}
        key={i}
        disabled={isDisabled}
      />)
    );
  };

  renderPrompt() {
    const {player} = this.props
    return(
      <div>
        <h2>
          Click on the card which you would like to play.
        </h2>
        <div className="cards-in-hand">
          {this.renderHand(player.round.get("hand"), false)}
        </div>
      </div>
    )
  }


  render() {
    const { player, stage } = this.props;
    if (stage.get("type") === "outcome"){
      return (
        <div className="response">
          {this.renderResult()}
        </div>
      );
    } else if (stage.get("type") === "play") {
      return(
        <div className="response">
          {this.renderPrompt()}
        </div>
      );
    } else {
      return (
      <div className="response">
        {this.renderGameResult()}
      </div>
      )
    } 
  }
}
