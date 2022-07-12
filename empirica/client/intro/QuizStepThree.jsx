import React from "react";

import { Centered } from "meteor/empirica:core";

import Radio from "./Radio";
export default class QuizStepTwo extends React.Component {
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

    if (answer.value !== "d") {
      this.setState({
        answer: {
          ...answer,
          error: true,
        },
        toast: {
          show: true,
          message: "Your answer was incorrect. Since spades `trump` other suits " +
          "we know that the spades must have won.",
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
          <h1> Question 3 </h1>
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
                  <img src="cards/queen_of_clubs.svg" alt="Queen of Clubs" />
                  <img src="cards/ace_of_hearts.svg" alt="Ace of Hearts" />
                  <img src="cards/9_of_spades.svg" alt="Nine of Spades" />
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
                      label="Queen of Clubs"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="c"
                      option="c"
                      label="Ace of Hearts"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="d"
                      option="d"
                      label="Nine of Spades"
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
