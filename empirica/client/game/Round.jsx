import React from "react";

import PlayerProfile from "./PlayerProfile.jsx";
import TaskStimulus from "./TaskStimulus.jsx";
import TaskResponse from "./TaskResponse.jsx";

import Instruction from "./component/Instruction.jsx";

export default class Round extends React.Component {
  renderRound() {
    const { round, stage, player, game } = this.props;
    const single = true
      //(stage.get("type") !== "social" && stage.get("type") !== "feedback") ||
      //stage.get("interpretationType") === "None";

    return (
      <main className={`main-container ${single ? "single-column" : ""}`}>
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
  renderInstructions() {
    return (
      <main className={`main-container  single-column`}>
        <header className="header-left"> </header>

        <section className="content-left">
          <div className="stimulus-card small">
            <div className="response">
              <div className="instructions">
                <h1 className={"bp3-heading"}>
                  Instructions - Interactive Round
                </h1>
                <Instruction {...this.props} />
              </div>
            </div>
          </div>
        </section>
      </main>
    );
  }
  render() {
    const { round } = this.props;
    return round.get("case") === "instruction"
      ? this.renderInstructions()
      : this.renderRound();
  }
}
