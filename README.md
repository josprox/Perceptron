# Práctica 3: Perceptrón — Sistemas Inteligentes (UNITEC)

Este repositorio contiene la implementación del algoritmo de entrenamiento del **Perceptrón con Retropropagación (Backpropagation)** desde cero en Python, estructurado bajo el patrón de arquitectura **Modelo-Vista-Controlador (MVC)** y desarrollado en consonancia con los principios **SMART**.

El objetivo es entrenar la neurona artificial para clasificar y predecir correctamente el conjunto de datos de entrenamiento provisto en la práctica institucional de la **UNITEC (Clave: SC8121)**.

---

## 👥 Datos del Alumno
*   **Nombre:** José Melchor
*   **Matrícula:** 336009446
*   **Materia:** Sistemas Inteligentes
*   **Fecha de Entrega:** 15 de Junio de 2026

---

## 📊 Especificación del Problema

El conjunto de datos de entrenamiento cuenta con 3 variables de entrada y una salida esperada binaria:

| Muestra | Entrada $X_1$ | Entrada $X_2$ | Entrada $X_3$ | Salida Esperada ($Y$) |
| :---: | :---: | :---: | :---: | :---: |
|   a   |       0       |       0       |       1       |           0           |
|   b   |       1       |       1       |       1       |           1           |
|   c   |       1       |       0       |       1       |           1           |
|   d   |       0       |       1       |       1       |           0           |

### Hiperparámetros de Entrenamiento:
*   **Sesgo (Bias):** $X_0 = 1$ asociado al peso $W_0$.
*   **Pesos Iniciales:** Propuestos de manera aleatoria en el rango $[-1.0, 1.0]$.
*   **Tasa de Aprendizaje ($\eta$):** $0.2$.
*   **Función de Activación:** Sigmoide ($\phi(z) = \frac{1}{1 + e^{-z}}$).
*   **Épocas de Entrenamiento:** 100,000 iteraciones.

---

## 🗂️ Estructura del Proyecto

El código está organizado en dos formatos para cumplir tanto con estándares profesionales de desarrollo como con los requisitos académicos de entrega:

### 1. Estructura Modular (MVC Profesional)
*   `requirements.txt`: Especifica las dependencias necesarias (`numpy` y `matplotlib`).
*   `model.py`: **Modelo**. Contiene la representación matemática del perceptrón, los pesos, la activación sigmoidal y el gradiente de retropropagación.
*   `view.py`: **Vista**. Maneja la salida por consola y exporta las gráficas de evolución del Error Cuadrático Medio (MSE).
*   `controller.py`: **Controlador**. Coordina el proceso de carga de datos, el ciclo de entrenamiento y la ejecución de las 5 corridas independientes.
*   `main.py`: Punto de entrada del script modular para inicializar y correr todo el experimento.

### 2. Archivos Finales de Entrega
*   `Practica_3_SI_Melchor_Jose.py`: Copia integrada y **autocontenida** del desarrollo modular en un solo archivo con comentarios detallados para la revisión académica.
*   `Practica_3_SI_Melchor_Jose.html`: Reporte interactivo con formato de portada institucional UNITEC, análisis de resultados de 5 corridas, diagrama de flujo en Mermaid y un **simulador interactivo de predicciones en tiempo real**.

---

## 🚀 Instrucciones de Configuración y Ejecución

### Requisitos Previos
Asegúrate de contar con Python 3.8 o superior instalado en tu equipo.

### 1. Instalación de Dependencias
Abre tu terminal en la carpeta del proyecto e instala los requerimientos necesarios:
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el Experimento Modular
Para iniciar el ciclo de entrenamiento modularizado de 5 ejecuciones independientes:
```bash
python main.py
```

### 3. Ejecutar el Script de Entrega
Para validar de forma independiente el script entregable en un solo archivo:
```bash
python Practica_3_SI_Melchor_Jose.py
```

Ambos scripts realizarán el entrenamiento de 100,000 épocas por cada una de las 5 corridas y generarán:
1.  Gráficos individuales de error: `error_curve_run_1.png` a `error_curve_run_5.png`.
2.  Un gráfico de error consolidado: `error_curve_combined.png`.
3.  El archivo `results.json` con las matrices de pesos y resultados históricos de las ejecuciones.

---

## 📄 Instrucciones para Generar el PDF Académico

El archivo HTML generado está diseñado para ser responsivo e interactivo en pantalla (con modo oscuro y simulador), pero cuenta con estilos específicos de impresión que eliminan los controles web y expanden las tablas en un formato de reporte de laboratorio formal en blanco y negro.

1.  Abre [Practica_3_SI_Melchor_Jose.html](./Practica_3_SI_Melchor_Jose.html) en tu navegador web.
2.  Presiona **`Ctrl + P`** en Windows (o haz clic en el botón flotante **"Guardar como PDF / Imprimir"** en la parte superior derecha).
3.  En la ventana de impresión, selecciona:
    *   **Destino:** Guardar como PDF.
    *   **Páginas:** Todo.
    *   **Más opciones de configuración:** Habilita la casilla de **"Gráficos de fondo"** (indispensable para conservar el color de los bordes y las tablas institucionales).
4.  Haz clic en **Guardar** con la nomenclatura: `Practica_3_SI_Melchor_Jose.pdf`.
