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
            Now you are moving on to the games. There are four different AI partners
            for you to play with. For each, you will play two games, and then 
            answer two questions about how well you think the agent played, and 
            whether you would choose it as a partner again.
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
