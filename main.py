{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "main.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/cmille47/CorbyRowKickoffDarty2022/blob/main/main.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import json\n",
        "import numpy as np\n",
        "import sklearn\n",
        "from sklearn.model_selection import train_test_split\n",
        "import matplotlib.pyplot as plt\n",
        "import pandas\n",
        "import tensorflow as tf\n",
        "from sklearn import model_selection\n",
        "import torch\n",
        "import pandas as pd"
      ],
      "metadata": {
        "id": "TR1pDW8UA1IL"
      },
      "execution_count": 4,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": 3,
      "metadata": {
        "id": "bt69TdYUzpVH",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "eedaca5b-a09c-4ef7-b202-e495bd971d7c"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Mounted at /content/drive\n"
          ]
        }
      ],
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "class basic_info:\n",
        "    def __init__(self, home, away, closeness):\n",
        "        self.home = home\n",
        "        self.away = away\n",
        "        self.result = closeness\n",
        "\n",
        "\n",
        "class minHeap:\n",
        "    def __init__(self):\n",
        "        self.heap = []\n",
        "\n",
        "    def insert(self, game):\n",
        "        self.heap.append(game)\n",
        "        self.build_min_heap()\n",
        "\n",
        "    def min_heapify(self, position):\n",
        "        left_child = self.left(position)\n",
        "        right_child = self.right(position)\n",
        "        if left_child < len(self.heap) and self.heap[left_child].result < self.heap[position].result:\n",
        "            smallest = left_child\n",
        "        else:\n",
        "            smallest = position\n",
        "        if right_child < len(self.heap) and self.heap[right_child].result < self.heap[smallest].result:\n",
        "            smallest = right_child\n",
        "        if smallest != position:\n",
        "            self.heap[position], self.heap[smallest] = self.heap[smallest], self.heap[position]\n",
        "            self.min_heapify(smallest)\n",
        "\n",
        "    def left(self, k):\n",
        "        return 2 * k + 1\n",
        "\n",
        "    def right(self, k):\n",
        "        return 2 * k + 2\n",
        "\n",
        "    def build_min_heap(self):\n",
        "        n = int((len(self.heap)//2)-1)\n",
        "        for k in range(n, -1, -1):\n",
        "            self.min_heapify(k)\n",
        "\n",
        "    def pop_top(self):\n",
        "        self.heap.pop(0)    \n",
        "        self.build_min_heap()\n",
        "\n",
        "class Net(torch.nn.Module):\n",
        "    def __init__(self, input_size, hidden_size):\n",
        "        super(Net, self).__init__()\n",
        "        self.input_size = input_size\n",
        "        self.hidden_size = hidden_size\n",
        "        self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)\n",
        "        self.relu = torch.nn.ReLU()\n",
        "        self.fc2 = torch.nn.Linear(self.hidden_size, 1)\n",
        "        self.sigmoid = torch.nn.Sigmoid() \n",
        "    def forward(self, x):\n",
        "        hidden = self.fc1(x)\n",
        "        relu = self.relu(hidden)\n",
        "        output = self.fc2(relu)\n",
        "        output = self.sigmoid(output)\n",
        "        return output\n"
      ],
      "metadata": {
        "id": "8W047gNP2KJY"
      },
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def normalize_data(data):\n",
        "    for i in range((len(data))):\n",
        "        num = data[i].max()\n",
        "        if num < 1:\n",
        "            continue\n",
        "        if num < 10:\n",
        "            data[i] = (data[i]) / (10)\n",
        "        elif num < 100:\n",
        "            data[i] = (data[i]) / (100)\n",
        "        elif num < 1000:\n",
        "            data[i] = (data[i]) / (1000)\n",
        "        else:\n",
        "            print(\"Error in normalization! Please check!\")\n",
        "    return data"
      ],
      "metadata": {
        "id": "6PJ3-TdGMBNE"
      },
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def blowoutmetric(val):\n",
        "    val = abs(val - 0.5)\n",
        "    val *= 200\n",
        "    return val"
      ],
      "metadata": {
        "id": "cdCRwDEfP2Ah"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def predict(ML_data):\n",
        "    s1=ML_data.iloc[:,0:].values\n",
        "    model = Net(54, 20) \n",
        "    model.load_state_dict(torch.load('/content/drive/MyDrive/DataStructuresProject/model1.pth'))\n",
        "    input =  s1[:,:-1]\n",
        "    output = s1[:,-1:]\n",
        "    normalize_data(input)\n",
        "\n",
        "    predictions = []\n",
        "    for i in range(len(input)):\n",
        "        inpts = torch.FloatTensor(input[i])\n",
        "        #print(inpts)\n",
        "        target = output[i]   # float32  [0.0] or [1.0]\n",
        "        with torch.no_grad():\n",
        "            oupt = model(inpts)\n",
        "        guess = (target.item(), oupt.item())\n",
        "        predictions.append(blowoutmetric(oupt.item()))\n",
        "        model.eval()\n",
        "    \n",
        "    return predictions\n"
      ],
      "metadata": {
        "id": "xaytkyRFBay_"
      },
      "execution_count": 11,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def displayResult(heap):\n",
        "    go = 'y'\n",
        "    count = 0\n",
        "\n",
        "    while(go == 'y'):\n",
        "        if not count:\n",
        "            print(f\"Closest game on {date}: {heap.heap[0].home} vs {heap.heap[0].away} with a Blowout Metric of {heap.heap[0].result:.2f}\")\n",
        "        else:\n",
        "            print(f\"Next closest game on {date}: {heap.heap[0].home} vs {heap.heap[0].away} with a Blowout Metric of {heap.heap[0].result:.2f}\")\n",
        "\n",
        "        go = input(\"Would you like to continue (y/n): \")\n",
        "        if (go == 'y'):\n",
        "            count += 1\n",
        "            if (count == len(game_set.index)):\n",
        "                print(f\"No more games on {date}\")\n",
        "                go = 'Stop'\n",
        "            \n",
        "            heap.pop_top()"
      ],
      "metadata": {
        "id": "fhbYFS0v56CF"
      },
      "execution_count": 22,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def main():\n",
        "    filepath = '/content/drive/MyDrive/DataStructuresProject/2022_2017_full_data.csv'\n",
        "\n",
        "    #import csv using pandas to format into dataframe\n",
        "    with open(filepath, 'r') as f:\n",
        "        game_set = pd.read_csv(f)\n",
        "\n",
        "    date = input('Enter the date you would like to find games (in format YYYY-MM-DD): ')\n",
        "    game_set = game_set[game_set['date'] == date].reset_index(drop=True)\n",
        "\n",
        "    # check if there are any games \n",
        "    if len(game_set.index) == 0:\n",
        "            print(f\"NO GAMES PLAYED ON {date}\")\n",
        "    else:\n",
        "        print(f'Schedule for {date}:\\n')\n",
        "        for row in game_set.index:\n",
        "            if len(game_set.index) == 1:\n",
        "                print('NO GAMES PLAYED TODAY')\n",
        "            print(f\"{game_set.at[row, 'team'][5:]} vs {game_set.at[row, 'opponent'][5:]}\")\n",
        "        print('')\n",
        "\n",
        "        ML_data = game_set.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1', 'game_ID', 'team', 'opponent', 'date', 'differential'])\n",
        "        heap = minHeap()\n",
        "\n",
        "        predictions = predict(ML_data)\n",
        "\n",
        "        for row in game_set.index:\n",
        "            teamA = game_set.at[row, 'team'][5:]\n",
        "            teamB = game_set.at[row, 'opponent'][5:]\n",
        "            heap.insert(basic_info(teamA, teamB, predictions[row]))\n",
        "\n",
        "        displayResult(heap)\n"
      ],
      "metadata": {
        "id": "WVJRwv4C0IFH"
      },
      "execution_count": 29,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "if __name__ == '__main__':\n",
        "    main()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "5o-tebr6T3F7",
        "outputId": "6b0b14c1-78c2-41d6-ce7a-f606d309ff9e"
      },
      "execution_count": 30,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Enter the date you would like to find games (in format YYYY-MM-DD): no\n",
            "NO GAMES PLAYED ON no\n"
          ]
        }
      ]
    }
  ]
}