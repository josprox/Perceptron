"""
Sistemas Inteligentes - Práctica 3: Perceptrón
Modelo (Model) - Arquitectura MVC
Autor: José Melchor
Matrícula: 336009446
Fecha de entrega: 15/06/2026

Este módulo define la clase PerceptronModel, la cual encapsula la lógica matemática del perceptrón:
pesos, función de activación sigmoidal, su derivada y las operaciones de propagación
hacia adelante y hacia atrás.
"""

import numpy as np

class PerceptronModel:
    """
    Representa el modelo matemático del Perceptrón.
    Contiene la lógica de inicialización de pesos, funciones de activación,
    propagación hacia adelante (forward) y propagación hacia atrás (backpropagation).
    """
    def __init__(self, learning_rate=0.2):
        self.learning_rate = learning_rate
        # Inicialización de pesos aleatorios para las 4 entradas (W0 para bias, W1, W2, W3 para variables)
        # Se proponen valores aleatorios entre -1 y 1
        self.weights = np.random.uniform(-1.0, 1.0, (4, 1))
        self.initial_weights = self.weights.copy()
        self.z = None
        self.output = None
        
    @staticmethod
    def sigmoid(x):
        """Función de activación sigmoidal (phi(x))."""
        return 1.0 / (1.0 + np.exp(-x))
    
    @staticmethod
    def sigmoid_derivative(x):
        """Gradiente de la curva sigmoidal de la salida (phi'(x) = x * (1 - x))."""
        return x * (1.0 - x)
    
    def forward(self, X):
        """
        Propagación hacia adelante:
        Realiza el producto punto entre la matriz de entradas (X) y la matriz de pesos (W),
        y luego aplica la función de activación sigmoidal.
        """
        self.z = np.dot(X, self.weights)
        self.output = self.sigmoid(self.z)
        return self.output
        
    def backward(self, X, y_expected):
        """
        Propagación hacia atrás (Backpropagation):
        Calcula el error, los ajustes basados en el gradiente de la sigmoide
        y actualiza los pesos mediante el producto punto de las entradas y los ajustes.
        """
        # 8. Calcula el error
        error = y_expected - self.output
        
        # 9. Calcula los ajustes: error * gradiente de la curva sigmoidal de la salida
        # Nota: La derivada de la sigmoide se calcula sobre la salida obtenida (self.output)
        gradient = self.sigmoid_derivative(self.output)
        adjustments = error * gradient
        
        # 10. Recalcula los pesos con el producto punto entre la transpuesta de las entradas y los ajustes
        # Se aplica la tasa de aprendizaje (learning_rate = 0.2)
        delta_weights = self.learning_rate * np.dot(X.T, adjustments)
        self.weights += delta_weights
        
        # Retorna el error para seguimiento
        return error

    def get_mse(self, X, y_expected):
        """Calcula el Error Cuadrático Medio (MSE)."""
        outputs = self.forward(X)
        return np.mean((y_expected - outputs) ** 2)
