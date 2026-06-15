"""
Sistemas Inteligentes - Práctica 3: Perceptrón
Controlador (Controller) - Arquitectura MVC
Autor: José Melchor
Matrícula: 336009446
Fecha de entrega: 15/06/2026

Este módulo define la clase PerceptronController, la cual coordina la interacción
entre el Modelo (PerceptronModel) y la Vista (PerceptronView), carga las variables
de entorno desde el archivo .env, gestiona el proceso de entrenamiento y almacena
los resultados del experimento.
"""

import os
import json
import numpy as np
from model import PerceptronModel
from view import PerceptronView

class PerceptronController:
    """
    Orquesta la comunicación entre el Modelo y la Vista.
    Administra la carga de datos, el ciclo de entrenamiento, la lectura de variables de entorno y la recolección de métricas.
    """
    def __init__(self):
        # 1. Definición de la matriz de entrada X (con X0 = 1 para el sesgo/bias prependido)
        # Las entradas originales son: [0,0,1], [1,1,1], [1,0,1], [0,1,1]
        self.X = np.array([
            [1.0, 0.0, 0.0, 1.0],  # Muestra a
            [1.0, 1.0, 1.0, 1.0],  # Muestra b
            [1.0, 1.0, 0.0, 1.0],  # Muestra c
            [1.0, 0.0, 1.0, 1.0]   # Muestra d
        ])
        
        # 2. Definición de la matriz de salida esperada Y
        self.y = np.array([
            [0.0],  # Muestra a
            [1.0],  # Muestra b
            [1.0],  # Muestra c
            [0.0]   # Muestra d
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
        """
        Carga variables de entorno desde un archivo .env si existe.
        Soporta comentarios y comillas. Usa variables del sistema como fallback.
        """
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
                                # Limpiar comillas
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
        """Ejecuta el ciclo de entrenamiento del perceptrón por las épocas indicadas."""
        if epochs is None:
            epochs = self.epochs
            
        error_history = []
        
        for epoch in range(1, epochs + 1):
            # Propagación hacia adelante
            model.forward(self.X)
            # Propagación hacia atrás y actualización de pesos
            model.backward(self.X, self.y)
            
            # Registrar el MSE cada época para la gráfica
            mse = model.get_mse(self.X, self.y)
            error_history.append(mse)
            
            # Mostrar progreso periódico en la vista de consola usando log_interval
            self.view.print_training_progress(epoch, mse, interval=self.log_interval)
            
        return error_history

    def run_experiment(self, run_index, epochs=None, save_dir=None):
        """Realiza una sola corrida de entrenamiento con pesos aleatorios iniciales."""
        if epochs is None:
            epochs = self.epochs
        if save_dir is None:
            save_dir = self.save_dir
            
        self.view.print_header(run_index)
        
        # Crear modelo de perceptrón con la tasa de aprendizaje cargada de la configuración
        model = PerceptronModel(learning_rate=self.learning_rate)
        self.view.print_initial_weights(model.initial_weights)
        
        # Entrenar
        error_history = self.train_perceptron(model, epochs)
        
        # Obtener salidas finales y pesos
        final_outputs = model.forward(self.X)
        final_weights = model.weights.copy()
        
        # Imprimir resultados finales en consola
        self.view.print_results(self.y, final_outputs, final_weights)
        
        # Generar gráfico de error de esta corrida
        plot_path = self.view.plot_errors(error_history, run_index, save_dir)
        
        # Generar gráfico de la frontera de decisión
        self.view.plot_decision_boundary(self.X, self.y, final_weights, run_index, save_dir)
        
        # Retornar datos resumidos para generar el reporte
        run_data = {
            "run_index": run_index,
            "initial_weights": model.initial_weights.flatten().tolist(),
            "final_weights": final_weights.flatten().tolist(),
            "final_outputs": final_outputs.flatten().tolist(),
            "final_mse": float(error_history[-1]),
            "error_history": error_history,
            "plot_path": plot_path
        }
        return run_data

    def run_all_experiments(self, epochs=None, save_dir=None):
        """Ejecuta los 5 experimentos requeridos y recopila las estadísticas."""
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
            
        # Generar gráfica combinada
        combined_plot = self.view.plot_combined_errors(all_errors, save_dir)
        print(f"Gráficas individuales generadas en '{save_dir}'.")
        print(f"Gráfica combinada generada en '{combined_plot}'.")
        
        # Guardar resumen en JSON para fácil carga en el reporte HTML
        summary = []
        for rd in all_runs_data:
            summary.append({
                "run": rd["run_index"],
                "initial_w": rd["initial_weights"],
                "final_w": rd["final_weights"],
                "final_y": rd["final_outputs"],
                "final_mse": rd["final_mse"]
            })
            
        with open(os.path.join(save_dir, "results.json"), "w") as f:
            json.dump(summary, f, indent=4)
            
        print("Resultados de las 5 ejecuciones guardados en 'results.json'.")
