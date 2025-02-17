# msc_thesis
This repository contains the code for an experiment regarding the possibility of using rules-based agents as a proxy for human behaviour in multiagent reinforcement learning. It consists of four major folders: empirica, card_game_files, and dqn_agents, which are described below. Each draws on the results of the others, but the Empirica section is written in JS and does not draw directly on code from the other two folders. More detailed Readme files will be made available within each subfolder.

The Empirica folder is used to run an online human-participant experiment with the Empirica model. AI agents pre-trained locally are tested in live games against volunteers online.

The card_game_files folder renders a card game environment on the local machine using Pygame. The user can play the game with AI agents trained in advance.

The dqn_agents folder runs training of a set of DQN agents to learn to play the desired card game. It uses RLLib and Ray to support the training process.
