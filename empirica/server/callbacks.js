import Empirica from "meteor/empirica:core";

// onGameStart is triggered once per game before the game starts, and before
// the first onRoundStart. It receives the game and list of all the players in
// the game.
Empirica.onGameStart((game) => {
  game.players.forEach((player) => {
    player.set("cumulativeScore", 0);
  });
});

// onRoundStart is triggered before each round starts, and before onStageStart.
// It receives the same options as onGameStart, and the round that is starting.
Empirica.onRoundStart((game, round) => {

  const ranks = ['9','10','jack','queen','king','ace']
  const suits = ['clubs','hearts','diamonds','spades']
  const deck = suits.flatMap((s) => (ranks.map((r) => ({rank: r, suit: s}))));

  const shuffled = _.shuffle(deck)

  game.players.forEach((player, i) => {
    player.round.set("hand", shuffled.slice(i*6, (i+1)*6));
    player.round.set("score", 0)
  })

  const human = game.players.filter((player) => {return !player.bot;})[0];
  round.set("humanPartner", human.get("partner"))

  round.set("winner", "East");
  let nullObs = new Float32Array(600);
  round.set('cumulative-obs', nullObs);
  round.set('current-stage', 0);

  console.log("onRoundStart start");
  
});

// onStageStart is triggered before each stage starts.
// It receives the same options as onRoundStart, and the stage that is starting.
Empirica.onStageStart((game, round, stage) => {
  console.log(`Stage ${stage.get("type")} start`)

  if (stage.get("type") === "outcome"){
    game.players.forEach((player) => {
      let card = round.get(`played-${player.get("seat")}`)
      stage.set(`played-${player.get("seat")}`, card)
    }) 
  } else if (stage.get("type") === "play") {
    game.players.forEach((player) => {
      stage.set(`played-${player.get("seat")}`, null)
      round.set(`played-${player.get("seat")}`, null)
      round.set(`submitted-${player.get("seat")}`, false)
    }) 
    round.set('current-stage', round.get('current-stage') + 1)
  } else {
    
  }

});

// onStageEnd is triggered after each stage.
// It receives the same options as onRoundEnd, and the stage that just ended.
Empirica.onStageEnd((game, round, stage) => {

  if (stage.get("type") === "play"){

    // Wait a brief moment for server lag
    let i = 0;
    while ((i < 1000) && (game.players.some((player) => {return round.get(`played-${player.get("seat")}`) !== undefined}))) {
      i++;
    }
    if (game.players.every((player) => {return (round.get(`played-${player.get("seat")}`) !== undefined) && (round.get(`played-${player.get("seat")}`) !== null)})){

      round.set("lead", round.get("winner"))
      const leader = round.get("lead");
      const leadCard = round.get(`played-${leader}`);
      const rankValues = {"9":9, "10":10, "jack":11, "queen":12, "king":13, "ace":14};
    
      // Waiting here briefly because the servers can be slow to update values
      stage.set("winningSuit", leadCard["suit"]);
      stage.set("winningRank", rankValues[leadCard["rank"]]);
      stage.set("winningSeat", leader);
      
      game.players.forEach((player) => {
        let card = round.get(`played-${player.get("seat")}`)
        if ((card['suit'] === stage.get("winningSuit")) && (rankValues[card["rank"]] > stage.get("winningRank"))) {
          stage.set("winningRank", rankValues[card["rank"]]);
          stage.set("winningSeat", player.get("seat"));
        } else if ((card['suit'] === "spades") && (stage.get("winningSuit") !== "spades")) {
          stage.set("winningSuit", "spades");
          stage.set("winningRank", rankValues[card["rank"]]);
          stage.set("winningSeat", player.get("seat"));  
        }
      });

      round.set("winner", stage.get("winningSeat"))
      
      game.players.forEach((p) => {
        if ((round.get("winner") === p.get("seat")) || (round.get("winner") === p.get("partner"))){
          p.round.set("score", p.round.get("score") + 1)
        }
      })
    } else {
      console.log("Timed out:")
      game.players.forEach((player) => {player.exit("timedOut")})
    }
  }
});

// onRoundEnd is triggered after each round.
// It receives the same options as onGameEnd, and the round that just ended.
Empirica.onRoundEnd((game, round) => {
});

// onGameEnd is triggered when the game ends.
// It receives the same options as onGameStart.
Empirica.onGameEnd((game) => {
  console.log("The game", game._id, "has ended");
});

// ===========================================================================
// => onSet, onAppend and onChange ==========================================
// ===========================================================================

// onSet, onAppend and onChange are called on every single update made by all
// players in each game, so they can rapidly become quite expensive and have
// the potential to slow down the app. Use wisely.
//
// It is very useful to be able to react to each update a user makes. Try
// nontheless to limit the amount of computations and database saves (.set)
// done in these callbacks. You can also try to limit the amount of calls to
// set() and append() you make (avoid calling them on a continuous drag of a
// slider for example) and inside these callbacks use the `key` argument at the
// very beginning of the callback to filter out which keys your need to run
// logic against.
//
// If you are not using these callbacks, comment them out so the system does
// not call them for nothing.

// // onSet is called when the experiment code call the .set() method
// // on games, rounds, stages, players, playerRounds or playerStages.
// Empirica.onSet((
//   game,
//   round,
//   stage,
//   player, // Player who made the change
//   target, // Object on which the change was made (eg. player.set() => player)
//   targetType, // Type of object on which the change was made (eg. player.set() => "player")
//   key, // Key of changed value (e.g. player.set("score", 1) => "score")
//   value, // New value
//   prevValue // Previous value
// ) => {
//   // // Example filtering
//   // if (key !== "value") {
//   //   return;
//   // }
// });

// // onAppend is called when the experiment code call the `.append()` method
// // on games, rounds, stages, players, playerRounds or playerStages.
// Empirica.onAppend((
//   game,
//   round,
//   stage,
//   player, // Player who made the change
//   target, // Object on which the change was made (eg. player.set() => player)
//   targetType, // Type of object on which the change was made (eg. player.set() => "player")
//   key, // Key of changed value (e.g. player.set("score", 1) => "score")
//   value, // New value
//   prevValue // Previous value
// ) => {
//   // Note: `value` is the single last value (e.g 0.2), while `prevValue` will
//   //       be an array of the previsous valued (e.g. [0.3, 0.4, 0.65]).
// });

// // onChange is called when the experiment code call the `.set()` or the
// // `.append()` method on games, rounds, stages, players, playerRounds or
// // playerStages.
// Empirica.onChange((
//   game,
//   round,
//   stage,
//   player, // Player who made the change
//   target, // Object on which the change was made (eg. player.set() => player)
//   targetType, // Type of object on which the change was made (eg. player.set() => "player")
//   key, // Key of changed value (e.g. player.set("score", 1) => "score")
//   value, // New value
//   prevValue, // Previous value
//   isAppend // True if the change was an append, false if it was a set
// ) => {
//   // `onChange` is useful to run server-side logic for any user interaction.
//   // Note the extra isAppend boolean that will allow to differenciate sets and
//   // appends.
//    Game.set("lastChangeAt", new Date().toString())
// });

// // onSubmit is called when the player submits a stage.
// Empirica.onSubmit((
//   game,
//   round,
//   stage,
//   player // Player who submitted
// ) => {
// });
