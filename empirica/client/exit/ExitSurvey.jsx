import {
  Button,
  Classes,
  FormGroup,
  Intent,
  Radio,
  RadioGroup,
  TextArea,
} from "@blueprintjs/core";
import { Centered } from "meteor/empirica:core";
import React from "react";

export default class ExitSurvey extends React.Component {
  static stepName = "ExitSurvey";
  state = {
    strategy: "",
    fair: "",
    feedback: "",
    experience: "",
    botUnderstand: "",
    botTrust: "",
    botAdopt: "",
    botUseful: "",
    comments: "",
  };

  handleChange = (event) => {
    const el = event.currentTarget;
    this.setState({ [el.name]: el.value });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { game } = this.props;

    this.props.onSubmit(this.state);
  };

  exitMessage = (player, game) => {
    return (
      <div>
        <h1> Exit Survey </h1>
      </div>
    );
  };

  exitForm = (game) => {
    const {
      strategy,
      fair,
      feedback,
      experience,
      botUnderstand,
      botTrust,
      botAdopt,
      botUseful,
      comments,
    } = this.state;

    return (
      <div>
        {" "}
        <p>
          Please answer the following short survey.
        </p>
        <form onSubmit={this.handleSubmit}>
          
          <div className="form-line">
            <RadioGroup
              inline={true}
              name="experience"
              label="How often do you play card games?"
              onChange={this.handleChange}
              selectedValue={experience}
            >
              <Radio
                selected={experience}
                name="experience"
                value="1"
                label="Never"
                onChange={this.handleChange}
              />
              <Radio
                selected={experience}
                name="experience"
                value="2"
                label="Occasionally"
                onChange={this.handleChange}
              />
              <Radio
                selected={experience}
                name="experience"
                value="3"
                label="Often"
                onChange={this.handleChange}
              />
              <Radio
                selected={experience}
                name="experience"
                value="4"
                label="All the time"
                onChange={this.handleChange}
              />
            </RadioGroup>
        

            <FormGroup
              className={"form-group"}
              inline={false}
              label={"Feedback, including problems you encountered."}
              labelFor={"fair"}
              //className={"form-group"}
              required
            >
              <TextArea
                id="feedback"
                name="feedback"
                large={true}
                intent={Intent.PRIMARY}
                onChange={this.handleChange}
                value={feedback}
                fill={true}
                required
              />
            </FormGroup>
          </div>

          <Button type="submit" intent={"primary"} rightIcon={"key-enter"}>
            Submit
          </Button>
        </form>{" "}
      </div>
    );
  };

  render() {
    const { player, game } = this.props;
    return (
      <Centered>
        <div className="exit-survey">
          {this.exitMessage(player, game)}
          <hr />
          {this.exitForm(game)}
        </div>
      </Centered>
    );
  }
}
