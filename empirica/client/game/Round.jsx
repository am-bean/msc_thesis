import React from "react";

import PlayerProfile from "./PlayerProfile.jsx";
import TaskStimulus from "./TaskStimulus.jsx";
import TaskResponse from "./TaskResponse.jsx";

export default class Round extends React.Component {
  renderRound() {
    const { round, stage, player, game } = this.props;

    return (
      <main className={`main-container single-column`}>
        <header className="header-left">
          <PlayerProfile
            player={player}
            stage={stage}
            game={game}
            round={round}
          />
        </header>

        <section className="content-left">
          <div className="stimulus-card">
            <TaskStimulus {...this.props} />
            <TaskResponse {...this.props} />
          </div>
        </section>

      </main>
    );
  }
  
  render() {
    return  this.renderRound();
  }
}
