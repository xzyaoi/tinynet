#coding:utf-8

from elenet.core import Parameter

class Layer(object):
    def __init__(self, name):
        self.name = name
        self.parameters = []
        self.type = 'unknown'
    
    def forward(self, input):
        '''
        > this function needs to be overridden
        compute the forward pass
        '''
        return self.input, lambda D: D
    
    def build_param(self, tensor):
        '''
        creates a parameter from a tensor, and save to the parameters.
        '''
        param = Parameter(tensor)
        self.parameters.append(param)
        return param
    
    def update(self, optimizer):
        '''
        updates the saved parameters with the given optimizer
        '''
        for param in self.parameters:
            optimizer.update(param)

    def backward(self, in_gradient):
        pass

    def summary(self):
        if hasattr(self, 'weights'):
            return [self.type, self.name, self.weights.tensor.shape]
        else:
            return [self.type, self.name, None]