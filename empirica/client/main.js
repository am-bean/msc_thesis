import { render } from "react-dom";
import Empirica from "meteor/empirica:core";
import InstructionStepOne from "./intro/InstructionStepOne";
import QuizStepOne from "./intro/QuizStepOne";
import QuizStepTwo from "./intro/QuizStepTwo";
import QuizStepThree from "./intro/QuizStepThree";
import PreRound from "./intro/PreRound";
import ExitSurvey from "./exit/ExitSurvey";
import Sorry from "./exit/Sorry";
import Thanks from "./exit/Thanks";
import Round from "./game/Round";
import Consent from "./intro/Consent";
import About from "./game/About";
import NewPlayer from "./intro/NewPlayer";

// Set the Consent Component you want to present players (optional).
Empirica.consent(Consent);

//Could set new player screen more nicely in future version of empirica by doing this
//Empirica.newPlayer(NewPlayer);

Empirica.breadcrumb(null);

Empirica.about(About);


// Introduction pages to show before they play the game (optional).
// At this point they have been assigned a treatment. You can return
// different instruction steps depending on the assigned treatment.
Empirica.introSteps(() => {
  //const steps = []
  const steps = [InstructionStepOne, QuizStepOne, QuizStepTwo, QuizStepThree, PreRound]; 
  return steps;
});

// The Round component containing the game UI logic.
// This is where you will be doing the most development.
// See client/game/Round.jsx to learn more.
Empirica.round(Round);

// End of Game pages. These may vary depending on player or game information.
// For example we can show the score of the user, or we can show them a
// different message if they actually could not participate the game (timed
// out), etc.
// The last step will be the last page shown to user and will be shown to the
// user if they come back to the website.
// If you don't return anything, or do not define this function, a default
// exit screen will be shown.
Empirica.exitSteps((game, player) => {
  return player.exitStatus !== "finished"
    ? [Sorry, Thanks]
    : [ExitSurvey, Thanks]; //ExitSurvey
});

// Start the app render tree.
// NB: This must be called after any other Empirica calls (Empirica.round(),
// Empirica.introSteps(), ...).
// It is required and usually does not need changing.
Meteor.startup(() => {
  render(Empirica.routes(), document.getElementById("app"));
});
