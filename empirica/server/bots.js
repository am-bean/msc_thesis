import Empirica from "meteor/empirica:core";

// This is where you add bots, like Bob:
const ort = require('onnxruntime-node');
const path = require('path');

Empirica.bot("bob", {
  // // NOT SUPPORTED Called at the beginning of each stage (after onRoundStart/onStageStart)
  onStageStart(bot, game, round, stage, players) {
    console.log("Called bob on stage start")
  },

  async loadNN() {
    try {
        // create a new session and load the specific model.
        //
        // the model in this example contains a single MatMul node
        // it has 2 inputs: 'a'(float32, 3x4) and 'b'(float32, 4x3)
        // it has 1 output: 'c'(float32, 3x3)
        const filepath = '../web.browser/app/pretrained_models/model.onnx'
        const fullpath = path.resolve(filepath)
        const session = await ort.InferenceSession.create(fullpath);

        // prepare inputs. a tensor need its corresponding TypedArray as data
        const dataA = Float32Array.from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
        const dataB = Float32Array.from([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]);
        const tensorA = new ort.Tensor('float32', dataA, [3, 4]);
        const tensorB = new ort.Tensor('float32', dataB, [4, 3]);

        // prepare feeds. use model input names as keys.
        const feeds = { a: tensorA, b: tensorB };

        // feed inputs and run
        const results = await session.run(feeds);

        // read from results
        const dataC = results.c.data;
        console.log(`data of result tensor 'c': ${dataC}`);

    } catch (e) {
        console.error(`failed to inference ONNX model: ${e}.`);
    }
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
      this.loadNN().then(value => {value});
      stage.set(`played-${bot.get("seat")}`, cardDetails);
      round.set(`played-${bot.get("seat")}`, cardDetails);
      let hand = bot.round.get("hand").filter((item) => {return item !== cardDetails;});
      bot.round.set("hand", hand);
      console.log("bob played");
      bot.stage.submit();
      round.set(`submitted-${bot.get("seat")}`, true);
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