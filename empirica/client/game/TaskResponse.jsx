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
  handleSubmit = (event, cardDetails) => {
    event.preventDefault();
    
    const { player, round, stage } = this.props;
    const playersTurn =  ((player.get("seat") === round.get("winner")) || (round.get(`submitted-${player.get("follows")}`)))
    console.log(round.get(`submitted-${player.get("follows")}`))
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
      round.set(`submitted-${player.get("seat")}`, true);
      return;
    }
  };

  handleNext = (event) => {
    event.preventDefault();
    const { player, stage } = this.props;
    player.stage.submit();
    round.set(`submitted-${player.get("seat")}`, true);
    return;

  };

  renderResult() {
    const { player, round, stage } = this.props;
    const winner = ((round.get("winner") === player.get("seat")) || (round.get("winner") === player.get("partner")));

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
              {round.get("lead")}
            </div>
          </div>
          <div className="result-item">
            <div className="result-entry label">Winning Player</div>
            <div className="result-entry value">
              {round.get("winner")}
            </div>
          </div>
          <div className="result-item last-item">
            <div className="result-entry label">Cumulative Score</div>
            <div className="result-entry value">
              {player.round.get("score")}
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
        <h3>
          Please choose the card from your hand which you would like to play.
        </h3>
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
    } else {
      return(
        <div className="response">
          {this.renderPrompt()}
        </div>
      )
    }
  }
}
