# NBA Game Prediction Tool
Authors: Christian Miller, Jack Lambert, Joe Gullo, Gabe Elbing

Project Manager: Deeksha Arun 

## Project Overview
The goal of this project is to predict the outcome of a NBA game using a neural network. These predictions are utilized to rank which games will be most competitive on any given day selected by the user. A full writeup of the project can be found here: [NBA-Game-Prediction-Writeup.pdf](https://github.com/cmille47/NBA-ML-Outcome-Predictor/files/9419757/NBA-Game-Prediction-Writeup.pdf)


## Requirements
- All scripts executed using Python 3.8
- Libraries used in acquire_box_score.py
  - basketball_reference_web_scraper
  - pandas
  - datetime
  - os
- Libraries used in MLALG1.ipynb and main.py
  - json
  - numpy
  - sklearn
  - matplotlib
  - pandas
  - tensorflow
  - torch

## High-Level Explanation
Execution of main.py will prompt the user to enter a date. The program will then make a prediction for each game scheduled for this date, returning these games in order from most competitive to least competitive.

The initial data used to train the model is scraped from the acquire_box_score.py script. The data we used spans from 2017 to 2022, but any years could be scraped by executing the script and enterring any start and end date.

The model is trained in the MLALG1.ipynb script, utilizing the data outputted from the acquire_box_score.py script.
