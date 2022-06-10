import React from "react";

const PlayingCard = ({ cardDetails, seat }) => {
  
  const isNull = cardDetails === null
  return (
    <div className="card-thumb">
        <strong> {seat} </strong>
        {!isNull && (  
          <img
          src={`/cards/${cardDetails["rank"]}_of_${cardDetails["suit"]}.svg`}
          alt={`2_of_clubs`}
        />
        )}
    </div>
  );
};


export default class TaskStimulus extends React.Component {
  state = { interestValue: 0.08 };

  render() {
    const {game, player, stage, round } = this.props;
    const task = round.get("task") || {};
    const pairData = task.features || {};

    return (
      <div className="cards-table">
        {stage.get("type") === "feedback" ?       
          (<h3>
            These are all the cards played in the past round:
          </h3>) :

          (<h3>
            The following cards have already been played this round:
          </h3>) 
        }
        <h3>
          You are playing as South, with North as your partner.
        </h3>
        <div className="cards">
          {game.players.map((plyr) => <PlayingCard cardDetails={stage.get(`played-${plyr.get("seat")}`)} key={plyr.get("seat")} seat={plyr.get("seat")}/>)}
        </div>
      </div>
    );
  }
}
