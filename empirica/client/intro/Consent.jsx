import React from "react";

import { Centered, ConsentButton } from "meteor/empirica:core";

export default class Consent extends React.Component {
  render() {
    return (
      <Centered>
        <div className="consent">
          <h2 className="bp3-heading"> Teaching AI to Cooperate with Human 
          Partners through Rule-based Play </h2>
          <br/>
          <h2 className="bp3-heading"> Informed Consent Form </h2>
          <br/>
          <h3 className="bp3-heading"> What is this study about? </h3>
          <p className="bp3-ui-text">
          The aim of this research project is to improve the ability of AI agents
          to be good collaborators with humans. In this study, we are focused on
          AI training methods which lead to a better understanding of new human
          partners. We have built a set of AIs trained with various techniques to
          play a card game. We now seek to compare how well the AIs can cooperate with 
          human partners.
          </p>
          <br/>
          <h3 className="bp3-heading"> General Information </h3>
          <p className="bp3-ui-text">
          We appreciate your interest in participating in this online task. You 
          are invited to participate if you are over the age of 18. 
          Please read through this information before agreeing to participate 
          (if you wish to) by clicking the ‘I AGREE’ box below.
          </p>
          <p className="bp3-ui-text">
          You may ask any questions before deciding to take part by contacting
          the researcher (details below). The Principal Researcher is Andrew Bean, 
          who is attached to the Oxford Internet Institute at the University of 
          Oxford. This project is being completed under the supervision of Dr Luc 
          Rocher and Dr Adam Mahdi. Participants will be asked to read the rules 
          of a card game, complete a few practices to ensure understanding, and 
          then play several rounds with an AI partner. Afterwards, we will ask 
          you about your experience. This should take about 10-15 minutes. No 
          background knowledge is required. We will collect the state of the game 
          (who has which cards, and which actions are taken) for each round of 
          cards. The data will be used to assess which AI agents are best able to 
          coordinate with human play.
          
        </p>
        <br/>
          <h3 className="bp3-heading"> Do I have to take part? </h3>
          <p className="bp3-ui-text">
          No. Please note that participation is voluntary. If you do decide to 
          take part, you may withdraw at any point for any reason before 
          submitting your answers by pressing the ‘Exit’ button/ closing the 
          browser.
          </p>
          <p className="bp3-ui-text">
          All questions and games are optional, but must be completed in order.
          </p>
          <br/>
          <h3 className="bp3-heading"> How will my data be used? </h3>
          <p className="bp3-ui-text">
          We will not collect any data that could directly identify you.
          </p>
          <p className="bp3-ui-text">
          Your IP address will not be stored. We will take all reasonable 
          measures to ensure that data remain confidential.
          </p>
          <p className="bp3-ui-text">
          The responses you provide will be stored in a password-protected 
          electronic file on University of Oxford secure servers and may be 
          used in academic publications, conference presentations, reports or 
          websites. Research data will be stored for three years after 
          publication or public release of the work of the research.
          The data that we collect from you may be transferred to, stored and/ 
          or processed at a destination outside the UK and the European Economic 
          Area. By submitting your personal data, you agree to this transfer, 
          storing or processing.
          </p>
          <br/>
          <h3 className="bp3-heading"> Who will have access to my data? </h3>
          <p className="bp3-ui-text">
          The University of Oxford is the data controller with respect to your
          personal data and, as such, will determine how your personal data is 
          used in the study. The University will process your personal data for 
          the purpose of the research outlined above. Research is a task that we 
          perform in the public interest. Further information about your rights 
          with respect to your personal data is available from 
          https://compliance.admin.ox.ac.uk/individual-rights.
          </p>
          <p className="bp3-ui-text">
          The data you provide may be shared with the other researchers on this 
          project, Dr Adam Mahdi and Dr Luc Rocher.
          </p>
          <p className="bp3-ui-text">
          We would also like your permission to use the data in future studies, 
          and to share data with other researchers (e.g. in online databases). 
          Data will be de-identified before it is shared with other 
          researchers or results are made public.
          </p>
          <p className="bp3-ui-text">
          The results will be written up for an MSc degree.
          </p>
          <br/>
          <h3 className="bp3-heading"> Who has reviewed this study? </h3>
          <p className="bp3-ui-text">
          This project has been reviewed by, and received ethics clearance 
          through, a subcommittee of the University of Oxford Central 
          University Research Ethics Committee SSH_OII_CIA_22_054.

          </p>
          <br/>
          <h3 className="bp3-heading"> Who do I contact if I have a concern or I wish to complain? </h3>
          <p className="bp3-ui-text">
          If you have a concern about any aspect of this study, please speak 
          to Andrew Bean (andrew.bean@oii.ox.ac.uk) or his supervisors, 
          Dr Luc Rocher (luc.rocher@oii.ox.ac.uk) or Dr Adam Mahdi (adam.mahdi@oii.ox.ac.uk)
          and we will do our best to answer your query. I/ We will acknowledge your concern within 10 
          working days and give you an indication of how it will be dealt with. 
          If you remain unhappy or wish to make a formal complaint, please contact 
          the Chair of the Research Ethics Committee at the University of Oxford 
          who will seek to resolve the matter as soon as possible:
          </p>
          <p className="bp3-ui-text">
          Social Sciences & Humanities Interdivisional Research Ethics Committee; 
          Email: ethics@socsci.ox.ac.uk; Address: Research Services, University of 
          Oxford, Boundary Brook House, Churchill Drive, Headington, Oxford OX3 7GB
          </p>
          <br/>
          <h3 className="bp3-heading"> Important Note </h3>
          <p className="bp3-ui-text">
          The next page will ask you for an identifier. Please enter 
          something long and random. This answer will be stored, so DO 
          NOT use anything which could identify you individually.
          </p>

          <h3 className="bp3-heading">
            {" "}
            Please note that you may only participate in this study if you are 18 years 
            of age or over. If you certify that you are 18 years of age or over, and if 
            you have read the information above and agree to participate 
            with the understanding that the data you submit will be processed accordingly, 
            please click the button below to start.
            {" "}
          </h3>

          <br/>
          <ConsentButton text="I AGREE"/>
        </div>
      </Centered>
    );
  }
}
