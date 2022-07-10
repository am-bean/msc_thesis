import Empirica from "meteor/empirica:core";

import "./callbacks.js";
import "./bots.js";
const path = require('path');

// gameInit is where the structure of a game is defined.
// Just before every game starts, once all the players needed are ready, this
// function is called with the treatment and the list of players.
// You must then add rounds and stages to the game, depending on the treatment
// and the players. You can also get/set initial values on your game, players,
// rounds and stages (with get/set methods), that will be able to use later in
// the game.

Empirica.gameInit((game) => {

  const seats = ['North', 'East', 'South', 'West']
  const partners = {"North":"South", "South":"North", "East":"West", "West":"East"}
  const follows = {"North":"West", "South":"East", "East":"North", "West":"South"}
  const numCards = 6

  const filepath = '../web.browser/app/pretrained_models/'
  const modelPaths = ['test_model.onnx']

  game.players.forEach((player, i) => {
    player.set("avatar", `/avatars/jdenticon/${player._id}`);
    player.set("score", 0);
    player.set("seat", seats[i])
    player.set("partner", partners[seats[i]])
    player.set("follows", follows[seats[i]])
  });

  const roundCount = game.treatment.roundCount || 3;
  const playerCount = game.treatment.playerCount || 4;
  const stageDuration = game.treatment.stageLength || 120;
  const modelStartIndex = game.treatment.partnerIndex || 0;
  console.log(`Using treatment ${modelStartIndex}`)

  for (let i = 0; i < roundCount; i++) {

    const round = game.addRound({
      data: {
        case: "base_game",
        partnerModel: path.resolve(filepath + modelPaths[(modelStartIndex + i) % modelPaths.length]),
        opponentModel: path.resolve(filepath + modelPaths[(modelStartIndex + i) % modelPaths.length]),
        effectiveIndex: i,
      },
    });
    for (let j = 0; j < numCards; j++){
      round.addStage({
        name: `card_${j}`,
        displayName: `Trick ${j}`,
        durationInSeconds: stageDuration,
        data: {
          type: "play",
        },
      });
      round.addStage({
        name: `result_${j}`,
        displayName: `Trick ${j} Outcome`,
        durationInSeconds: stageDuration,
        data: {
          type: "outcome",
        },
      });
      continue;
    }
  }
});
