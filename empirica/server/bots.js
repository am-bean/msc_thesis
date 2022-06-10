import Empirica from "meteor/empirica:core";

// This is where you add bots, like Bob:

Empirica.bot("bob", {
  // // NOT SUPPORTED Called at the beginning of each stage (after onRoundStart/onStageStart)
  // onStageStart(bot, game, round, stage, players) {},

  // Called during each stage at tick interval (~1s at the moment)
  onStageTick(bot, game, round, stage, secondsRemaining) {
    if (bot.stage.submitted) {
      return;
    }
    //console.log("stage.name", stage.name);
    console.log("bob returned immediately");
    bot.stage.submit();
  },

  // // NOT SUPPORTED A player has changed a value
  // // This might happen a lot!
  // onStagePlayerChange(bot, game, round, stage, players, player) {}

  // // NOT SUPPORTED Called at the end of the stage (after it finished, before onStageEnd/onRoundEnd is called)
  // onStageEnd(bot, game, round, stage, players) {}
});

Empirica.bot("alice", {
  // // NOT SUPPORTED Called at the beginning of each stage (after onRoundStart/onStageStart)
  // onStageStart(bot, game, round, stage, players) {},

  // Called during each stage at tick interval (~1s at the moment)
  onStageTick(bot, game, round, stage, secondsRemaining) {
    if (bot.stage.submitted) {
      return;
    }
    //console.log("stage.name", stage.name);
    console.log("alice returned immediately");
    bot.stage.submit();
  },

  // // NOT SUPPORTED A player has changed a value
  // // This might happen a lot!
  // onStagePlayerChange(bot, game, round, stage, players, player) {}

  // // NOT SUPPORTED Called at the end of the stage (after it finished, before onStageEnd/onRoundEnd is called)
  // onStageEnd(bot, game, round, stage, players) {}
});
