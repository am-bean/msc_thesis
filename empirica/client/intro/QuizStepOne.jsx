import React from "react";

import { Centered } from "meteor/empirica:core";

import Radio from "./Radio";

export default class QuizStepOne extends React.Component {
  state = {
    answer: {
      value: "",
      error: false,
    },
    toast: {
      show: false,
      message: "",
    },
  };

  handleChange = (event) => {
    const el = event.currentTarget;
    this.setState({
      [el.name]: {
        value: el.value.trim().toLowerCase(),
        error: false,
      },
    });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { answer } = this.state;

    if (answer.value !== "c") {
      this.setState({
        answer: {
          ...answer,
          error: true,
        },
        toast: {
          show: true,
          message: "Your answer was incorrect. When all cards are the same suit, the highest one wins.",
        },
      });
      return;
    }
    this.props.onNext();
    this.setState({
      answer: {
        error: false,
      },
    });
  };

  render() {
    const { hasPrev, onPrev } = this.props;
    const { answer, toast } = this.state;
    return (
      <Centered className="with-topper">
        <div className="quiz">
          <br/>
          <p>
            Having read the instructions, there are now three questions to ensure
            that you understand the rules before starting the experiment. You may 
            go back to the instructions during this quiz.
          </p>
          <h1> Question 1 </h1>
          {toast.show && (
            <div className="intro-alert alert-error">{toast.message}</div>
          )}
          <form onSubmit={this.handleSubmit}>
            <div>
              <ol className="question">

                  <p>
                    All of the cards shown below are played in a trick. Which one wins?
                  </p>
                  <div className="intro-grid">
                  <img src="cards/king_of_diamonds.svg" alt="King of Diamonds" />
                  <img src="cards/queen_of_diamonds.svg" alt="Queen of Diamonds" />
                  <img src="cards/ace_of_diamonds.svg" alt="Ace of Diamonds" />
                  <img src="cards/9_of_diamonds.svg" alt="Nine of Diamonds" />
                  </div>
                  <br/>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="a"
                      option="a"
                      label="King of Diamonds"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="b"
                      option="b"
                      label="Queen of Diamonds"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="c"
                      option="c"
                      label="Ace of Diamonds"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="d"
                      option="d"
                      label="Nine of Diamonds"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="e"
                      option="e"
                      label="I cannot tell from this information"
                      onChange={this.handleChange}
                    />
                  </div>

              </ol>
            </div>
            <p className="action-step">
              <button type="button" onClick={onPrev} disabled={!hasPrev}>
                Back to instructions
              </button>
              <button type="submit" disabled={answer.value === ""}>
                Submit
              </button>
            </p>
          </form>
        </div>
      </Centered>
    );
  }
}
