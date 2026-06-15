"""
Sistemas Inteligentes - Práctica 3: Perceptrón
Autor: José Melchor
Matrícula: 336009446
Fecha de entrega: 15/06/2026
Profesor: Docente UNITEC

Este script implementa un perceptrón con el algoritmo de backpropagation desde cero
siguiendo la arquitectura Modelo-Vista-Controlador (MVC) y los principios SMART.
El objetivo es entrenar al perceptrón para resolver el conjunto de datos especificado en la práctica.

Este archivo es autocompletado y autocontenido para facilitar la entrega académica,
e incluye lectura dinámica de parámetros mediante un archivo de configuración `.env`
así como la graficación de la frontera de decisión en 2D de la neurona.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import os

# ==========================================
# 1. MODELO (Model)
# ==========================================
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
        
    @staticmethod
    def sigmoid(x):
        """Función de activación sigmoidal."""
        return 1.0 / (1.0 + np.exp(-x))
    
    @staticmethod
    def sigmoid_derivative(x):
        """Gradiente de la curva sigmoidal de la salida."""
        return x * (1.0 - x)
    
    def forward(self, X):
        """
        Propagación hacia adelante:
        Realiza el producto punto entre la matriz de entradas y la matriz de pesos,
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
        gradient = self.sigmoid_derivative(self.output)
        adjustments = error * gradient
        
        # 10. Recalcula los pesos con el producto punto entre la transpuesta de las entradas y los ajustes
        # Se aplica la tasa de aprendizaje (learning_rate)
        delta_weights = self.learning_rate * np.dot(X.T, adjustments)
        self.weights += delta_weights
        
        # Retorna el error para seguimiento
        return error

    def get_mse(self, X, y_expected):
        """Calcula el Error Cuadrático Medio (MSE)."""
        outputs = self.forward(X)
        return np.mean((y_expected - outputs) ** 2)


