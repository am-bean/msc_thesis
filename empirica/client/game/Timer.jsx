import React from "react";

import { StageTimeWrapper } from "meteor/empirica:core";

import Timer from "./Timer.jsx";

class timer extends React.Component {
  startTimer = () => {
    const { remainingSeconds } = this.props;
    const timer = remainingSeconds;
    let minutes = parseInt(timer / 60, 10);
    let seconds = parseInt(timer % 60, 10);
    if (remainingSeconds < 0) return "00:00";
    return ( "Timeout in:  " +
      minutes.toString().padStart(2, "0") +
      ":" +
      seconds.toString().padStart(2, "0")
    );
  };

  render() {
    const { remainingSeconds } = this.props;

    const classes = ["timer"];
    if (remainingSeconds <= 5) {
      classes.push("lessThan5");
    } else if (remainingSeconds <= 10) {
      classes.push("lessThan10");
    }

    return <div className="timer">{this.startTimer()}</div>;
  }
}

export default Timer = StageTimeWrapper(timer);
