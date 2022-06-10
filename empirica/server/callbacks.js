import Empirica from "meteor/empirica:core";

// onGameStart is triggered once per game before the game starts, and before
// the first onRoundStart. It receives the game and list of all the players in
// the game.
Empirica.onGameStart((game) => {
  game.players.forEach((player) => {
    player.set("cumulativeScore", 0);
    player.stage.set("firstPrediction", player.round.get("firstPrediction"));
  });
});

// onRoundStart is triggered before each round starts, and before onStageStart.
// It receives the same options as onGameStart, and the round that is starting.
Empirica.onRoundStart((game, round) => {

  const dummyCard = {rank: '10', suit: "clubs"}
  const dummyCard2 = {rank: 'ace', suit: "hearts"}
  const dummyHand = [dummyCard, dummyCard2]

  game.players.forEach((player) => {
    player.round.set("hand", dummyHand);
  })

  console.log("onRoundStart start");
  if (round.get("case") === "initial") {
    game.players.forEach((player) => {
      player.round.set("score", 0);
      if (player.bot) {
        player.round.set("prediction", round.get("task").model_prediction_prob);
      } else {
        player.round.set("prediction", null);

        if (round.get("practice")) {
          player.set(
            `prediction-practice-${round.get("effectiveIndex")}`,
            null
          );
        } else {
          player.set(`prediction-${round.get("effectiveIndex")}`, null);
        }
        player.round.set("score", 0);
      }
    });
  }

  if (round.get("case") === "revise") {
    game.players.forEach((player) => {
      if (player.bot) {
        player.round.set("prediction", round.get("task").model_prediction_prob);
      } else {
        if (round.get("practice")) {
          console.log(
            "previous prediction",
            player.get(`prediction-practice-${round.get("effectiveIndex")}`)
          );
          player.round.set(
            "prediction",
            player.get(`prediction-practice-${round.get("effectiveIndex")}`)
          );
          player.round.set(
            "previousPrediction",
            player.get(`prediction-practice-${round.get("effectiveIndex")}`)
          );
        } else {
          console.log(
            "previous prediction",
            player.get(`prediction-${round.get("effectiveIndex")}`)
          );
          player.round.set(
            "prediction",
            player.get(`prediction-${round.get("effectiveIndex")}`)
          );
          player.round.set(
            "previousPrediction",
            player.get(`prediction-${round.get("effectiveIndex")}`)
          );
        }
      }
    });
  }
});

// onStageStart is triggered before each stage starts.
// It receives the same options as onRoundStart, and the stage that is starting.
Empirica.onStageStart((game, round, stage) => {
  console.log("onstage start now");

  const dummyCard = {rank: '10', suit: "clubs"}
  if (stage.name === "outcome" || stage.name === "practice-outcome"){
    game.players.forEach((player) => {
      let card = round.get(`played-${player.get("seat")}`)
      stage.set(`played-${player.get("seat")}`, card)
    }) 
  } else {
    game.players.forEach((player) => {
      stage.set(`played-${player.get("seat")}`, dummyCard)
      round.set(`played-${player.get("seat")}`, null)
    })  
  }

  if (round.get("case") === "revise" && game.treatment.giveFeedback) {
    if (stage.name === "outcome" || stage.name === "practice-outcome") {
      const outcome = round.get("task").correct_answer === "Yes" ? 1 : 0;

      game.players.forEach((player) => {
        const prediction = player.round.get("prediction");
        if (prediction !== null && prediction !== undefined) {
          const score = 1 - Math.pow(prediction - outcome, 2); //1 - brier score
          console.log(
            "outcome is ",
            outcome,
            "prediction",
            prediction,
            "score",
            score
          );
          player.round.set("score", score);
        } else {
          player.round.set("score", 0);
        }
      });
    }
  }
});

// onStageEnd is triggered after each stage.
// It receives the same options as onRoundEnd, and the stage that just ended.
Empirica.onStageEnd((game, round, stage) => {
  const winner = Math.max(game.players.map((player) => {
    player.get("prediction")
  }))
  round.set("winner", winner)
});

// onRoundEnd is triggered after each round.
// It receives the same options as onGameEnd, and the round that just ended.
Empirica.onRoundEnd((game, round) => {
  if (round.get("case") === "initial") {
    game.players.forEach((player) => {
      const prediction = player.round.get("prediction");
      if (prediction !== null && prediction !== undefined) {
        // player.set(`prediction-${round.get("effectiveIndex")}`, prediction);
        if (round.get("practice")) {
          player.set(
            `prediction-practice-${round.get("effectiveIndex")}`,
            prediction
          );
        } else {
          player.set(`prediction-${round.get("effectiveIndex")}`, prediction);
        }
      } else {
        game.players.forEach((player) => {
          if (round.get("practice")) {
            player.set(
              `prediction-practice-${round.get("effectiveIndex")}`,
              null
            );
          } else {
            player.set(`prediction-${round.get("effectiveIndex")}`, null);
          }
        });
      }
    });
  }

  if (round.get("case") === "revise" && game.treatment.giveFeedback === false) {
    const outcome = round.get("task").correct_answer === "Yes" ? 1 : 0;

    game.players.forEach((player) => {
      const prediction = player.round.get("prediction");
      if (prediction !== null && prediction !== undefined) {
        const score = 1 - Math.pow(prediction - outcome, 2); //1 - brier score
        console.log(
          "outcome is ",
          outcome,
          "prediction",
          prediction,
          "score",
          score
        );
        player.round.set("score", score);
      } else {
        player.round.set("score", 0);
      }
    });
  }

  if (round.get("case") === "revise" && !round.get("practice")) {
    game.players.forEach((player) => {
      player.set(
        "cumulativeScore",
        player.get("cumulativeScore") + player.round.get("score")
      );
    });
  }
});

// onGameEnd is triggered when the game ends.
// It receives the same options as onGameStart.
Empirica.onGameEnd((game) => {
  console.log("The game", game._id, "has ended");
  const conversionRate = game.treatment.conversionRate;

  game.players.forEach((player) => {
    const bonus =
      player.get("cumulativeScore") > 0
        ? Math.round(player.get("cumulativeScore") * conversionRate * 100) / 100
        : 0;
    player.set("bonus", bonus);
  });
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
