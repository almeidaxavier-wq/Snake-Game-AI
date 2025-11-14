from collections import deque
from typing import Tuple
from scipy.special import softmax, expit
from dataclasses import dataclass

import time
import numpy as np

@dataclass
class Camada:
    n_neuronios:int

class Brain:
    def __init__(self, *camadas):
        self.camadas = list(camadas)
        #print(len(self.camadas))
        self.pesos = [np.random.randn(self.camadas[i].n_neuronios, self.camadas[i+1].n_neuronios) for i in range(len(self.camadas)-1)]
        #print(self.pesos)
        self.biases = [np.random.randn(self.camadas[i+1].n_neuronios) for i in range(len(self.camadas)-1)]
        self.lr = 0.01
        self.direcoes = ['N', 'S', 'L', 'O']

    def feedforward(self, recompensas, anterior):
        x = np.array(recompensas)
        anterior = anterior.reshape(anterior.size, 1)
        x = x.reshape(1, x.size)
        print(x.size)

        for i, (peso, bias) in enumerate(zip(self.pesos, self.biases)):
            print(anterior.shape, x.shape, peso.shape, (x.T@x).shape, x.reshape(1, x.size).shape)
            print((x @ peso + bias).shape, bias.shape)
            
            
            x = expit(x @ peso + bias)
            print(x.shape, peso.shape, anterior.shape)
            
            self.pesos[i] += anterior * x - peso @ np.triu(x.reshape(x.size, 1)@x.reshape(1, x.size))
            self.biases[i] = np.sum(self.pesos[i] * self.lr, axis=0)
            anterior = x.reshape(x.size, 1)
        
        print(softmax(x), self.direcoes)
        time.sleep(0.5)
        return softmax(x)

class Snake:
    def __init__(self, *initial_positions:Tuple[int, int]):
        self.positions = deque(initial_positions)
        self.brain = Brain(Camada(4), Camada(10), Camada(20), Camada(3))
        

    def forward(self, next_position, grow=False):
        self.positions.appendleft(next_position)
        if not grow:
            self.positions.pop()

    def proxima_direcao(self, recompensas, anterior):
        print(self.brain.direcoes[np.argmax(self.brain.feedforward(recompensas, anterior))])
        return self.brain.direcoes[np.argmax(self.brain.feedforward(recompensas, anterior))], self.brain.feedforward(recompensas, anterior)
