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
  
  export default class IntermediateSurvey extends React.Component {
    static stepName = "IntermediateSurvey";
    state = {
      partner: "",
      strength: "",
    };
  
    handleChange = (event) => {
      const el = event.currentTarget;
      console.log('Changed state')
      this.setState({ [el.name]: el.value });
    };
  
    handleSubmit = (event) => {
      event.preventDefault();
      console.log('Clicked submit')
      const { game, player } = this.props;
      player.stage.submit();
      this.props.onSubmit(this.state);
      this.props.onNext();
    };
  
    exitMessage = (player, game) => {
      return (
        <div>
          <h1> Survey </h1>
        </div>
      );
    };
  
    exitForm = (game, stage) => {
      const {
        partner,
        strength,
      } = this.state;
      const first = stage.name == "questions_1"
      
      if (first) {
      return (
        <div>
          {" "}
          <p>
            Please answer the following questions about your partner agent in the last two games:
          </p>
          <form onSubmit={this.handleSubmit}>
            
            <div className="form-line">
              <RadioGroup
                inline={true}
                name="strength"
                label="How would you rate the performance of your partner?"
                onChange={this.handleChange}
                selectedValue={strength}
              >
                <Radio
                  selected={strength}
                  name="strength"
                  value="1"
                  label="Very Weak"
                  onChange={this.handleChange}
                />
                <Radio
                  selected={strength}
                  name="strength"
                  value="2"
                  label="Weak"
                  onChange={this.handleChange}
                />
                <Radio
                  selected={strength}
                  name="strength"
                  value="3"
                  label="Average"
                  onChange={this.handleChange}
                />
                <Radio
                  selected={strength}
                  name="strength"
                  value="4"
                  label="Strong"
                  onChange={this.handleChange}
                />
                                <Radio
                  selected={strength}
                  name="strength"
                  value="5"
                  label="Very Strong"
                  onChange={this.handleChange}
                />
              </RadioGroup>
            </div>
            <Button type="submit" intent={"primary"} rightIcon={"key-enter"} onClick={this.handleSubmit}>
              Submit
            </Button>
          </form>{" "}
        </div>
      );
    } else {
    return (<div>
      {" "}
      <p>
        Please answer the following questions about your partner agent in the last two games:
      </p>
      <form onSubmit={this.handleSubmit}>
        
        <div className="form-line">
          <RadioGroup
            inline={true}
            name="strength"
            label="How would you rate the performance of your partner?"
            onChange={this.handleChange}
            selectedValue={strength}
          >
            <Radio
              selected={strength}
              name="strength"
              value="1"
              label="Very Weak"
              onChange={this.handleChange}
            />
            <Radio
              selected={strength}
              name="strength"
              value="2"
              label="Weak"
              onChange={this.handleChange}
            />
            <Radio
              selected={strength}
              name="strength"
              value="3"
              label="Average"
              onChange={this.handleChange}
            />
            <Radio
              selected={strength}
              name="strength"
              value="4"
              label="Strong"
              onChange={this.handleChange}
            />
                            <Radio
              selected={strength}
              name="strength"
              value="5"
              label="Very Strong"
              onChange={this.handleChange}
            />
          </RadioGroup>
        </div>

        <div className="form-line">
          <RadioGroup
            inline={true}
            name="partner"
            label="Would you rather play with this agent or the previous one as your partner?"
            onChange={this.handleChange}
            selectedValue={partner}
          >
            <Radio
              selected={partner}
              name="partner"
              value="1"
              label="This Agent"
              onChange={this.handleChange}
            />
            <Radio
              selected={partner}
              name="partner"
              value="-1"
              label="Previous Agent"
              onChange={this.handleChange}
            />
            <Radio
              selected={partner}
              name="partner"
              value="0"
              label="Indifferent"
              onChange={this.handleChange}
            />
          </RadioGroup>
        </div>
        
        <Button type="submit" intent={"primary"} rightIcon={"key-enter"} onClick={this.handleSubmit}>
          Submit
        </Button>
      </form>{" "}
    </div>
  );};
}

  
    render() {
      const { player, game, stage } = this.props;
      return (
        <Centered>
          <div className="exit-survey">
            {this.exitMessage(player, game)}
            <hr />
            {this.exitForm(game, stage)}
          </div>
        </Centered>
      );
    }
  }
  