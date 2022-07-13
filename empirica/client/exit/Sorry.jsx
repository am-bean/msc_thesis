import React from "react";

import { Centered } from "meteor/empirica:core";
import { Button } from "@blueprintjs/core";

export default class Sorry extends React.Component {
  static stepName = "Sorry";

  render() {
    const { player } = this.props;
    let msg;
    switch (player.exitStatus) {
      case "gameFull":
        msg = "All games you are eligible for have filled up too fast...";
        break;
      case "gameLobbyTimedOut":
        msg = "There were NOT enough players for the game to start..";
        break;
      case "playerEndedLobbyWait":
        msg =
          "You decided to stop waiting, we are sorry it was too long a wait.";
        break;
      case "timedOut":
        msg =
          "You timed out of the games.";
        break;
      default:
        msg = "The game timed out.";
        break;
    }
    return (
      <Centered>
        <div className="score">
          <h1>Sorry!</h1>
          <br/>
          <p>Sorry, you were not able to play today! {msg}</p>
          <br/>
          <p>
            <strong>If you want to try again, clear your browser cookies.</strong>{" "}
          </p>

        </div>
      </Centered>
    );
  }
}
