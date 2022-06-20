import Empirica from "meteor/empirica:core";

// This is where you add bots, like Bob:
const ort = require('onnxruntime-node');
const path = require('path');

Empirica.bot("bob", {
  // // NOT SUPPORTED Called at the beginning of each stage (after onRoundStart/onStageStart)
  onStageStart(bot, game, round, stage, players) {
    console.log("Called bob on stage start")
  },

  async loadNN(actionMask, obs) {
    try {
        // create a new session and run the specific model.
        //
        const filepath = '../web.browser/app/pretrained_models/test_model.onnx'
        const fullpath = path.resolve(filepath)
        const session = await ort.InferenceSession.create(fullpath);

        // prepare inputs. a tensor need its corresponding TypedArray as data
        const infMask = actionMask.map(x => Math.log(x))
        let dataA = new Float32Array(624);
        const dataB = Float32Array.from([0]);
        actionMask.forEach((x, i) => dataA[i] = x)
        obs.forEach((x, i) => dataA[i+24] = x)
        const tensorA = new ort.Tensor('float32', dataA, [1, 624]);
        const tensorB = new ort.Tensor('float32', dataB, [1]);

        // prepare feeds. use model input names as keys.
        const feeds = { obs: tensorA, state_ins: tensorB };

        // feed inputs and run
        const results = await session.run(feeds);

        // read from results
        const dataC = results.output.data;
        const maskData = dataC.map((x, i) => x + infMask[i])

        const action = [].reduce.call(maskData, (m, c, i, arr) => c > arr[m] ? i : m, 0)
        const suitValues = {0: 'spades', 1: 'clubs', 2: 'diamonds', 3: 'hearts'}
        const rankValues = {0: "9", 1: "10", 2: "jack", 3: "queen", 4: "king", 5: "ace"}
        const actionCard = {rank: rankValues[action % 6], suit: suitValues[parseInt(action/6)]}
        return actionCard


    } catch (e) {
        console.error(`failed to inference ONNX model: ${e}.`);
    }
},

  // Called during each stage at tick interval (~1s at the moment)
onStageTick(bot, game, round, stage, secondsRemaining) {
  const suitValues = {spades: 0, clubs: 1, diamonds: 2, hearts: 3}
  const rankValues = {9: 0, 10: 1, jack: 2, queen: 3, king: 4, ace: 5}
  
  if (bot.stage.submitted) {
    return;
  }
  if (stage.get("type") === "play") {
    if ((bot.get("seat") === round.get("winner")) || (round.get(`submitted-${bot.get("follows")}`))){
      

      let hand = bot.round.get("hand")
      const hasLead = (bot.get("seat") === round.get("winner"))
      const isFollowing = (round.get(`submitted-${bot.get("follows")}`))
      let hasSuit = false
      if (hasLead) {console.log(`Bob ${bot.get("seat")} leading`)}
      if (isFollowing) {console.log(`Bob ${bot.get("seat")} following`)}
      if (!hasLead) {hasSuit = hand.some((item) => {return item['suit'] === stage.get(`played-${round.get("winner")}`)['suit'];})}

      let actionMask = new Float32Array(24);
      if (hasSuit) {
        hand.forEach(card => {
          actionMask[suitValues[card['suit']]*6 + rankValues[card['rank']]] = (card['suit'] === stage.get(`played-${round.get("winner")}`)['suit'] ? 1 : 0);
        }); 
      } else {
        hand.forEach(card => {
          actionMask[suitValues[card['suit']]*6 + rankValues[card['rank']]] = 1;
        }); 
      }

      let obs = new Float32Array(600);

      this.loadNN(actionMask, obs).then(action => 
        {console.log(action)
        stage.set(`played-${bot.get("seat")}`, action);
        round.set(`played-${bot.get("seat")}`, action);
        let hand = bot.round.get("hand").filter((item) => {return !((item['rank'] === action['rank']) && (item['suit'] === action['suit']));});
        bot.round.set("hand", hand);
        round.set(`submitted-${bot.get("seat")}`, true);
        bot.stage.submit();
      })
    }
  }
  if (stage.get("type") === "outcome") {
    const cardDetails = round.get(`played-${bot.get("seat")}`);
    stage.set(`played-${bot.get("seat")}`, cardDetails);
    bot.stage.submit();
    round.set(`submitted-${bot.get("seat")}`, true);
  }
},

  // // NOT SUPPORTED A player has changed a value
  // // This might happen a lot!
  // onStagePlayerChange(bot, game, round, stage, players, player) {}

  // // NOT SUPPORTED Called at the end of the stage (after it finished, before onStageEnd/onRoundEnd is called)
  // onStageEnd(bot, game, round, stage, players) {}
});