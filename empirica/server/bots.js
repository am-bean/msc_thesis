import Empirica from "meteor/empirica:core";

// This is where you add bots, like Bob:

Empirica.bot("bob", {
  // // NOT SUPPORTED Called at the beginning of each stage (after onRoundStart/onStageStart)
  onStageStart(bot, game, round, stage, players) {
    console.log("Called bob on stage start")
  },

  // Called during each stage at tick interval (~1s at the moment)
  onStageTick(bot, game, round, stage, secondsRemaining) {
    if (bot.stage.submitted) {
      return;
    }
    console.log("called bob")
    if (stage.get("type") === "play") {
      if ((bot.get("seat") === round.get("winner")) || (round.get(`submitted-${bot.get("follows")}`))){
        const cardDetails = bot.round.get("hand")[0];
        stage.set(`played-${bot.get("seat")}`, cardDetails);
        round.set(`played-${bot.get("seat")}`, cardDetails);
        let hand = bot.round.get("hand").filter((item) => {return item !== cardDetails;});
        bot.round.set("hand", hand);
        console.log("bob played");
        bot.stage.submit();
      }
    }
    if (stage.get("type") === "outcome") {
      const cardDetails = round.get(`played-${bot.get("seat")}`);
      stage.set(`played-${bot.get("seat")}`, cardDetails);
      bot.stage.submit();
    }
  },

  // // NOT SUPPORTED A player has changed a value
  // // This might happen a lot!
  // onStagePlayerChange(bot, game, round, stage, players, player) {}

  // // NOT SUPPORTED Called at the end of the stage (after it finished, before onStageEnd/onRoundEnd is called)
  // onStageEnd(bot, game, round, stage, players) {}
});