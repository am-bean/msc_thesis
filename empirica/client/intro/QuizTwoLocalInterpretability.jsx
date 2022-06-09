import { Centered } from "meteor/empirica:core";
import React from "react";
import Radio from "./Radio";

export default class QuizTwoLocalInterpretability extends React.Component {
  state = {
    answer: {
      value: "",
      error: false,
    },
    answer_2: {
      value: "",
      error: false,
    },
    answer_3: {
      value: "",
      error: false,
    },
    answered: 0,
  };

  handleChange = (event) => {
    const el = event.currentTarget;
    let { answered } = this.state;
    this.setState({
      [el.name]: {
        value: el.value.trim().toLowerCase(),
        error: false,
      },
      answered: answered < 3 ? answered + 1 : answered,
    });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { nextStep, giveFeedback } = this.props;
    const { answer, answer_2, answer_3, answered } = this.state;
    let count = 0;

    if (answer.value !== "d") {
      this.setState({
        answer: {
          ...answer,
          error: true,
        },
      });
      count++;
    }
    if (answer_2.value !== "true") {
      this.setState({
        answer_2: {
          ...answer_2,
          error: true,
        },
      });
      count++;
    }

    if (answer_3.value != "a" && giveFeedback) {
      this.setState({
        answer_3: {
          ...answer_3,
          error: true,
        },
      });
      count++;
    }

    if (count > 0) {
      nextStep(false);
      return;
    }
    nextStep(true);
  };

  render() {
    const { answer, answer_2, answer_3, answered } = this.state;
    const { giveFeedback } = this.props;
    const passedPoint = giveFeedback ? 3 : 2;
    return (
      <Centered>
        <div className="quiz">
          <h2>Quiz </h2>
          <p>
            Having read the instructions, please answer the following question
            before starting the experiment.
          </p>
          <form onSubmit={this.handleSubmit}>
            <div>
              <ol className="question">
                <li
                  className={`question-list${
                    answer.error ? " wrong-answer" : ""
                  }`}
                >
                  <p>In step 2, you will:</p>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="a"
                      option="a"
                      label="Receive predictions made by an AI system"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="b"
                      option="b"
                      label="Receive predictions made by other people"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="c"
                      option="c"
                      label="Have a chance to revise your initial predictions from step 1"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer.value}
                      name="answer"
                      value="d"
                      option="d"
                      label="Both a and c"
                      onChange={this.handleChange}
                    />
                  </div>
                </li>
                <li
                  className={`question-list${
                    answer_2.error ? " wrong-answer" : ""
                  }`}
                >
                  <p>
                    True or False: The AI system’s predictions will be
                    accompanied by information about how the AI system makes its
                    predictions.
                  </p>
                  <div>
                    <Radio
                      selected={answer_2.value}
                      name="answer_2"
                      value="false"
                      label="False"
                      onChange={this.handleChange}
                    />
                  </div>
                  <div>
                    <Radio
                      selected={answer_2.value}
                      name="answer_2"
                      value="true"
                      label="True"
                      onChange={this.handleChange}
                    />
                  </div>
                </li>
                {giveFeedback && (
                  <li
                    className={`question-list${
                      answer_3.error ? " wrong-answer" : ""
                    }`}
                  >
                    <p>Which of the following two statements is true:</p>
                    <div>
                      <Radio
                        selected={answer_3.value}
                        name="answer_3"
                        value="a"
                        label="After you revise your prediction, you will receive information about whether that couple actually had a second date."
                        onChange={this.handleChange}
                      />
                    </div>
                    <div>
                      <Radio
                        selected={answer_3.value}
                        name="answer_3"
                        value="b"
                        label="Even after you revise your prediction, you will not receive information about whether the couple actually went on a second date."
                        onChange={this.handleChange}
                      />
                    </div>
                  </li>
                )}
              </ol>
            </div>
            <p>
              <button
                type="submit"
                className="btn-prediction-big"
                disabled={answered < passedPoint}
              >
                Submit
              </button>
            </p>
          </form>
        </div>
      </Centered>
    );
  }
}
