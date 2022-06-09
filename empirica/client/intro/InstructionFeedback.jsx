import React from "react";

import { Centered } from "meteor/empirica:core";

export default class InstructionFeedback extends React.Component {
  render() {
    const { hasPrev, hasNext, onNext, onPrev, game } = this.props;

    return (
      <Centered>
        <div className="instructions">
          <h1 className={"bp3-heading"}> Instructions - Feedback</h1>

          <p>
            Now we give feedback on how your guess compares to the actual
            outcome of the date
            {""}
            {game.treatment.playerCount > 1
              ? " and the guess of the A.I."
              : "."}
            {/*{game.treatment.revealBots ? "A.I." : "other player"}.*/}
          </p>

          <p>
            The score displayed is calculated based on the Brier score function
            to determine the accuracy of probabilistic predictions.
          </p>

          <p>
            <strong>The score is:</strong>
          </p>

          <p align="center">
            <span style={{ color: "blue" }}>
              <i>
                1 - [the difference between the actual outcome (1 for match, 0
                for no match) and the prediction, squared]
              </i>
            </span>
          </p>

          <p>
            Refer to the table below for an example of how it will look like in
            the experiment:
          </p>

          <img
            className="small-sample-img"
            src={
              game.treatment.playerCount > 1
                ? "/feedbacksample.png"
                : "/feedback_solo.png"
            }
          />
          <p />

          <p>
            <button type="button" onClick={onPrev} disabled={!hasPrev}>
              Previous
            </button>
            <button type="button" onClick={onNext} disabled={!hasNext}>
              Next
            </button>
          </p>
        </div>
      </Centered>
    );
  }
}
