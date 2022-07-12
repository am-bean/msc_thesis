import React from "react";

import PlayerProfile from "./PlayerProfile.jsx";
import TaskStimulus from "./TaskStimulus.jsx";
import TaskResponse from "./TaskResponse.jsx";
import IntermediateSurvey from "./IntermediateSurvey.jsx";

export default class Round extends React.Component {

  renderStimulus = (stage) => {
    const questions = stage.get("type") !== "round_questions"
    if (questions) {
      return (<div className="stimulus-card">
                        <TaskStimulus {...this.props} />
                        <TaskResponse {...this.props} />
                      </div>)
    } else {
      return (<div className="stimulus-card">
      <IntermediateSurvey {...this.props} />
    </div>)
    }
  }

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
          {this.renderStimulus(stage)};
        </section>
      </main>
    );
  }
  
  render() {
    return  this.renderRound();
  }
}
