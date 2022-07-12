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
            Now you are moving on to the games. There are four games,
            each time you will face the same opponents, but have different
            partners. At the end you will be asked which partners you preferred.
            Good luck!
          </p>

          <p>
            <button
              type="button"
              onClick={onNext}
              className="btn-prediction-big"
            >
              Next
            </button>
          </p>
        </div>
      </Centered>
    );
  }
}
