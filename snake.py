from collections import deque
from typing import Tuple
from scipy.special import softmax
from dataclasses import dataclass

import numpy as np

@dataclass
class Camada:
    n_neuronios:int

class Brain:
    def __init__(self, *camadas):
        self.camadas = list(camadas)
        self.pesos = [np.random.randn(self.camadas[i], self.camadas[i+1]) for i in range(len(camadas)-1)]
        self.biases = [np.random.randn(self.camadas[i+1]) for i in range(len(camadas)-1)]
        self.lr = 0.0001

    def feedforward(self, recompensas):
        x = np.array(recompensas)
        for i, (peso, bias) in enumerate(zip(self.pesos, self.biases)):
            x = x @ peso + bias
            self.pesos[i] = x @ recompensas.T + np.triu(x@x.T) @ peso.T
            self.biases[i] = self.pesos[i] * self.lr

        return softmax(x)

class Snake:
    def __init__(self, initial_position:Tuple[int, int]):
        self.positions = deque([initial_position])
        self.brain = Brain([Camada(4), Camada(10), Camada(20), Camada(3)])
        self.direcoes = ['N', 'S', 'L', 'O']

    def forward(self, next_position, grow=False):
        self.positions.appendleft(next_position)
        if not grow:
            self.positions.pop()

    def proxima_direcao(self, recompensas):
        return np.argmax(self.brain.feedforward(recompensas))