# ==========================================
# 2. VISTA (View)
# ==========================================
class PerceptronView:
    """
    Se encarga de la interfaz con el usuario (consola y visualización de gráficos).
    Sigue el principio de separación de responsabilidades al no contener lógica del modelo.
    """
    @staticmethod
    def print_header(run_num):
        print("=" * 60)
        print(f" EJECUCIÓN # {run_num} - ENTRENAMIENTO DEL PERCEPTRÓN")
        print("=" * 60)

    @staticmethod
    def print_initial_weights(weights):
        print("\nPesos iniciales propuestos aleatoriamente:")
        for i, w in enumerate(weights.flatten()):
            print(f"  W{i} = {w:+.6f}")

    @staticmethod
    def print_training_progress(epoch, mse, interval=10000):
        if epoch % interval == 0 or epoch == 1:
            print(f"Época {epoch:5d} | Error Cuadrático Medio (MSE): {mse:.8f}")

    @staticmethod
    def print_results(expected, obtained, final_weights):
        print("\n" + "-" * 50)
        print("RESULTADOS FINALES DE LA EJECUCIÓN:")
        print("-" * 50)
        print("Muestra | Entradas (X1,X2,X3) | Esperada (Y) | Obtenida (Y_hat) | Error")
        
        # Muestras originales sin la columna de bias en la visualización
        samples = [
            ([0, 0, 1], expected[0,0], obtained[0,0]),
            ([1, 1, 1], expected[1,0], obtained[1,0]),
            ([1, 0, 1], expected[2,0], obtained[2,0]),
            ([0, 1, 1], expected[3,0], obtained[3,0])
        ]
        
        for idx, (x, y_exp, y_obt) in enumerate(samples, 1):
            err = y_exp - y_obt
            print(f"   {idx:2d}   |       {x}       |      {y_exp}       |     {y_obt:.6f}   | {err:+.6f}")
            
        print("\nPesos finales entrenados:")
        for i, w in enumerate(final_weights.flatten()):
            print(f"  W{i} (sesgo) = {w:+.6f}" if i == 0 else f"  W{i} = {w:+.6f}")
        print("\n" + "=" * 60 + "\n")

    @staticmethod
    def plot_errors(run_errors, run_index, save_dir="."):
        """Genera y guarda la gráfica de error contra épocas para una ejecución."""
        plt.figure(figsize=(8, 5))
        plt.plot(run_errors, label=f'MSE (Run {run_index})', color='#1e3d59', linewidth=2)
        plt.title(f'Evolución del Error Cuadrático Medio - Ejecución {run_index}', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Época', fontsize=10)
        plt.ylabel('Error Cuadrático Medio (MSE)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        
        filename = os.path.join(save_dir, f"error_curve_run_{run_index}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        return filename

    @staticmethod
    def plot_combined_errors(all_errors, save_dir="."):
        """Genera una gráfica combinada con las 5 ejecuciones."""
        plt.figure(figsize=(10, 6))
        colors = ['#1e3d59', '#ff6e40', '#17b978', '#3498db', '#7b1fa2']
        for idx, errors in enumerate(all_errors, 1):
            plt.plot(errors, label=f'Ejecución {idx}', color=colors[idx-1], alpha=0.85, linewidth=1.5)
            
        plt.title('Evolución del Error - 5 Ejecuciones Independientes', fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Épocas', fontsize=12)
        plt.ylabel('Error Cuadrático Medio (MSE)', fontsize=12)
        plt.yscale('log')
        plt.grid(True, which="both", linestyle='--', alpha=0.5)
        plt.legend(fontsize=10)
        plt.tight_layout()
        
        filename = os.path.join(save_dir, "error_curve_combined.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        return filename

    @staticmethod
    def plot_decision_boundary(X, y, weights, run_index, save_dir="."):
        """Genera y guarda la gráfica de la frontera de decisión en 2D (X1 y X2)."""
        plt.figure(figsize=(7, 6))
        
        # Malla de prueba para graficar el heatmap
        x_min, x_max = -0.5, 1.5
        y_min, y_max = -0.5, 1.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                             np.linspace(y_min, y_max, 200))
        
        # Preparar datos [Bias=1, X1, X2, X3=1]
        grid_input = np.c_[np.ones(xx.ravel().shape), 
                           xx.ravel(), 
                           yy.ravel(), 
                           np.ones(xx.ravel().shape)]
        
        z = np.dot(grid_input, weights)
        grid_predictions = 1.0 / (1.0 + np.exp(-z))
        grid_predictions = grid_predictions.reshape(xx.shape)
        
        contour = plt.contourf(xx, yy, grid_predictions, levels=50, cmap='RdBu', alpha=0.25)
        cbar = plt.colorbar(contour)
        cbar.set_label('Probabilidad de Predicción ($\hat{y}$)', fontsize=10)
        
        # Trazar frontera de decisión en nivel 0.5
        plt.contour(xx, yy, grid_predictions, levels=[0.5], colors='#1e3d59', linestyles='--', linewidths=2.5)
        
        # Dibujar muestras de entrenamiento
        for i in range(len(y)):
            x1 = X[i, 1]
            x2 = X[i, 2]
            target = y[i, 0]
            color = '#17b978' if target == 1.0 else '#ff6e40'
            label = 'Clase 1 (Y=1)' if target == 1.0 else 'Clase 0 (Y=0)'
            plt.scatter(x1, x2, color=color, s=160, edgecolors='black', linewidths=1.5, zorder=5, 
                        label=label if i < 2 else "")
            
            plt.annotate(f"({int(x1)}, {int(x2)})", (x1 + 0.05, x2 + 0.05), fontsize=9, fontweight='bold', zorder=6)
            
        plt.title(f'Frontera de Decisión - Ejecución {run_index}', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Entrada X1', fontsize=10)
        plt.ylabel('Entrada X2', fontsize=10)
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend(loc='lower left', framealpha=0.9)
        plt.tight_layout()
        
        filename = os.path.join(save_dir, f"decision_boundary_run_{run_index}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        return filename


# ==========================================
# 3. CONTROLADOR (Controller)
# ==========================================
class PerceptronController:
    """
    Orquesta la comunicación entre el Modelo y la Vista.
    Administra la carga de datos, el ciclo de entrenamiento y la lectura de variables de entorno.
    """
    def __init__(self):
        # 1. Definición de la matriz de entrada X (con X0 = 1 para el bias)
        self.X = np.array([
            [1.0, 0.0, 0.0, 1.0],
            [1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 0.0, 1.0],
            [1.0, 0.0, 1.0, 1.0]
        ])
        
        # 2. Definición de la matriz de salida esperada Y
        self.y = np.array([
            [0.0],
            [1.0],
            [1.0],
            [0.0]
        ])
        
        self.view = PerceptronView()
        
        # Cargar variables de configuración desde .env
        self.config = self.load_environment()
        self.epochs = int(self.config.get("EPOCHS", 100000))
        self.learning_rate = float(self.config.get("LEARNING_RATE", 0.2))
        self.save_dir = self.config.get("SAVE_DIR", ".")
        self.log_interval = int(self.config.get("LOG_INTERVAL", 10000))

    @staticmethod
    def load_environment():
        """Carga variables de entorno desde un archivo .env si existe."""
        env_vars = {
            "EPOCHS": "100000",
            "LEARNING_RATE": "0.2",
            "SAVE_DIR": ".",
            "LOG_INTERVAL": "10000"
        }
        
        env_path = ".env"
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            parts = line.split("=", 1)
                            if len(parts) == 2:
                                key, val = parts[0].strip(), parts[1].strip()
                                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                                    val = val[1:-1]
                                env_vars[key] = val
            except Exception as e:
                print(f"Advertencia al leer el archivo .env: {e}")
                
        # Sobrescribir con variables de entorno del sistema si están definidas
        for key in env_vars:
            if key in os.environ:
                env_vars[key] = os.environ[key]
                
        return env_vars

    def train_perceptron(self, model, epochs=None):
        if epochs is None:
            epochs = self.epochs
            
        error_history = []
        for epoch in range(1, epochs + 1):
            model.forward(self.X)
            model.backward(self.X, self.y)
            mse = model.get_mse(self.X, self.y)
            error_history.append(mse)
            self.view.print_training_progress(epoch, mse, interval=self.log_interval)
        return error_history

    def run_experiment(self, run_index, epochs=None, save_dir=None):
        if epochs is None:
            epochs = self.epochs
        if save_dir is None:
            save_dir = self.save_dir
            
        self.view.print_header(run_index)
        model = PerceptronModel(learning_rate=self.learning_rate)
        self.view.print_initial_weights(model.initial_weights)
        error_history = self.train_perceptron(model, epochs)
        final_outputs = model.forward(self.X)
        final_weights = model.weights.copy()
        
        self.view.print_results(self.y, final_outputs, final_weights)
        plot_path = self.view.plot_errors(error_history, run_index, save_dir)
        self.view.plot_decision_boundary(self.X, self.y, final_weights, run_index, save_dir)
        
        return {
            "run_index": run_index,
            "initial_weights": model.initial_weights.flatten().tolist(),
            "final_weights": final_weights.flatten().tolist(),
            "final_outputs": final_outputs.flatten().tolist(),
            "final_mse": float(error_history[-1]),
            "error_history": error_history,
            "plot_path": plot_path
        }

    def run_all_experiments(self, epochs=None, save_dir=None):
        if epochs is None:
            epochs = self.epochs
        if save_dir is None:
            save_dir = self.save_dir
            
        print("INICIANDO EXPERIMENTO DE 5 EJECUCIONES DEL PERCEPTRÓN\n")
        print(f"Configuración activa de .env: Épocas={epochs}, Tasa de aprendizaje={self.learning_rate}, Dir Guardado='{save_dir}'\n")
        
        all_runs_data = []
        all_errors = []
        
        for i in range(1, 6):
            run_data = self.run_experiment(i, epochs, save_dir)
            all_runs_data.append(run_data)
            all_errors.append(run_data["error_history"])
            
        combined_plot = self.view.plot_combined_errors(all_errors, save_dir)
        print(f"Gráficas y resultados guardados en '{save_dir}'.")


if __name__ == "__main__":
    controller = PerceptronController()
    os.makedirs(controller.save_dir, exist_ok=True)
    controller.run_all_experiments()
