"""
Sistemas Inteligentes - Práctica 3: Perceptrón
Vista (View) - Arquitectura MVC
Autor: José Melchor
Matrícula: 336009446
Fecha de entrega: 15/06/2026

Este módulo define la clase PerceptronView, la cual se encarga de la interfaz con
el usuario, incluyendo la visualización en consola de los resultados de entrenamiento,
los pesos, la generación de gráficas de error (MSE vs Épocas), la frontera de decisión en 2D,
la frontera en 3D y la visualización 4D utilizando gradientes de color.
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
        Dado que X3 = 1 es constante, la visualización en 2D representa la proyección del espacio.
        """
        plt.figure(figsize=(7, 6))
        
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
        
        contour = plt.contourf(xx, yy, grid_predictions, levels=50, cmap='RdBu', alpha=0.25)
        cbar = plt.colorbar(contour)
        cbar.set_label('Probabilidad de Predicción ($\hat{y}$)', fontsize=10)
        
        plt.contour(xx, yy, grid_predictions, levels=[0.5], colors='#1e3d59', linestyles='--', linewidths=2.5)
        
        # Graficar las muestras de entrenamiento reales
        for i in range(len(y)):
            x1 = X[i, 1]
            x2 = X[i, 2]
            target = y[i, 0]
            color = '#17b978' if target == 1.0 else '#ff6e40'
            label = 'Clase 1 (Y=1)' if target == 1.0 else 'Clase 0 (Y=0)'
            plt.scatter(x1, x2, color=color, s=160, edgecolors='black', linewidths=1.5, zorder=5, 
                        label=label if i < 2 else "")
            
            plt.annotate(f"({int(x1)}, {int(x2)})", (x1 + 0.05, x2 + 0.05), fontsize=9, fontweight='bold', zorder=6)
            
        plt.title(f'Frontera de Decisión 2D - Ejecución {run_index}', fontsize=12, fontweight='bold', pad=15)
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

    @staticmethod
    def plot_decision_boundary_3d(X, y, weights, run_index, save_dir="."):
        """
        Genera y guarda la gráfica de la frontera de decisión en 3D (X1, X2, X3).
        El plano de decisión se dibuja como una superficie 3D: W0 + W1*X1 + W2*X2 + W3*X3 = 0
        """
        fig = plt.figure(figsize=(8, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        # Graficar muestras de entrenamiento
        for i in range(len(y)):
            x1 = X[i, 1]
            x2 = X[i, 2]
            x3 = X[i, 3]
            target = y[i, 0]
            color = '#17b978' if target == 1.0 else '#ff6e40'
            label = 'Clase 1 (Y=1)' if target == 1.0 else 'Clase 0 (Y=0)'
            ax.scatter(x1, x2, x3, color=color, s=180, edgecolors='black', linewidths=1.5, zorder=5,
                       label=label if i < 2 else "")
            ax.text(x1, x2, x3 + 0.05, f"({int(x1)}, {int(x2)}, {int(x3)})", fontsize=8, fontweight='bold')

        # Dibujar el plano de decisión: W0 + W1*X1 + W2*X2 + W3*X3 = 0
        # => X3 = -(W1*X1 + W2*X2 + W0) / W3
        w0, w1, w2, w3 = weights.flatten()
        
        x1_grid = np.linspace(-0.5, 1.5, 30)
        x2_grid = np.linspace(-0.5, 1.5, 30)
        x1_mesh, x2_mesh = np.meshgrid(x1_grid, x2_grid)
        
        if np.abs(w3) > 1e-5:
            x3_mesh = -(w1 * x1_mesh + w2 * x2_mesh + w0) / w3
            # Recortar plano para que se vea dentro del rango
            x3_mesh[x3_mesh < -0.5] = np.nan
            x3_mesh[x3_mesh > 1.5] = np.nan
            
            # Graficar la superficie
            ax.plot_surface(x1_mesh, x2_mesh, x3_mesh, alpha=0.3, cmap='coolwarm', edgecolor='none')
        
        ax.set_title(f'Frontera de Decisión 3D - Ejecución {run_index}', fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel('Entrada X1')
        ax.set_ylabel('Entrada X2')
        ax.set_zlabel('Entrada X3')
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 1.5)
        ax.set_zlim(-0.5, 1.5)
        ax.legend(loc='upper left')
        plt.tight_layout()
        
        filename = os.path.join(save_dir, f"decision_boundary_3d_run_{run_index}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        return filename

    @staticmethod
    def plot_decision_boundary_4d(X, y, weights, run_index, save_dir="."):
        """
        Visualiza el espacio de 4 dimensiones mapeando X1, X2, X3 como coordenadas 3D,
        y la predicción de salida y_hat (4ta dimensión) como el color de los puntos en el espacio.
        """
        fig = plt.figure(figsize=(8, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        # Generar una rejilla fina de puntos en el espacio 3D (X1, X2, X3)
        x1_vals = np.linspace(-0.3, 1.3, 12)
        x2_vals = np.linspace(-0.3, 1.3, 12)
        x3_vals = np.linspace(-0.3, 1.3, 12)
        x1_mesh, x2_mesh, x3_mesh = np.meshgrid(x1_vals, x2_vals, x3_vals)
        
        # Preparar entrada [Bias=1, X1, X2, X3]
        grid_input = np.c_[np.ones(x1_mesh.ravel().shape),
                           x1_mesh.ravel(),
                           x2_mesh.ravel(),
                           x3_mesh.ravel()]
        
        # Calcular predicciones
        z = np.dot(grid_input, weights)
        y_hat = 1.0 / (1.0 + np.exp(-z))
        
        # Graficar la rejilla de puntos 3D coloreados por su predicción y_hat (4D)
        sc = ax.scatter(x1_mesh.ravel(), x2_mesh.ravel(), x3_mesh.ravel(), 
                        c=y_hat, cmap='RdBu', alpha=0.15, s=25, edgecolors='none')
        
        # Graficar las muestras de entrenamiento reales con mayor opacidad
        for i in range(len(y)):
            x1 = X[i, 1]
            x2 = X[i, 2]
            x3 = X[i, 3]
            target = y[i, 0]
            color = '#17b978' if target == 1.0 else '#ff6e40'
            label = 'Clase 1 (Y=1)' if target == 1.0 else 'Clase 0 (Y=0)'
            ax.scatter(x1, x2, x3, color=color, s=200, edgecolors='black', linewidths=1.5, zorder=5,
                       label=label if i < 2 else "")
            ax.text(x1, x2, x3 + 0.05, f"({int(x1)}, {int(x2)}, {int(x3)})", fontsize=8, fontweight='bold')
            
        cbar = fig.colorbar(sc, ax=ax, pad=0.1)
        cbar.set_label('Predicción de Salida $\hat{y}$ (4ta Dimensión - Color)', fontsize=10)
        
        ax.set_title(f'Visualización 4D (Espacio + Color) - Ejecución {run_index}', fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel('Entrada X1')
        ax.set_ylabel('Entrada X2')
        ax.set_zlabel('Entrada X3')
        ax.set_xlim(-0.4, 1.4)
        ax.set_ylim(-0.4, 1.4)
        ax.set_zlim(-0.4, 1.4)
        ax.legend(loc='upper left')
        plt.tight_layout()
        
        filename = os.path.join(save_dir, f"decision_boundary_4d_run_{run_index}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        return filename
