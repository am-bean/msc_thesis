import React from "react";

import { NonIdealState } from "@blueprintjs/core";

export default class Thanks extends React.Component {
  static stepName = "Thanks";
  render() {
    const { player } = this.props;
    const submissionCode = "Submission code: " + player._id;
    return (
      <div className="thanks-page">
        <NonIdealState
          icon={"thumbs-up"}
          title={submissionCode}
          description="Thank you for participating!"
          //action={"what is an actions?"}
        />
      </div>
    );
  }
}
