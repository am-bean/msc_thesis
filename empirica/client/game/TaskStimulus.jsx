import React from "react";

const PlayingCard = ({ cardDetails }) => {
  return (
    <div className="card-thumb">
        <strong> {cardDetails["seat"]} </strong>
        <img
            src={`/cards/${cardDetails["rank"]}_of_${cardDetails["suit"]}.svg`}
            alt={`2_of_clubs`}
          />
    </div>
  );
};


export default class TaskStimulus extends React.Component {
  state = { interestValue: 0.08 };

  render() {
    const { stage, round } = this.props;
    const task = round.get("task") || {};
    const pairData = task.features || {};
    const dummyCard = {rank: 'jack', suit: "clubs", seat: "North"}
    const dummyCard2 = {rank: 'ace', suit: "clubs", seat: "East"}
    const dummyHand = [dummyCard, dummyCard2]

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
          {dummyHand.map((val, i) => <PlayingCard cardDetails={val} key={i}/>)}
        </div>
      </div>
    );
  }
}
