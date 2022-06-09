import React from "react";
import PreRound from "../../intro/PreRound";
import QuizTwoGlobalInterpretability from "../../intro/QuizTwoGlobalInterpretability";
import QuizTwoLocalInterpretability from "../../intro/QuizTwoLocalInterpretability";
import QuizTwoNoInterpretability from "../../intro/QuizTwoNoInterpretability";
import StepTwoGlobalInterpretability from "../../intro/StepTwoGlobalInterpretability.jsx";
import StepTwoLocalInterpretability from "../../intro/StepTwoLocalInterpretability.jsx";
import StepTwoNoInterpretability from "../../intro/StepTwoNoInterpretability.jsx";

export default class Instruction extends React.Component {
  state = {
    quiz: false,
    answered: false,
    preRound: false,
    toast: {},
  };
  goToQuiz = () => {
    this.setState({
      quiz: true,
    });
  };
  goToNextStep = (passed = false) => {
    if (passed) {
      this.setState({
        toast: {
          show: false,
          message: "",
        },
        preRound: true,
      });
      return;
    }
    this.setState({
      toast: {
        show: true,
        message: "Your answer was incorrect. Please try again.",
      },
    });
  };
  handleToNextRound = () => {
    const { player } = this.props;
    player.stage.submit();
  };
  render() {
    const {
      game: { treatment },
    } = this.props;
    const { interpretationType = "None", giveFeedback } = treatment;
    const { toast, quiz, preRound } = this.state;

    if (preRound) {
      return <PreRound onNext={this.handleToNextRound} step={2} />;
    }

    if (quiz && !preRound) {
      return (
        <>
          {toast.show && (
            <div className="intro-alert alert-error">{toast.message}</div>
          )}
          {interpretationType.toLowerCase() === "global" && (
            <QuizTwoGlobalInterpretability
              nextStep={this.goToNextStep}
              giveFeedback={giveFeedback}
            />
          )}
          {interpretationType.toLowerCase() === "local" && (
            <QuizTwoLocalInterpretability
              nextStep={this.goToNextStep}
              giveFeedback={giveFeedback}
            />
          )}
          {interpretationType.toLowerCase() === "none" && (
            <QuizTwoNoInterpretability
              nextStep={this.goToNextStep}
              giveFeedback={giveFeedback}
            />
          )}
        </>
      );
    }
    if (!quiz && !preRound)
      return (
        <>
          {!treatment.revealBots ? (
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
              <button
                type="button"
                className="btn-prediction-big"
                onClick={() => {
                  player.stage.submit();
                }}
              >
                Start the revision of previous cases
              </button>
            </div>
          ) : interpretationType.toLowerCase() === "global" ? (
            <StepTwoGlobalInterpretability
              nextStep={this.goToQuiz}
              giveFeedback={giveFeedback}
            />
          ) : interpretationType.toLowerCase() === "local" ? (
            <StepTwoLocalInterpretability
              nextStep={this.goToQuiz}
              giveFeedback={giveFeedback}
            />
          ) : (
            <StepTwoNoInterpretability
              nextStep={this.goToQuiz}
              giveFeedback={giveFeedback}
            />
          )}
        </>
      );
  }
}
