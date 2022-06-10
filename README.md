# msc_thesis
This repository contains the code for an experiment regarding the possibility of using rules-based agents as a proxy for human behaviour in multiagent reinforcement learning. It consists of three major folders: empirica, local_pygame, and dqn_agents, which are described below. Each draws on the results of the others, but is self-contained as far as code references. More detailed Readme files will be made available within each subfolder.

The Empirica folder is used to run an online human-participant experiment with the Empirica model. AI agents pre-trained locally are tested in live games against volunteers online.

The local_pygame folder renders a card game environment on the local machine using Pygame. The user can play the game with AI agents trained in advance.

The dqn_agents folder runs training of a set of DQN agents to learn to play the desired card game. It uses RLLib and Ray to support the training process.
