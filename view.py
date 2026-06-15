"""
Sistemas Inteligentes - Práctica 3: Perceptrón
Vista (View) - Arquitectura MVC
Autor: José Melchor
Matrícula: 336009446
Fecha de entrega: 15/06/2026

Este módulo define la clase PerceptronView, la cual se encarga de la interfaz con
el usuario, incluyendo la visualización en consola de los resultados de entrenamiento,
los pesos, la generación de gráficas de error (MSE vs Épocas) y de la frontera de decisión en 2D.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

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
        plt.plot(run_errors, label=f'MSE (Corrida {run_index})', color='#1e3d59', linewidth=2)
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
        plt.yscale('log')  # Escala logarítmica para ver mejor la convergencia rápida
        plt.grid(True, which="both", linestyle='--', alpha=0.5)
        plt.legend(fontsize=10)
        plt.tight_layout()
        
        filename = os.path.join(save_dir, "error_curve_combined.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        return filename

    @staticmethod
    def plot_decision_boundary(X, y, weights, run_index, save_dir="."):
        """
        Genera y guarda la gráfica de la frontera de decisión en 2D (X1 y X2).
        Dado que X3 = 1 es constante, la visualización en 2D representa fielmente el espacio de entrada.
        """
        plt.figure(figsize=(7, 6))
        
        # Crear una malla fina para pintar los fondos de las regiones de decisión
        x_min, x_max = -0.5, 1.5
        y_min, y_max = -0.5, 1.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                             np.linspace(y_min, y_max, 200))
        
        # Preparar la entrada para la malla de prueba [Bias=1, X1, X2, X3=1]
        grid_input = np.c_[np.ones(xx.ravel().shape), 
                           xx.ravel(), 
                           yy.ravel(), 
                           np.ones(xx.ravel().shape)]
        
        # Calcular las predicciones probabilísticas de la sigmoide para toda la malla
        z = np.dot(grid_input, weights)
        grid_predictions = 1.0 / (1.0 + np.exp(-z))
        grid_predictions = grid_predictions.reshape(xx.shape)
        
        # Dibujar regiones coloreadas (heatmap de probabilidad suave)
        contour = plt.contourf(xx, yy, grid_predictions, levels=50, cmap='RdBu', alpha=0.25)
        cbar = plt.colorbar(contour)
        cbar.set_label('Probabilidad de Predicción ($\hat{y}$)', fontsize=10)
        
        # Dibujar la línea de la frontera de decisión (donde la predicción es exactamente 0.5)
        plt.contour(xx, yy, grid_predictions, levels=[0.5], colors='#1e3d59', linestyles='--', linewidths=2.5)
        
        # Graficar las muestras de entrenamiento con colores para sus clases
        for i in range(len(y)):
            x1 = X[i, 1]
            x2 = X[i, 2]
            target = y[i, 0]
            color = '#17b978' if target == 1.0 else '#ff6e40'
            label = 'Clase 1 (Y=1)' if target == 1.0 else 'Clase 0 (Y=0)'
            plt.scatter(x1, x2, color=color, s=160, edgecolors='black', linewidths=1.5, zorder=5, 
                        label=label if i < 2 else "")  # Evitar duplicar etiquetas en la leyenda
            
            # Anotar las coordenadas en la gráfica
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
