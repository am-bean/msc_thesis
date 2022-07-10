import React from "react";

const PlayingCard = ({ cardDetails, seat, player }) => {
  
  const isNull = cardDetails === null
  const self = player.get("seat") === seat ? "(You)" : ""
  const partner = player.get("partner") === seat ? "(Partner)" : ""
  return (
    <div className="card-thumb">
        <strong> {seat} {self} {partner} </strong>
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
        {stage.get("type") === "outcome" ?       
          (<h3>
            These are all the cards played in the past round:
          </h3>) : ( stage.get("type") === "play" ?

          (<div>
          <h3>
            The leader this round is: {round.get("winner")} {round.get("winner") === player.get("self") ? "(You)" : ""} {round.get("winner") === player.get("partner") ? "(Partner)" : ""} 
          </h3>
          <h3>
          The following cards have already been played this round:
          </h3>
          </div>) : 
          
          (<div>
            <h3>
              The winners of this game are:
            </h3>
            </div>)
          )
        }
        <div className="cards">
          {displayOrder.map((seat) => 
          <PlayingCard cardDetails={stage.get(`played-${seat}`)} key={seat} seat={seat} player={player}/>
            )
            }
        </div>
      </div>
    ));
  }
}
