import React from "react";

const PlayingCard = ({ cardDetails, seat, player, round }) => {
  
  const isNull = cardDetails === null
  const self = player.get("seat") === seat ? "(You)" : ""
  const partner = player.get("partner") === seat ? "(Partner)" : ""
  const isLeader = round.get("winner") === seat
  const cssSeat = (player.get("seat") === seat) ? "self" : (player.get("partner") === seat) ? "partner" : (player.get("follows") === seat) ? "after" : "before"
  const cssClass = "card-thumb " +  cssSeat
  return (
    <div className={cssClass}>
        
        <strong className="card-label"> {seat} {self} {partner} </strong>
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

    return (stage.get("type") === "round_outcome" ? (<br/>) : (
      <div className="cards-table">
        <div className="cards">
          {displayOrder.map((seat) => 
          <PlayingCard cardDetails={stage.get(`played-${seat}`)} key={seat} seat={seat} player={player} round={round}/>
            )
            }
          <div className="leader"><strong>{(stage.get("type") === "play") ? "Lead: " : "Winner: "} {round.get("winner")}</strong></div>
        </div>
      </div>
    ));
  }
}
