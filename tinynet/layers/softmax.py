import numpy as np
from .base import Layer

class Softmax(Layer):
    def __init__(self, name='softmax'):
        super().__init__(name)
    
    def forward(self, input):
        self.input = input
        exps = np.exp(input - np.max(input))
        self.output = exps / np.sum(exps)
        return self.output

    def backward(self, in_gradient):
        return in_gradient
