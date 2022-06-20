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
    const seats = ["North", "East", "South", "West"]
    let index = seats.findIndex( element => {
      if ((element === round.get("lead")) && (stage.get("type") === "outcome")) {
        return true;
      }
      if ((element === round.get("winner")) && (stage.get("type") === "play")) {
        return true;
      }
    });
    let displayOrder = []
    seats.forEach((s,i) => displayOrder[(i - index + 4) % 4] = s)

    return (
      <div className="cards-table">
        {stage.get("type") === "outcome" ?       
          (<h3>
            These are all the cards played in the past round:
          </h3>) :

          (<h3>
            {round.get("winner")} has the lead in this. The following cards have already been played this round:
          </h3>) 
        }
        <h3>
          You are playing as {player.get("seat")}, with {player.get("partner")} as your partner.
        </h3>
        <div className="cards">
          {displayOrder.map((seat) => 
          <PlayingCard cardDetails={stage.get(`played-${seat}`)} key={seat} seat={seat}/>
            )}
        </div>
      </div>
    );
  }
}
