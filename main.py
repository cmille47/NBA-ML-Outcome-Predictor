import json
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas
import tensorflow as tf
from sklearn import model_selection
import torch
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

class basic_info:
    def __init__(self, home, away, closeness):
        self.home = home
        self.away = away
        self.result = closeness


class minHeap:
    def __init__(self):
        self.heap = []

    def insert(self, game):
        self.heap.append(game)
        self.build_min_heap()

    def min_heapify(self, position):
        left_child = self.left(position)
        right_child = self.right(position)
        if left_child < len(self.heap) and self.heap[left_child].result < self.heap[position].result:
            smallest = left_child
        else:
            smallest = position
        if right_child < len(self.heap) and self.heap[right_child].result < self.heap[smallest].result:
            smallest = right_child
        if smallest != position:
            self.heap[position], self.heap[smallest] = self.heap[smallest], self.heap[position]
            self.min_heapify(smallest)

    def left(self, k):
        return 2 * k + 1

    def right(self, k):
        return 2 * k + 2

    def build_min_heap(self):
        n = int((len(self.heap)//2)-1)
        for k in range(n, -1, -1):
            self.min_heapify(k)

    def pop_top(self):
        self.heap.pop(0)    
        self.build_min_heap()

class Net(torch.nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Net, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(self.hidden_size, 1)
        self.sigmoid = torch.nn.Sigmoid() 
    def forward(self, x):
        hidden = self.fc1(x)
        relu = self.relu(hidden)
        output = self.fc2(relu)
        output = self.sigmoid(output)
        return output

def normalize_data(data):
    for i in range((len(data))):
        num = data[i].max()
        if num < 1:
            continue
        if num < 10:
            data[i] = (data[i]) / (10)
        elif num < 100:
            data[i] = (data[i]) / (100)
        elif num < 1000:
            data[i] = (data[i]) / (1000)
        else:
            print("Error in normalization! Please check!")
    return data

def blowoutmetric(val):
    val = abs(val - 0.5)
    val *= 200
    return val

def predict(ML_data):
    s1=ML_data.iloc[:,0:].values
    model = Net(54, 20) 
    model.load_state_dict(torch.load('/content/drive/MyDrive/DataStructuresProject/model1.pth'))
    input =  s1[:,:-1]
    output = s1[:,-1:]
    normalize_data(input)

    predictions = []
    for i in range(len(input)):
        inpts = torch.FloatTensor(input[i])
        #print(inpts)
        target = output[i]   # float32  [0.0] or [1.0]
        with torch.no_grad():
            oupt = model(inpts)
        guess = (target.item(), oupt.item())
        predictions.append(blowoutmetric(oupt.item()))
        model.eval()
    
    return predictions

def displayResult(heap):
    go = 'y'
    count = 0

    while(go == 'y'):
        if not count:
            print(f"Closest game on {date}: {heap.heap[0].home} vs {heap.heap[0].away} with a Blowout Metric of {heap.heap[0].result:.2f}")
        else:
            print(f"Next closest game on {date}: {heap.heap[0].home} vs {heap.heap[0].away} with a Blowout Metric of {heap.heap[0].result:.2f}")

        go = input("Would you like to continue (y/n): ")
        if (go == 'y'):
            count += 1
            if (count == len(game_set.index)):
                print(f"No more games on {date}")
                go = 'Stop'
            
            heap.pop_top()

def main():
    filepath = '/content/drive/MyDrive/DataStructuresProject/2022_2017_full_data.csv'

    #import csv using pandas to format into dataframe
    with open(filepath, 'r') as f:
        game_set = pd.read_csv(f)

    date = input('Enter the date you would like to find games (in format YYYY-MM-DD): ')
    game_set = game_set[game_set['date'] == date].reset_index(drop=True)

    # check if there are any games 
    if len(game_set.index) == 0:
            print(f"NO GAMES PLAYED ON {date}")
    else:
        print(f'Schedule for {date}:\n')
        for row in game_set.index:
            if len(game_set.index) == 1:
                print('NO GAMES PLAYED TODAY')
            print(f"{game_set.at[row, 'team'][5:]} vs {game_set.at[row, 'opponent'][5:]}")
        print('')

        ML_data = game_set.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1', 'game_ID', 'team', 'opponent', 'date', 'differential'])
        heap = minHeap()

        predictions = predict(ML_data)

        for row in game_set.index:
            teamA = game_set.at[row, 'team'][5:]
            teamB = game_set.at[row, 'opponent'][5:]
            heap.insert(basic_info(teamA, teamB, predictions[row]))

        displayResult(heap)

if __name__ == '__main__':
    main()
