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

    const { player, round,stage } = this.props;
    if (!player.stage.submitted){
      stage.set(`played-${player.get("seat")}`, cardDetails);
      round.set(`played-${player.get("seat")}`, cardDetails);
      let hand = player.round.get("hand").filter((item) => {return item !== cardDetails;});
      player.round.set("hand", hand);

      WarningToaster.show({ message: "You chose the " + cardDetails['rank'] + " of " + cardDetails['suit']});
      player.stage.submit();
    }
    return;
  };

  handleNext = (event) => {
    event.preventDefault();

    const { player, stage } = this.props;
    player.stage.submit();
    return;

  };

  renderResult() {
    const { player, round, stage } = this.props;
    const task = round.get("task");

    const correct_answer = task.correct_answer === "Yes" ? 1 : 0;
    if (stage.get("type") === "feedback") {
      return (
        <div className="result">
          {correct_answer === 1 ? (
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
              <div className="result-entry label">Winning Player</div>
              <div className="result-entry value">
                {player.round.get("prediction") !== null
                  ? round.get("winner")
                  : player.round.get("name")}
              </div>
            </div>
            <div className="result-item last-item">
              <div className="result-entry label">Cumulative Score</div>
              <div className="result-entry value">
                {player.round.get("score") || null}
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
    return null;
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


  render() {
    const { player, stage } = this.props;
        

    const isOutcome =
      stage.name === "outcome" || stage.name === "practice-outcome";
    
    return (
      <div className="response">
        {this.renderResult()}
        {!isOutcome && (
          <h3>
            Please choose the card from your hand which you would like to play.
          </h3>
        )}
        {!isOutcome && (  
          <div className="cards-in-hand">
            {this.renderHand(player.round.get("hand"), false)}
          </div>
        )}
      </div>
    );
  }
}
