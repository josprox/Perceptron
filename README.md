# Práctica 3: Perceptrón — Sistemas Inteligentes (UNITEC)

Este repositorio contiene la implementación del algoritmo de entrenamiento del **Perceptrón con Retropropagación (Backpropagation)** desde cero en Python, estructurado bajo el patrón de arquitectura **Modelo-Vista-Controlador (MVC)** y desarrollado en consonancia con los principios **SMART**.

El objetivo es entrenar la neurona artificial para clasificar y predecir correctamente el conjunto de datos de entrenamiento provisto en la práctica institucional de la **UNITEC (Clave: SC8121)**, complementado con configuraciones vía entorno y visualización de fronteras de decisión.

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
*   **Tasa de Aprendizaje ($\eta$):** $0.2$ (configurable).
*   **Función de Activación:** Sigmoide ($\phi(z) = \frac{1}{1 + e^{-z}}$).
*   **Épocas de Entrenamiento:** 100,000 iteraciones (configurable).

---

## 🗂️ Estructura del Proyecto

El código está organizado en dos formatos para cumplir tanto con estándares profesionales de desarrollo como con los requisitos académicos de entrega:

### 1. Estructura Modular (MVC Profesional)
*   `requirements.txt`: Especifica las dependencias necesarias (`numpy` y `matplotlib`).
*   `.env`: Archivo de configuración para controlar los parámetros de entrenamiento de forma externa.
*   `model.py`: **Modelo**. Contiene la representación matemática del perceptrón, los pesos, la activación sigmoidal y el gradiente de retropropagación.
*   `view.py`: **Vista**. Maneja la salida por consola y exporta las gráficas de evolución del Error Cuadrático Medio (MSE) y de la frontera de decisión en 2D.
*   `controller.py`: **Controlador**. Coordina el proceso de carga de datos, el archivo `.env`, el ciclo de entrenamiento y la ejecución de las 5 corridas independientes.
*   `main.py`: Punto de entrada del script modular para inicializar y correr todo el experimento.

### 2. Archivos Finales de Entrega
*   `Practica_3_SI_Melchor_Jose.py`: Copia integrada y **autocontenida** del desarrollo modular en un solo archivo con comentarios detallados para la revisión académica.
*   `Practica_3_SI_Melchor_Jose.html`: Reporte interactivo con formato de portada institucional UNITEC, análisis de resultados de 5 corridas a 100k épocas, **gráficas de frontera de decisión en 2D** integradas, y un **simulador interactivo de predicciones en tiempo real**.

---

## ⚙️ Configuración mediante archivo `.env`
Puedes cambiar los parámetros del experimento modificando el archivo local `.env`:
*   `EPOCHS`: Número de iteraciones de entrenamiento (ej. `100000`).
*   `LEARNING_RATE`: Tasa de aprendizaje $\eta$ (ej. `0.2`).
*   `SAVE_DIR`: Directorio de guardado de los resultados (se autodefine como `assets` para mantener el espacio ordenado).
*   `LOG_INTERVAL`: Intervalo de épocas para imprimir el MSE en consola (ej. `10000`).

---

## 📈 Visualizaciones de la Frontera de Decisión (2D, 3D y 4D)

Para comprender geométricamente el espacio de clasificación aprendido por el perceptrón, el script genera visualizaciones en tres dimensionalidades por cada una de las 5 corridas independientes:

1. **Frontera de Decisión en 2D (Plano $X_1 \times X_2$):**
   * Puesto que la tercera entrada es constante ($X_3 = 1$), se visualiza en 2D.
   * La **línea discontinua** representa la frontera lineal de decisión ($z = 0$, donde la probabilidad $\hat{y} = 0.5$).
   * El **fondo sombreado** representa el gradiente de probabilidad de clasificación (Rojo = Clase 0, Azul = Clase 1).
   * Genera los archivos `assets/decision_boundary_run_1.png` a `assets/decision_boundary_run_5.png`.

2. **Frontera de Decisión en 3D (Espacio $X_1 \times X_2 \times X_3$):**
   * El espacio de entradas se modela como un espacio tridimensional.
   * La **superficie translúcida** representa el plano de decisión $W_0 + W_1 X_1 + W_2 X_2 + W_3 X_3 = 0$.
   * Las muestras se ubican como esferas tridimensionales de color según su clase esperada.
   * Genera los archivos `assets/decision_boundary_3d_run_1.png` a `assets/decision_boundary_3d_run_5.png`.

3. **Visualización 4D (Espacio 3D + Gradiente de Probabilidad en Color):**
   * Mapea $X_1, X_2, X_3$ en coordenadas espaciales tridimensionales.
   * La **cuarta dimensión** (la salida probabilística continua $\hat{y}$) se representa como una densa malla de puntos coloreados según su predicción sigmoidal mediante una escala de color divergente.
   * Genera los archivos `assets/decision_boundary_4d_run_1.png` a `assets/decision_boundary_4d_run_5.png`.

---

## 🚀 Instrucciones de Ejecución

### 1. Instalación de Dependencias
Abre tu terminal en la carpeta del proyecto e instala los requerimientos:
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el Experimento Modular
```bash
python main.py
```

### 3. Ejecutar el Script de Entrega
```bash
python Practica_3_SI_Melchor_Jose.py
```

Ambos scripts realizarán el entrenamiento de 100,000 épocas por cada una de las 5 corridas y generarán dentro de la carpeta `assets/`:
1.  Gráficos individuales de error: `assets/error_curve_run_1.png` a `assets/error_curve_run_5.png`.
2.  Gráficos de frontera de decisión en 2D, 3D y 4D por cada corrida (por ejemplo, `assets/decision_boundary_run_1.png`, `assets/decision_boundary_3d_run_1.png`, `assets/decision_boundary_4d_run_1.png`).
3.  Un gráfico de error consolidado: `assets/error_curve_combined.png`.
4.  El archivo `assets/results.json` con las matrices de pesos y resultados históricos de las ejecuciones.

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
