import React from "react";

import Timer from "./Timer.jsx";

export default class PlayerProfile extends React.Component {
  render() {
    const { game, stage, player, round } = this.props;
    return (
      <>
        <div className="value-label">
          <span>CASE</span>{" "}
          {round.get("effectiveIndex") +
              " / " +
              game.treatment.roundCount.toString()}
        </div>

        <div className="value-label">
          <span>SCORE</span> {(player.round.get("score"))}
        </div>
        
        <Timer stage={stage} player={player} />

      </>
    );
  }
}
