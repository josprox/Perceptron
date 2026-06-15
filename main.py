"""
Sistemas Inteligentes - Práctica 3: Perceptrón
Punto de Entrada (Entry Point) - Arquitectura MVC
Autor: José Melchor
Matrícula: 336009446
Fecha de entrega: 15/06/2026

Este script sirve como punto de entrada para ejecutar el experimento de 5 ejecuciones
del perceptrón entrenado con retropropagación. Utiliza la configuración cargada desde el archivo .env.
"""

import os
from controller import PerceptronController

if __name__ == "__main__":
    # Inicializar controlador (carga la configuración desde .env de forma automática)
    controller = PerceptronController()
    
    # Asegurar que la carpeta de destino especificada en .env existe
    os.makedirs(controller.save_dir, exist_ok=True)
    
    # Ejecutar experimentos utilizando los parámetros del entorno
    controller.run_all_experiments()
