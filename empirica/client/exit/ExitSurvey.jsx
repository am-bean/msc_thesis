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
    age: "",
    gender: "",
    strategy: "",
    fair: "",
    feedback: "",
    education: "",
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

    if (
      (this.state.botUnderstand === "" ||
        this.state.botTrust === "" ||
        this.state.botAdopt === "" ||
        this.state.botUseful === "") &&
      game.treatment.playerCount > 1
    ) {
      alert(
        "Please answer all the radio button survey questions before you can submit."
      );
      return;
    }

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
      age,
      gender,
      strategy,
      fair,
      feedback,
      education,
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
          Please answer the following short survey. Fields with asterisk (*) are
          required.
        </p>
        <form onSubmit={this.handleSubmit}>
          <div className="form-line">
            <FormGroup
              inline={true}
              label={"Age"}
              labelFor={"age"}
              className={"form-group exit-radio-area"}
            >
              <input
                id="age"
                className={Classes.INPUT}
                type="number"
                min="0"
                max="150"
                step="1"
                dir="auto"
                name="age"
                value={age}
                onChange={this.handleChange}
              />
            </FormGroup>

            <FormGroup
              inline={true}
              label={"Gender"}
              labelFor={"gender"}
              className={"form-group exit-radio-area"}
            >
              <input
                id="gender"
                className={Classes.INPUT}
                type="text"
                dir="auto"
                name="gender"
                value={gender}
                onChange={this.handleChange}
              />
            </FormGroup>
          </div>

          <div className="form-line">
            <RadioGroup
              inline={true}
              name="education"
              label="Highest Education Qualification?"
              onChange={this.handleChange}
              selectedValue={education}
            >
              <Radio
                selected={education}
                name="education"
                value="high-school"
                label="High School"
                onChange={this.handleChange}
              />
              <Radio
                selected={education}
                name="education"
                value="bachelor"
                label="US Bachelor's Degree"
                onChange={this.handleChange}
              />
              <Radio
                selected={education}
                name="education"
                value="master"
                label="Master's or higher"
                onChange={this.handleChange}
              />
              <Radio
                selected={education}
                name="education"
                value="other"
                label="Other"
                onChange={this.handleChange}
              />
            </RadioGroup>
          </div>

          <div className="form-line thirds">
            <FormGroup
              className={"form-group"}
              inline={false}
              label={"How would you describe your strategy in the game?*"}
              labelFor={"strategy"}
              //className={"form-group"}
              required
            >
              <TextArea
                id="strategy"
                large={true}
                intent={Intent.PRIMARY}
                onChange={this.handleChange}
                value={strategy}
                fill={true}
                name="strategy"
                required
              />
            </FormGroup>

            <FormGroup
              className={"form-group"}
              inline={false}
              label={"Do you feel the pay was fair?"}
              labelFor={"fair"}
              //className={"form-group"}
            >
              <TextArea
                id="fair"
                name="fair"
                large={true}
                intent={Intent.PRIMARY}
                onChange={this.handleChange}
                value={fair}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              className={"form-group"}
              inline={false}
              label={"Feedback, including problems you encountered.*"}
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

          {game.treatment.playerCount > 1 ? (
            <div>
              <div className="form-line">
                <RadioGroup
                  required
                  inline={true}
                  name="botUnderstand"
                  label="Was the A.I. prediction system easy to understand?*"
                  onChange={this.handleChange}
                  selectedValue={botUnderstand}
                >
                  <Radio
                    selected={botUnderstand}
                    name="botUnderstand"
                    value="extremely-easy"
                    label="Extremely easy"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botUnderstand}
                    name="botUnderstand"
                    value="somewhat-easy"
                    label="Somewhat easy"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botUnderstand}
                    name="botUnderstand"
                    value="neither"
                    label="Neither easy nor difficult"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botUnderstand}
                    name="botUnderstand"
                    value="somewhat-difficult"
                    label="Somewhat difficult"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botUnderstand}
                    name="botUnderstand"
                    value="extremely-difficult"
                    label="Extremely difficult"
                    onChange={this.handleChange}
                  />
                </RadioGroup>
              </div>

              <div className="form-line">
                <RadioGroup
                  inline={true}
                  name="botTrust"
                  label="Having experienced the A.I. system, do you trust the A.I. prediction systems?*"
                  onChange={this.handleChange}
                  selectedValue={botTrust}
                  required
                >
                  <Radio
                    selected={botTrust}
                    name="botTrust"
                    value="extremely-trust"
                    label="Extremely trust"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botTrust}
                    name="botTrust"
                    value="somewhat-trust"
                    label="Somewhat trust"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botTrust}
                    name="botTrust"
                    value="neither"
                    label="Neither trust nor distrust"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botTrust}
                    name="botTrust"
                    value="somewhat-distrust"
                    label="Somewhat distrust"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botTrust}
                    name="botTrust"
                    value="extremely-distrust"
                    label="Extremely distrust"
                    onChange={this.handleChange}
                  />
                </RadioGroup>
              </div>

              <div className="form-line">
                <RadioGroup
                  inline={true}
                  name="botAdopt"
                  label="Having experienced the A.I. system, how likely would you be to adopt A.I. prediction systems?*"
                  onChange={this.handleChange}
                  selectedValue={botAdopt}
                  required
                >
                  <Radio
                    selected={botAdopt}
                    name="botAdopt"
                    value="extremely-likely"
                    label="Extremely likely"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botAdopt}
                    name="botAdopt"
                    value="somewhat-likely"
                    label="Somewhat likely"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botAdopt}
                    name="botAdopt"
                    value="neither"
                    label="Neither likely nor unlikely"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botAdopt}
                    name="botAdopt"
                    value="somewhat-unlikely"
                    label="Somewhat unlikely"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botAdopt}
                    name="botAdopt"
                    value="extremely-unlikely"
                    label="Extremely unlikely"
                    onChange={this.handleChange}
                  />
                </RadioGroup>
              </div>

              <div className="form-line">
                <RadioGroup
                  inline={true}
                  name="botUseful"
                  label="Having experienced the A.I. system, how much would A.I. systems be useful to improve the quality of your decision making?*"
                  onChange={this.handleChange}
                  selectedValue={botUseful}
                  required
                >
                  <Radio
                    selected={botUseful}
                    name="botUseful"
                    value="extremely-useful"
                    label="Extremely useful"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botUseful}
                    name="botUseful"
                    value="very-useful"
                    label="Very useful"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botUseful}
                    name="botUseful"
                    value="moderately-useful"
                    label="Moderately useful"
                    onChange={this.handleChange}
                  />
                  <Radio
                    sselected={botUseful}
                    name="botUseful"
                    value="slightly-useful"
                    label="Slightly useful"
                    onChange={this.handleChange}
                  />
                  <Radio
                    selected={botUseful}
                    name="botUseful"
                    value="not-useful"
                    label="Not at all useful"
                    onChange={this.handleChange}
                  />
                </RadioGroup>
              </div>
              <div className="form-line">
                <FormGroup
                  className={"form-group"}
                  inline={false}
                  label={
                    "Please leave any additional comments about the A.I. system in the space provided below."
                  }
                  labelFor={"comments"}
                  //className={"form-group"}
                >
                  <TextArea
                    id="comments"
                    large={true}
                    intent={Intent.PRIMARY}
                    onChange={this.handleChange}
                    value={comments}
                    fill={true}
                    name="comments"
                  />
                </FormGroup>
              </div>
            </div>
          ) : (
            ""
          )}

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
