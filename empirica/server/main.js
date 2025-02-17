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
  const modelPaths = ['fcplay.onnx', 'poolplay.onnx', 'selfplay.onnx', 'rulebasedplay.onnx']
  const opponentPath = ['random.onnx']

  game.players.forEach((player, i) => {
    player.set("avatar", `/avatars/jdenticon/${player._id}`);
    player.set("score", 0);
    player.set("seat", seats[i])
    player.set("partner", partners[seats[i]])
    player.set("follows", follows[seats[i]])
  });

  const human = game.players.filter((player) => {return !player.bot;})[0];

  const partnerNames = ['TauBot', 'MuBot', 'SigmaBot', 'PiBot']
  game.set("partnerNames", partnerNames)

  game.players.forEach((player, i) => {
    if (!player.bot) {player.set("name", player.id)}
    else if (player.get("seat") === human.get("follows")) {player.set("name", "GammaBot")}
    else if (player.get("follows") === human.get("seat")) {player.set("name", "PsiBot")}
    else if (player.get("seat") === human.get("partner")) {player.set("name", partnerNames[0])}
  })

  const roundCount = game.treatment.roundCount || 4;
  const playerCount = game.treatment.playerCount || 4;
  const stageDuration = game.treatment.stageLength || 120;
  const shuffledPaths = _.shuffle(modelPaths)
  game.set('modelOrder',shuffledPaths)

  for (let i = 0; i < roundCount * 2; i++) {

    const round = game.addRound({
      data: {
        case: "base_game",
        partnerModel: path.resolve(filepath + shuffledPaths[Math.floor(i / 2) % modelPaths.length]),
        opponentModel: path.resolve(filepath + opponentPath[0]),
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
    round.addStage({
      name: `summary_${i}`,
      displayName: `Game ${i} Outcome`,
      durationInSeconds: stageDuration,
      data: {
        type: "round_outcome",
      },
    });
    if ((i % 2 !== 0)) {
      round.addStage({
        name: `questions_${i}`,
        displayName: `Game ${i} Questions`,
        durationInSeconds: stageDuration,
        data: {
          type: "round_questions",
        },
      });
    }
  }
});
