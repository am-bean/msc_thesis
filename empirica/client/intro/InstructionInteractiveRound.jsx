import React from "react";

import { Centered } from "meteor/empirica:core";

export default class InstructionInteractiveRound extends React.Component {
  render() {
    const { hasPrev, hasNext, onNext, onPrev, game } = this.props;

    return (
      <Centered>
        <div className="instructions">
          <h1 className={"bp3-heading"}> Instructions - Interactive Round</h1>

          {!game.treatment.revealBots ? (
            <div>
              <p>
                Now we provide the other player's predictions for your last
                forecasts.
              </p>
              <p>
                You can decide whether or not to modify the predictions made in
                the previous step. You can choose to modify your predictions at
                any point. If you want to modify your results, select the value
                you want, otherwise please reselect the same value.
              </p>
            </div>
          ) : game.treatment.interpretationType === "Global" ? (
            <div>
              <p>
                Now we provide the A.I. model predictions for your last
                forecasts.
              </p>
              <p>
                You can decide whether or not to modify the predictions made in
                the previous step. You can choose to modify your predictions at
                any point. If you want to modify your results, select the value
                you want, otherwise please reselect the same value.
              </p>
              <p>
                The A.I. algorithm was trained based on data from 1,000 dates
                and the actual outcomes (i.e. whether a match was successful or
                not). The following chart explains which factors or attributes
                the A.I. algorithm weighs more as it arrives at its predictions.
              </p>
              <img
                className="interpretation-image"
                src="/task/tasks/global.png"
              />
              <p>
                According to A.I. algorithm,{" "}
                <strong>Man’s Attractiveness</strong>,{" "}
                <strong>Woman’s Attractiveness</strong>, and{" "}
                <strong>Woman’s Fun</strong> are the most important factors
                influencing the match probabilities. The next most important
                factors are <strong>Woman’s Shared Interests</strong> and{" "}
                <strong>Man’s Fun</strong> .
              </p>
              <p>
                On the other hand, the algorithm indicates that the
                <strong>Participant’s Sincerity</strong> or{" "}
                <strong>Man’s Ambition</strong> has little effect on whether a
                speed date will be in a match. Whether the participants are of
                the <strong>Same Race</strong> or <strong>Man’s Race</strong> is
                determined to be the least important factor.
              </p>
            </div>
          ) : game.treatment.interpretationType === "Local" ? (
            <div>
              <p>
                Now we provide the A.I. model predictions for your last
                forecast.
              </p>
              <p>
                You can decide whether or not to modify the predictions made in
                the previous step. You can choose to modify your predictions at
                any point. If you want to modify your results, select the value
                you want, otherwise please reselect the same value.
              </p>
              <p>
                The A.I. algorithm was trained based on data from 1,000 dates
                and the actual outcomes (i.e. whether a match was successful or
                not). For example, the algorithm shows that the matching
                probability for the couple below is 76%, and the following chart
                explains why the algorithm derived such a result.
              </p>
              <img className="interpretation-image" src="/task_sample.png" />
              <img
                className="interpretation-image"
                src="/task/tasks/1049.png"
              />
              <p>
                According to the algorithm, <strong>Woman</strong> received a
                high score between 7 and 8 points from her partner in{" "}
                <strong>Attractiveness</strong>, which raised the couple's
                matching probability by more than <strong>15%</strong>. The
                participants' high <strong>Shared Interests</strong> also played
                a <strong>positive</strong> role in the couple's matching
                probability.
              </p>
              <p>
                On the other hand, a relatively low score of{" "}
                <strong> Man’s Attractiveness </strong> had{" "}
                <strong>negative </strong> effects on the match probability by
                more than <strong>20%</strong>. The relatively young{" "}
                <strong>Age of Women</strong>
                was also a factor that lowered the chances of matching.
              </p>
            </div>
          ) : (
            <div>
              <p>
                Now we provide the A.I. model predictions for your last
                forecasts.
              </p>
              <p>
                You can decide whether or not to modify the predictions made in
                the previous step. You can choose to modify your predictions at
                any point. If you want to modify your results, select the value
                you want, otherwise please reselect the same value.
              </p>
              <p>
                If you want to modify your results, select the value you want,
                otherwise please reselect the same value.
              </p>
            </div>
          )}

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
