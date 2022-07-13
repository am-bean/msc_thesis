import React from "react";

import { Centered } from "meteor/empirica:core";

export default class PreRound extends React.Component {
  render() {
    const { onNext, step = 1 } = this.props;

    return (
      <Centered className="with-topper">
        <div className="instructions">
          <h1 className={"bp3-heading"}>Instructions</h1>
          <p className="p-pre-round">
            Now you are moving on to the games. You will play two games each with four different
            AI partners. Pay attention to how well the AI acts as a partner so that you can 
            provide feedback between games.
          </p>
          <p>
            Good luck!
          </p>

          <p>
            <button
              type="button"
              onClick={onNext}
              className="btn-prediction-big"
            >
              Begin
            </button>
          </p>
        </div>
      </Centered>
    );
  }
}
