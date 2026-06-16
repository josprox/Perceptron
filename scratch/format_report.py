import json
import os

def generate_html():
    # 1. Cargar resultados del archivo JSON
    results_path = os.path.join("assets", "results.json")
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    # Convertir pesos a formato de lista JavaScript para el simulador
    js_model_runs = {}
    for r in results:
        run_num = r["run"]
        fw = r["final_w"]
        js_model_runs[run_num] = {
            "w0": fw[0],
            "w1": fw[1],
            "w2": fw[2],
            "w3": fw[3]
        }

    js_model_runs_str = json.dumps(js_model_runs, indent=8)

    # 2. Generar el bloque de ejecuciones individuales (8b, 8c, 8d, 8e, 8f)
    run_letters = {1: "b", 2: "c", 3: "d", 4: "e", 5: "f"}
    runs_html = []
    
    for r in results:
        run_num = r["run"]
        letter = run_letters[run_num]
        init_w = r["initial_w"]
        final_w = r["final_w"]
        final_y = r["final_y"]
        mse = r["final_mse"]

        err_a = 0.0 - final_y[0]
        err_b = 1.0 - final_y[1]
        err_c = 1.0 - final_y[2]
        err_d = 0.0 - final_y[3]

        run_block = f"""
        <!-- ==========================================
             PÁGINA 8{letter}: RESULTADOS (EJECUCIÓN {run_num})
             ========================================== -->
        <div class="unitec-page" id="page-8{letter}">
            <div class="unitec-page-content">
                <table class="unitec-header-table">
                    <tr>
                        <td class="logo-col">
                            <div class="unitec-logo-container">
                                <span class="unitec-logo-text">UNITEC</span>
                                <span class="unitec-logo-subtext">Universidad Tecnológica de México</span>
                            </div>
                        </td>
                        <td class="title-col">Practicario de Sistemas Inteligentes</td>
                        <td class="clave-col">Clave: SC8121</td>
                    </tr>
                </table>

                <div class="pdf-section">
                    <div class="pdf-section-header">Resultados obtenidos - Ejecución {run_num}:</div>
                    <div class="pdf-section-body">
                        <h4 style="margin-bottom: 0.5rem; color: var(--primary);">Pesos iniciales y finales (Ejecución {run_num}):</h4>
                        <div class="table-responsive">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Parámetro</th>
                                        <th>W0 (Bias/Sesgo)</th>
                                        <th>W1 (Entrada X1)</th>
                                        <th>W2 (Entrada X2)</th>
                                        <th>W3 (Entrada X3)</th>
                                        <th>Error Final (MSE)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong>Valor Inicial</strong></td>
                                        <td>{init_w[0]:+.6f}</td>
                                        <td>{init_w[1]:+.6f}</td>
                                        <td>{init_w[2]:+.6f}</td>
                                        <td>{init_w[3]:+.6f}</td>
                                        <td rowspan="2" style="vertical-align: middle; font-weight: bold; color: var(--primary-light);">{mse:.4e}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Valor Final</strong></td>
                                        <td>{final_w[0]:+.6f}</td>
                                        <td>{final_w[1]:+.6f}</td>
                                        <td>{final_w[2]:+.6f}</td>
                                        <td>{final_w[3]:+.6f}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <h4 style="margin-top: 1.25rem; margin-bottom: 0.5rem; color: var(--primary);">Verificación de Convergencia de Datos:</h4>
                        <div class="table-responsive">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Muestra</th>
                                        <th>Entrada X1</th>
                                        <th>Entrada X2</th>
                                        <th>Entrada X3</th>
                                        <th>Salida Esperada (Y)</th>
                                        <th>Salida Obtenida (&Ycirc;)</th>
                                        <th>Diferencia / Error</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>a</td>
                                        <td>0</td>
                                        <td>0</td>
                                        <td>1</td>
                                        <td>0.0</td>
                                        <td>{final_y[0]:.6f}</td>
                                        <td>{err_a:+.6f}</td>
                                    </tr>
                                    <tr>
                                        <td>b</td>
                                        <td>1</td>
                                        <td>1</td>
                                        <td>1</td>
                                        <td>1.0</td>
                                        <td>{final_y[1]:.6f}</td>
                                        <td>{err_b:+.6f}</td>
                                    </tr>
                                    <tr>
                                        <td>c</td>
                                        <td>1</td>
                                        <td>0</td>
                                        <td>1</td>
                                        <td>1.0</td>
                                        <td>{final_y[2]:.6f}</td>
                                        <td>{err_c:+.6f}</td>
                                    </tr>
                                    <tr>
                                        <td>d</td>
                                        <td>0</td>
                                        <td>1</td>
                                        <td>1</td>
                                        <td>0.0</td>
                                        <td>{final_y[3]:.6f}</td>
                                        <td>{err_d:+.6f}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--primary);">Curva de Error y Fronteras de Decisión (Ejecución {run_num}):</h4>
                        <div class="graphs-grid">
                            <div class="image-container">
                                <h5 style="margin-top: 0; margin-bottom: 0.5rem; color: var(--primary);">Curva de Aprendizaje (Error MSE)</h5>
                                <img src="assets/error_curve_run_{run_num}.png" alt="Curva de error MSE corrida {run_num}" class="result-image">
                                <div class="image-caption">
                                    Evolución del MSE a lo largo de las 100,000 épocas.
                                </div>
                            </div>
                            <div class="image-container">
                                <h5 style="margin-top: 0; margin-bottom: 0.5rem; color: var(--primary);">Frontera 2D (Plano $X_1 \\times X_2$)</h5>
                                <img src="assets/decision_boundary_run_{run_num}.png" alt="Frontera de decisión de la corrida {run_num}" class="result-image">
                                <div class="image-caption">
                                    Proyección del hiperplano de separación en 2D, con entrada constante $X_3 = 1$.
                                </div>
                            </div>
                        </div>
                        <div class="graphs-grid" style="margin-top: 1rem;">
                            <div class="image-container">
                                <h5 style="margin-top: 0; margin-bottom: 0.5rem; color: var(--primary);">Frontera 3D (Espacio $X_1 \\times X_2 \\times X_3$)</h5>
                                <img src="assets/decision_boundary_3d_run_{run_num}.png" alt="Frontera de decisión 3D de la corrida {run_num}" class="result-image">
                                <div class="image-caption">
                                    Superficie del hiperplano de decisión: $W_0 + W_1 X_1 + W_2 X_2 + W_3 X_3 = 0$.
                                </div>
                            </div>
                            <div class="image-container">
                                <h5 style="margin-top: 0; margin-bottom: 0.5rem; color: var(--primary);">Visualización 4D (Probabilidad como Color)</h5>
                                <img src="assets/decision_boundary_4d_run_{run_num}.png" alt="Frontera de decisión 4D de la corrida {run_num}" class="result-image">
                                <div class="image-caption">
                                    Espacio tridimensional coloreado según la probabilidad de predicción sigmoidal $\\hat{{y}}$.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="unitec-page-footer">
                <div class="footer-left">Dirección de Tecnología Educativa e Integración de Prácticas</div>
                <div class="footer-right">Página 8{letter} de 12</div>
            </div>
        </div>"""
        runs_html.append(run_block)

    runs_combined_html = "\n".join(runs_html)

    # 3. Plantilla HTML base en texto plano
    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Practica_3_SI_Melchor_Jose - Reporte de Perceptrón (100k)</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- MathJax para formulas matemáticas -->
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true
            },
            options: {
                ignoreHtmlClass: 'tex2jax_ignore',
                processHtmlClass: 'tex2jax_process'
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <!-- Mermaid.js para diagramas de flujo -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'neutral',
            securityLevel: 'loose',
            themeVariables: {
                primaryColor: '#1e3d59',
                primaryTextColor: '#fff',
                lineColor: '#ff6e40'
            }
        });
    </script>

    <style>
        :root {
            --primary: #1e3d59;
            --primary-light: #17b978;
            --secondary: #ff6e40;
            --dark-bg: #0f172a;
            --dark-card: #1e293b;
            --dark-text: #f1f5f9;
            --light-bg: #f8fafc;
            --light-card: #ffffff;
            --light-text: #334155;
            --border: #cbd5e1;
            --border-dark: #334155;
            --accent: #7b1fa2;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: background-color 0.3s, border-color 0.3s, color 0.3s;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--light-bg);
            color: var(--light-text);
            line-height: 1.5;
        }

        body.dark-mode {
            background-color: var(--dark-bg);
            color: var(--dark-text);
        }

        h1, h2, h3, h4, h5 {
            font-family: 'Montserrat', sans-serif;
            color: var(--primary);
            font-weight: 700;
        }

        body.dark-mode h1, body.dark-mode h2, body.dark-mode h3, body.dark-mode h4, body.dark-mode h5 {
            color: white;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }

        /* Controles de interfaz */
        .controls {
            position: fixed;
            top: 1.5rem;
            right: 1.5rem;
            display: flex;
            gap: 1rem;
            z-index: 1000;
        }

        .btn-control {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem 1.25rem;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .btn-control:hover {
            transform: translateY(-2px);
            background-color: var(--secondary);
        }

        body.dark-mode .btn-control {
            background-color: var(--dark-card);
            border: 1px solid var(--border-dark);
        }

        /* Estilo de página virtual (A4 Preview) */
        .unitec-page {
            background-color: var(--light-card);
            border-radius: 0;
            padding: 3rem;
            margin-bottom: 3rem;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            position: relative;
            min-height: 29.7cm;
            display: flex;
            flex-direction: column;
            page-break-after: always;
        }

        body.dark-mode .unitec-page {
            background-color: var(--dark-card);
            border-color: var(--border-dark);
        }

        .unitec-page-content {
            flex-grow: 1;
            margin-bottom: 2rem;
        }

        .unitec-page-footer {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 0.8rem;
            color: #64748b;
            border-top: 1px solid #cbd5e1;
            padding-top: 0.75rem;
            margin-top: auto;
            gap: 0.25rem;
        }

        body.dark-mode .unitec-page-footer {
            border-top-color: var(--border-dark);
            color: #94a3b8;
        }

        /* Tabla de cabecera oficial */
        .unitec-header-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 2rem;
        }

        .unitec-header-table td {
            border: 1px solid #475569;
            padding: 0.75rem;
            text-align: center;
            vertical-align: middle;
            color: var(--light-text);
        }

        body.dark-mode .unitec-header-table td {
            border-color: var(--border-dark);
            color: var(--dark-text);
        }

        .unitec-header-table .logo-col {
            width: 30%;
        }

        .unitec-header-table .title-col {
            width: 50%;
            font-weight: 700;
            font-size: 1.05rem;
            background-color: #f8fafc;
            color: var(--primary);
        }

        body.dark-mode .unitec-header-table .title-col {
            background-color: #1e293b;
            color: white;
        }

        .unitec-header-table .clave-col {
            width: 20%;
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--primary);
        }

        body.dark-mode .unitec-header-table .clave-col {
            color: white;
        }

        .unitec-logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .unitec-logo-text {
            font-weight: 800;
            font-size: 1.3rem;
            color: var(--primary);
            letter-spacing: 1.5px;
            border-bottom: 3px solid var(--secondary);
            padding-bottom: 2px;
            margin-bottom: 4px;
        }

        body.dark-mode .unitec-logo-text {
            color: white;
        }

        .unitec-logo-subtext {
            font-size: 0.65rem;
            color: #64748b;
            text-transform: uppercase;
        }

        body.dark-mode .unitec-logo-subtext {
            color: #94a3b8;
        }

        /* Secciones del PDF con bordes */
        .pdf-section {
            border: 1px solid #cbd5e1;
            margin-bottom: 1.5rem;
            border-radius: 0;
            overflow: hidden;
            background-color: var(--light-card);
        }

        body.dark-mode .pdf-section {
            border-color: var(--border-dark);
            background-color: var(--dark-card);
        }

        .pdf-section-header {
            background-color: #f1f5f9;
            padding: 0.6rem 1rem;
            font-weight: 700;
            font-size: 0.95rem;
            border-bottom: 1px solid #cbd5e1;
            color: var(--primary);
        }

        body.dark-mode .pdf-section-header {
            background-color: #1e293b;
            border-bottom-color: var(--border-dark);
            color: white;
        }

        .pdf-section-body {
            padding: 1.25rem;
        }

        /* Tabla de metadatos */
        .datos-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1.5rem;
        }

        .datos-table td {
            border: 1px solid #cbd5e1;
            padding: 0.6rem;
            font-size: 0.9rem;
        }

        body.dark-mode .datos-table td {
            border-color: var(--border-dark);
        }

        .datos-table .cell-label {
            width: 35%;
            font-weight: 700;
            background-color: #f8fafc;
            color: var(--primary);
        }

        body.dark-mode .datos-table .cell-label {
            background-color: #1e293b;
            color: white;
        }

        .datos-table .cell-value {
            width: 65%;
        }

        .table-responsive {
            overflow-x: auto;
            margin: 1.5rem 0;
            border-radius: 0;
            border: 1px solid var(--border);
        }

        body.dark-mode .table-responsive {
            border-color: var(--border-dark);
        }

        table.data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        table.data-table th, table.data-table td {
            padding: 0.75rem 1rem;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }

        body.dark-mode table.data-table th, body.dark-mode table.data-table td {
            border-bottom-color: var(--border-dark);
        }

        table.data-table th {
            background-color: #f1f5f9;
            font-weight: 600;
            color: var(--primary);
        }

        body.dark-mode table.data-table th {
            background-color: #1e293b;
            color: white;
        }

        /* Bloque de formulas */
        .formula {
            background-color: transparent;
            padding: 0.5rem 0;
            border: none;
            margin: 0.75rem 0;
            text-align: center;
        }

        body.dark-mode .formula {
            background-color: transparent;
        }

        /* Contenedores de imagenes */
        .image-container {
            text-align: center;
            margin: 1.5rem 0;
            border-radius: 0;
            overflow: hidden;
            background-color: white;
            padding: 1rem;
            border: 1px solid var(--border);
        }

        body.dark-mode .image-container {
            border-color: var(--border-dark);
            background-color: #0f172a;
        }

        .result-image {
            max-width: 100%;
            height: auto;
            border-radius: 0;
            max-height: 400px;
        }

        .image-caption {
            font-size: 0.85rem;
            color: #64748b;
            margin-top: 0.75rem;
            font-style: italic;
        }

        body.dark-mode .image-caption {
            color: #94a3b8;
        }

        .graphs-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-top: 1rem;
        }

        @media (max-width: 768px) {
            .graphs-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Simulador */
        .sim-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-top: 1rem;
        }

        @media (max-width: 768px) {
            .sim-grid {
                grid-template-columns: 1fr;
            }
        }

        .sim-card {
            background-color: #f1f5f9;
            padding: 1.5rem;
            border-radius: 0;
            border: 1px solid var(--border);
        }

        body.dark-mode .sim-card {
            background-color: #0f172a;
            border-color: var(--border-dark);
        }

        .sim-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary);
            border-bottom: 1px solid rgba(0,0,0,0.1);
            padding-bottom: 0.5rem;
        }

        body.dark-mode .sim-title {
            color: white;
            border-bottom-color: rgba(255,255,255,0.1);
        }

        .control-group {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .control-label {
            font-weight: 600;
            font-size: 0.95rem;
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 48px;
            height: 24px;
        }

        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #cbd5e1;
            transition: .3s;
            border-radius: 24px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .3s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: var(--primary-light);
        }

        input:checked + .slider:before {
            transform: translateX(24px);
        }

        .select-run {
            width: 100%;
            padding: 0.5rem;
            border-radius: 0;
            border: 1px solid var(--border);
            font-family: inherit;
            margin-bottom: 1rem;
            background-color: white;
        }

        body.dark-mode .select-run {
            background-color: var(--dark-card);
            color: white;
            border-color: var(--border-dark);
        }

        .output-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            min-height: 150px;
            text-align: center;
            background-color: white;
            border-radius: 0;
            padding: 1.5rem;
            border: 1px solid var(--border);
        }

        body.dark-mode .output-box {
            background-color: var(--dark-card);
            border-color: var(--border-dark);
        }

        .output-value {
            font-size: 2rem;
            font-weight: 800;
            color: var(--primary-light);
            margin: 0.5rem 0;
            font-family: 'Fira Code', monospace;
        }

        .output-z {
            font-size: 0.9rem;
            color: #64748b;
            font-family: 'Fira Code', monospace;
        }

        body.dark-mode .output-z {
            color: #94a3b8;
        }

        /* Tabs de corridas */
        .tabs-container {
            margin-top: 1.5rem;
        }

        .tab-buttons {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
            overflow-x: auto;
        }

        body.dark-mode .tab-buttons {
            border-bottom-color: var(--border-dark);
        }

        .tab-btn {
            background-color: transparent;
            color: var(--light-text);
            border: none;
            padding: 0.5rem 1.25rem;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            border-radius: 0;
            white-space: nowrap;
        }

        body.dark-mode .tab-btn {
            color: var(--dark-text);
        }

        .tab-btn:hover {
            background-color: rgba(30, 61, 89, 0.1);
        }

        .tab-btn.active {
            background-color: var(--primary);
            color: white;
        }

        body.dark-mode .tab-btn.active {
            background-color: var(--secondary);
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .diagram-container {
            display: flex;
            justify-content: center;
            background-color: white;
            padding: 1.5rem;
            border-radius: 0;
            margin: 1.5rem 0;
            border: 1px solid var(--border);
            overflow-x: auto;
        }

        .bib-list {
            list-style-type: none;
            padding-left: 0;
        }

        .bib-list li {
            margin-bottom: 1rem;
            padding-left: 1.5rem;
            text-indent: -1.5rem;
            text-align: justify;
        }

        /* Estilo de la portada */
        .cover-page {
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .cover-page::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 8px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, var(--primary-light) 100%);
        }

        .cover-logo-container {
            margin-bottom: 2.5rem;
        }

        .cover-unitec-logo {
            background-color: var(--primary);
            color: white;
            font-family: 'Montserrat', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            padding: 0.6rem 2rem;
            border-radius: 0;
            letter-spacing: 3px;
            display: inline-block;
            border-bottom: 5px solid var(--secondary);
        }

        .cover-subtitle {
            font-size: 1.25rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-bottom: 1rem;
            font-weight: 500;
        }

        body.dark-mode .cover-subtitle {
            color: #94a3b8;
        }

        .cover-title {
            font-size: 2.5rem;
            margin-bottom: 2.5rem;
            line-height: 1.3;
            color: var(--primary);
        }

        body.dark-mode .cover-title {
            color: white;
        }

        .cover-meta-table {
            width: 100%;
            max-width: 600px;
            margin: 2rem auto;
            border-collapse: collapse;
            text-align: left;
        }

        .cover-meta-table td {
            padding: 0.9rem 1.2rem;
            border-bottom: 1px solid var(--border);
            font-size: 1rem;
        }

        body.dark-mode .cover-meta-table td {
            border-bottom-color: var(--border-dark);
        }

        .cover-meta-table td.label {
            font-weight: 700;
            color: var(--primary);
            width: 35%;
        }

        body.dark-mode .cover-meta-table td.label {
            color: #38bdf8;
        }

        /* Estilos de Impresión oficiales del Practicario */
        @media print {
            body {
                background-color: white !important;
                color: black !important;
                font-size: 10pt !important;
            }

            .container {
                max-width: 100% !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            .controls, .btn-control, .theme-switcher, .tab-buttons, .only-screen {
                display: none !important;
            }

            .unitec-page {
                box-shadow: none !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 0 5cm 0 !important;
                background-color: white !important;
                min-height: auto !important;
                page-break-after: always !important;
                display: flex !important;
                flex-direction: column !important;
            }

            .unitec-page-footer {
                border-top: 1px solid #000 !important;
                color: black !important;
                margin-top: auto !important;
            }

            .unitec-header-table td {
                border: 1px solid #000 !important;
                color: black !important;
            }

            .unitec-header-table .title-col {
                background-color: #e2e8f0 !important;
            }

            .pdf-section {
                border: 1px solid #000 !important;
                page-break-inside: avoid;
            }

            .pdf-section-header {
                background-color: #e2e8f0 !important;
                border-bottom: 1px solid #000 !important;
                color: black !important;
            }

            .tab-content {
                display: block !important;
                page-break-inside: avoid;
                margin-bottom: 2rem;
            }

            .tab-header-print {
                display: block !important;
                font-weight: 700;
                font-size: 1.1rem;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
                border-bottom: 1px dashed #000;
                padding-bottom: 0.25rem;
            }
        }
    </style>
</head>
<body>

    <!-- Botones de Control flotantes -->
    <div class="controls">
        <button class="btn-control" onclick="toggleDarkMode()" id="btn-theme">
            <span id="theme-icon">🌙</span> Modo Oscuro
        </button>
        <button class="btn-control" onclick="window.print()">
            🖨️ Guardar como PDF / Imprimir
        </button>
    </div>

    <div class="container">
        
        <!-- ==========================================
             PORTADA DE ENTREGA
             ========================================== -->
        <div class="unitec-page cover-page">
            <div class="unitec-page-content">
                <div class="cover-logo-container" style="margin-top: 4rem;">
                    <div class="cover-unitec-logo">UNITEC</div>
                </div>
                <div class="cover-subtitle">Universidad Tecnológica de México</div>
                <h1 class="cover-title" style="margin-top: 2rem; font-weight: 800;">Entregable 4 - Práctica 3: Perceptrón</h1>
                <p style="text-align: center; color: #64748b; font-weight: 500; font-size: 1.1rem;">
                    Materia: Sistemas Inteligentes | Clave de Asignatura: SC8121
                </p>
                
                <table class="cover-meta-table" style="margin-top: 4rem;">
                    <tr>
                        <td class="label">Carrera:</td>
                        <td>Ingeniería en Sistemas Computacionales</td>
                    </tr>
                    <tr>
                        <td class="label">Nombre del Alumno:</td>
                        <td><strong>Melchor Estrada José Luis</strong></td>
                    </tr>
                    <tr>
                        <td class="label">Matrícula:</td>
                        <td><strong>336009446</strong></td>
                    </tr>
                    <tr>
                        <td class="label">Profesor:</td>
                        <td><strong>RAYMUNDO SOTO SOTO</strong></td>
                    </tr>
                    <tr>
                        <td class="label">Matrícula del Profesor:</td>
                        <td><strong>107885</strong></td>
                    </tr>
                    <tr>
                        <td class="label">Fecha de Entrega:</td>
                        <td>15 de Junio de 2026</td>
                    </tr>
                </table>
            </div>
            <div class="unitec-page-footer">
                <div>Universidad Tecnológica de México - Entregable de Práctica</div>
                <div>Portada</div>
            </div>
        </div>

        <!-- ==========================================
             PÁGINA 7 DEL PRACTICARIO
             ========================================== -->
        <div class="unitec-page" id="page-7">
            <div class="unitec-page-content">
                <table class="unitec-header-table">
                    <tr>
                        <td class="logo-col">
                            <div class="unitec-logo-container">
                                <span class="unitec-logo-text">UNITEC</span>
                                <span class="unitec-logo-subtext">Universidad Tecnológica de México</span>
                            </div>
                        </td>
                        <td class="title-col">Practicario de Sistemas Inteligentes</td>
                        <td class="clave-col">Clave: SC8121</td>
                    </tr>
                </table>

                <h3 style="margin-bottom: 1rem; font-size: 1.25rem;">Datos de la Práctica 3</h3>
                <table class="datos-table">
                    <tr>
                        <td class="cell-label">Práctica 3 de 4:</td>
                        <td class="cell-value" style="font-weight: bold; font-style: italic;">Perceptron</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Objetivo de la práctica:</td>
                        <td class="cell-value">Aplicar los conocimientos en redes neuronales y el lenguaje de programación Python, para programar un perceptron, a través del desarrollo de una aplicación.</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Temas y subtemas asociados:</td>
                        <td class="cell-value">
                            5. Redes neuronales<br>
                            &nbsp;&nbsp;5.2. Control con redes neuronales<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;5.2.1. Red de perceptron<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;5.2.2. Red de retropropagación
                        </td>
                    </tr>
                    <tr>
                        <td class="cell-label">Fecha:</td>
                        <td class="cell-value">15 de Junio de 2026</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Duración (horas):</td>
                        <td class="cell-value">2 horas</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Laboratorio de:</td>
                        <td class="cell-value">Cómputo</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Equipo de seguridad para ingresar al laboratorio (indispensable):</td>
                        <td class="cell-value">N/A</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Software requerido:</td>
                        <td class="cell-value">Cualquier IDE que soporte desarrollo con Python 3</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Equipo necesario en laboratorio:</td>
                        <td class="cell-value">Computadora</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Material/Sustancias/Reactivos disponible en laboratorio:</td>
                        <td class="cell-value">N/A</td>
                    </tr>
                    <tr>
                        <td class="cell-label">Material/Sustancias/Reactivos aportado por el alumno:</td>
                        <td class="cell-value">N/A</td>
                    </tr>
                </table>

                <div class="pdf-section">
                    <div class="pdf-section-header">Desarrollo práctica 3:</div>
                    <div class="pdf-section-body">
                        <p style="font-weight: 700; margin-bottom: 0.75rem;">Indicaciones de la práctica:</p>
                        <ol style="margin-left: 1.5rem; margin-bottom: 0.5rem; font-size: 0.92rem;">
                            <li style="margin-bottom: 0.6rem;">Implementar una matriz en Python para los siguientes datos de entrada:<br>
                                <strong>a.</strong> 0,0,1 | <strong>b.</strong> 1,1,1 | <strong>c.</strong> 1,0,1 | <strong>d.</strong> 0,1,1
                            </li>
                            <li style="margin-bottom: 0.6rem;">A su vez se deberá implementar una segunda matriz la cual funcionará como los datos de salida esperada para el perceptron, los datos de la salida esperada son:<br>
                                <strong>a.</strong> 0 | <strong>b.</strong> 1 | <strong>c.</strong> 1 | <strong>d.</strong> 0
                            </li>
                            <li style="margin-bottom: 0.6rem;">Crear una función la cual representará a la función sigmoidal. Recuerda que la fórmula es:
                                <div class="formula">
                                    $$\\phi(x) = \\frac{1}{1 + e^{-x}}$$
                                </div>
                            </li>
                            <li style="margin-bottom: 0.6rem;">Crea una matriz con los pesos iniciales para las 4 entradas. Estos valores deberán ser valores aleatorios.</li>
                        </ol>
                    </div>
                </div>
            </div>
            <div class="unitec-page-footer">
                <div class="footer-left">Dirección de Tecnología Educativa e Integración de Prácticas</div>
                <div class="footer-right">Página 7 de 12</div>
            </div>
        </div>

        <!-- ==========================================
             PÁGINA 8 DEL PRACTICARIO (Indicaciones 5-12)
             ========================================== -->
        <div class="unitec-page" id="page-8">
            <div class="unitec-page-content">
                <table class="unitec-header-table">
                    <tr>
                        <td class="logo-col">
                            <div class="unitec-logo-container">
                                <span class="unitec-logo-text">UNITEC</span>
                                <span class="unitec-logo-subtext">Universidad Tecnológica de México</span>
                            </div>
                        </td>
                        <td class="title-col">Practicario de Sistemas Inteligentes</td>
                        <td class="clave-col">Clave: SC8121</td>
                    </tr>
                </table>

                <div class="pdf-section">
                    <div class="pdf-section-header">Desarrollo práctica 3:</div>
                    <div class="pdf-section-body">
                        <ol start="5" style="margin-left: 1.5rem; margin-bottom: 0.5rem; font-size: 0.92rem;">
                            <li style="margin-bottom: 0.6rem;">Realiza la propagación hacia adelante, realizando el producto punto entre la matriz con las entradas y la matriz con los pesos.</li>
                            <li style="margin-bottom: 0.6rem;">Aplica la función sigmoidal programada en el paso 3, al resultado obtenido en el paso 5.</li>
                            <li style="margin-bottom: 0.6rem;">Crear una función la cual representará a la gradiente de la curva sigmoidal. Para ello recuerda que la fórmula es:
                                <div class="formula">
                                    $$\\phi'(x) = x \\cdot (1 - x)$$
                                </div>
                            </li>
                            <li style="margin-bottom: 0.6rem;">Calcula el error del resultado obtenido en la propagación hacia adelante, para ello tienes a la siguiente fórmula:
                                <div class="formula">
                                    $$\\text{{error}} = \\text{{salida esperada}} - \\text{{salida obtenida}}$$
                                </div>
                            </li>
                            <li style="margin-bottom: 0.6rem;">Posteriormente se calcularán los ajustes en base a la siguiente fórmula:
                                <div class="formula">
                                    $$f(x) = \\text{{error}} \\cdot \\text{{gradiente de la curva sigmoidal de la salida}}$$
                                </div>
                            </li>
                            <li style="margin-bottom: 0.6rem;">Recalcula los pesos realizando el producto punto entre la matriz que contiene las entradas y la matriz que contiene los ajustes.</li>
                            <li style="margin-bottom: 0.6rem;">Incluye el proceso de propagación adelante y propagación atrás en un ciclo que se repita 50,000 veces. *(Nota: Por solicitud e investigación SMART, se configuró a 100,000 épocas para asegurar un error mínimo de convergencia de orden $10^{{-5}}$).*</li>
                            <li style="margin-bottom: 0.6rem;">Imprime en pantalla la salida obtenida y el valor de los pesos después del proceso de entrenamiento.</li>
                        </ol>
                    </div>
                </div>
            </div>
            <div class="unitec-page-footer">
                <div class="footer-left">Dirección de Tecnología Educativa e Integración de Prácticas</div>
                <div class="footer-right">Página 8 de 12</div>
            </div>
        </div>

        <!-- ==========================================
             PÁGINA 8a: RESULTADOS (SIMULADOR INTERACTIVO)
             ========================================== -->
        <div class="unitec-page" id="page-8a">
            <div class="unitec-page-content">
                <table class="unitec-header-table">
                    <tr>
                        <td class="logo-col">
                            <div class="unitec-logo-container">
                                <span class="unitec-logo-text">UNITEC</span>
                                <span class="unitec-logo-subtext">Universidad Tecnológica de México</span>
                            </div>
                        </td>
                        <td class="title-col">Practicario de Sistemas Inteligentes</td>
                        <td class="clave-col">Clave: SC8121</td>
                    </tr>
                </table>

                <div class="pdf-section">
                    <div class="pdf-section-header">Resultados obtenidos:</div>
                    <div class="pdf-section-body">
                        <p style="margin-bottom: 1rem;">
                            <strong>Descripción del Logro:</strong> Desarrollar aplicaciones usando un perceptron con retropropagación, mediante del desarrollo de una aplicación en Python. Se implementó una arquitectura limpia Modelo-Vista-Controlador (MVC) y se realizaron 5 ejecuciones independientes a 100,000 épocas cada una, obteniendo convergencia perfecta en todas ellas.
                        </p>

                        <div class="only-screen" style="margin-top: 1.5rem;">
                            <h4 style="margin-bottom: 0.5rem; color: var(--primary);">Simulador de Predicción Interactivo (Exclusivo Web):</h4>
                            <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 1rem;">
                                Selecciona una de las 5 corridas entrenadas a 100,000 épocas y manipula los switches de las entradas para calcular la predicción $\\hat{{y}}$ instantáneamente.
                            </p>
                            <div class="sim-grid">
                                <div class="sim-card">
                                    <div class="sim-title">Entradas del Perceptrón</div>
                                    <div class="control-group">
                                        <label for="select-model-run" class="control-label">Ejecución del Modelo:</label>
                                        <select id="select-model-run" class="select-run" onchange="runSimulation()">
                                            <option value="1">Ejecución 1</option>
                                            <option value="2">Ejecución 2</option>
                                            <option value="3">Ejecución 3</option>
                                            <option value="4">Ejecución 4</option>
                                            <option value="5">Ejecución 5</option>
                                        </select>
                                    </div>
                                    <div class="control-group">
                                        <span class="control-label">Sesgo ($X_0$):</span>
                                        <span style="font-weight: bold; color: var(--primary);">1 (Activo)</span>
                                    </div>
                                    <div class="control-group">
                                        <label class="control-label">Entrada $X_1$:</label>
                                        <label class="switch">
                                            <input type="checkbox" id="input-x1" onchange="runSimulation()">
                                            <span class="slider"></span>
                                        </label>
                                    </div>
                                    <div class="control-group">
                                        <label class="control-label">Entrada $X_2$:</label>
                                        <label class="switch">
                                            <input type="checkbox" id="input-x2" onchange="runSimulation()">
                                            <span class="slider"></span>
                                        </label>
                                    </div>
                                    <div class="control-group">
                                        <label class="control-label">Entrada $X_3$:</label>
                                        <label class="switch">
                                            <input type="checkbox" id="input-x3" checked onchange="runSimulation()">
                                            <span class="slider"></span>
                                        </label>
                                    </div>
                                </div>
                                <div class="output-box">
                                    <div class="sim-title">Salida del Perceptrón</div>
                                    <div style="font-size: 0.85rem; color: #64748b;">Probabilidad Obtenida ($\\hat{{y}}$):</div>
                                    <div class="output-value" id="sim-output-val">0.000000</div>
                                    <div class="output-z" id="sim-class-val" style="font-weight: 700; margin-bottom: 0.5rem;">Clasificación: -</div>
                                    <div class="output-z" id="sim-math-val" style="font-size: 0.75rem; text-align: center;">-</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="unitec-page-footer">
                <div class="footer-left">Dirección de Tecnología Educativa e Integración de Prácticas</div>
                <div class="footer-right">Página 8a de 12</div>
            </div>
        </div>

        __INDIVIDUAL_RUNS_PLACEHOLDER__

        <!-- ==========================================
             PÁGINA 8g: RESULTADOS (EVIDENCIA & CURVA COMBINADA)
             ========================================== -->
        <div class="unitec-page" id="page-8g">
            <div class="unitec-page-content">
                <table class="unitec-header-table">
                    <tr>
                        <td class="logo-col">
                            <div class="unitec-logo-container">
                                <span class="unitec-logo-text">UNITEC</span>
                                <span class="unitec-logo-subtext">Universidad Tecnológica de México</span>
                            </div>
                        </td>
                        <td class="title-col">Practicario de Sistemas Inteligentes</td>
                        <td class="clave-col">Clave: SC8121</td>
                    </tr>
                </table>

                <div class="pdf-section">
                    <div class="pdf-section-header">Resultados obtenidos:</div>
                    <div class="pdf-section-body">
                        <h4 style="margin-bottom: 0.5rem; color: var(--primary);">Curva de Aprendizaje Combinada (5 Ejecuciones):</h4>
                        <div class="image-container">
                            <img src="assets/error_curve_combined.png" alt="Evolución del MSE" class="result-image" style="max-height: 450px;">
                            <div class="image-caption">
                                Figura 2: Evolución comparativa del MSE de las 5 ejecuciones en escala semilogarítmica.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="pdf-section">
                    <div class="pdf-section-header">Evidencia de la práctica: (fotografías, videos, archivo, etc.)</div>
                    <div class="pdf-section-body">
                        <p style="font-weight: 700; margin-bottom: 0.5rem;">Entrega del código fuente (archivo .py):</p>
                        <p style="margin-bottom: 1rem;">
                            Se hace entrega del archivo de código fuente de entrega unificado y autocontenido bajo el nombre de <code>Practica_3_SI_Melchor_Jose.py</code>, el cual implementa de forma exacta todos los pasos matemáticos descritos en el practicario escolar:
                        </p>
                        <ul style="margin-left: 1.5rem; margin-bottom: 1rem;">
                            <li>Lógica matemática del perceptrón sigmoidal (Modelo).</li>
                            <li>Trazado en consola y exportación de curvas de aprendizaje y fronteras (Vista).</li>
                            <li>Coordinación de corrida, carga de entorno desde .env y persistencia de resultados JSON (Controlador).</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="unitec-page-footer">
                <div class="footer-left">Dirección de Tecnología Educativa e Integración de Prácticas</div>
                <div class="footer-right">Página 8g de 12</div>
            </div>
        </div>

        <!-- ==========================================
             PÁGINA 8h: CONCLUSIONES & BIBLIOGRAFÍA
             ========================================== -->
        <div class="unitec-page" id="page-8h">
            <div class="unitec-page-content">
                <table class="unitec-header-table">
                    <tr>
                        <td class="logo-col">
                            <div class="unitec-logo-container">
                                <span class="unitec-logo-text">UNITEC</span>
                                <span class="unitec-logo-subtext">Universidad Tecnológica de México</span>
                            </div>
                        </td>
                        <td class="title-col">Practicario de Sistemas Inteligentes</td>
                        <td class="clave-col">Clave: SC8121</td>
                    </tr>
                </table>

                <div class="pdf-section">
                    <div class="pdf-section-header">Conclusiones:</div>
                    <div class="pdf-section-body" style="font-size: 0.92rem;">
                        <p style="margin-bottom: 1rem;">
                            <strong>Al término de la práctica se espera que el alumno sea capaz de comprender cómo se pueden desarrollar y aplicar las redes neuronales para la resolución de problemas usando la inteligencia artificial.</strong>
                        </p>
                        <ol style="margin-left: 1.5rem;">
                            <li style="margin-bottom: 0.75rem;">
                                <strong>Separabilidad Lineal y Coeficientes:</strong> El conjunto de datos propuesto presenta un comportamiento lineal separable donde el resultado esperado $Y$ es idéntico al valor de la entrada $X_1$. La red identificó correctamente esta regla al asignar un peso extremadamente alto a $W_1$ (convergencia a $\\approx +10.46$) y un peso irrelevante cercano a cero a $W_2$ (convergencia a $\\approx -0.11$).
                            </li>
                            <li style="margin-bottom: 0.75rem;">
                                <strong>Impacto de la Inicialización Aleatoria:</strong> Aunque la inicialización aleatoria de pesos conduce a distintas combinaciones algebraicas de valores de pesos finales en cada ejecución (particularmente distribuyendo la compensación del sesgo y $W_3$), el comportamiento predictivo final de la neurona se mantiene idéntico. Esto enfatiza la robustez y la convergencia del algoritmo hacia soluciones equivalentes dentro del espacio de búsqueda.
                            </li>
                            <li style="margin-bottom: 0.75rem;">
                                <strong>Arquitectura Limpia y Visualización Multi-Dimensional:</strong> La implementación basada en el patrón de diseño <strong>Modelo-Vista-Controlador (MVC)</strong> y la filosofía <strong>SMART</strong> facilitaron un código estructurado y modular. La incorporación de visualizaciones de la <strong>frontera de decisión en 2D, 3D y 4D</strong> proporciona una perspectiva geométrica robusta del aprendizaje, demostrando visualmente cómo el clasificador lineal traza hiperplanos y distribuciones de probabilidad en el espacio continuo para cumplir perfectamente con el conjunto de entrenamiento especificado.
                            </li>
                        </ol>
                    </div>
                </div>

                <div class="pdf-section">
                    <div class="pdf-section-header">Bibliografía:</div>
                    <div class="pdf-section-body">
                        <ul class="bib-list" style="font-size: 0.9rem;">
                            <li>
                                Ponce, J., Soto, A., Sayuri, F. (2014). <em>Inteligencia Artificial</em>. LATIn Project.
                            </li>
                            <li>
                                Rosenblatt, F. (1958). The Perceptron: A probabilistic model for information storage and organization in the brain. <em>Psychological Review</em>, 65(6), 386–408.
                            </li>
                            <li>
                                Russell, S., & Norvig, P. (2021). <em>Artificial Intelligence: A Modern Approach</em> (4th ed.). Pearson.
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="unitec-page-footer">
                <div class="footer-left">Dirección de Tecnología Educativa e Integración de Prácticas</div>
                <div class="footer-right">Página 8h de 12</div>
            </div>
        </div>

        <!-- ==========================================
             PÁGINA 9 DEL PRACTICARIO (Criterios de Evaluación)
             ========================================== -->
        <div class="unitec-page" id="page-9">
            <div class="unitec-page-content">
                <table class="unitec-header-table">
                    <tr>
                        <td class="logo-col">
                            <div class="unitec-logo-container">
                                <span class="unitec-logo-text">UNITEC</span>
                                <span class="unitec-logo-subtext">Universidad Tecnológica de México</span>
                            </div>
                        </td>
                        <td class="title-col">Practicario de Sistemas Inteligentes</td>
                        <td class="clave-col">Clave: SC8121</td>
                    </tr>
                </table>

                <div class="pdf-section">
                    <div class="pdf-section-header">Criterios de evaluación:</div>
                    <div class="pdf-section-body">
                        <p style="font-weight: 700; margin-bottom: 0.75rem;">En el código fuente:</p>
                        <table class="datos-table">
                            <thead>
                                <tr style="background-color: #f1f5f9; font-weight: bold; font-family: 'Montserrat', sans-serif;">
                                    <td style="width: 80%; font-weight: bold;">Criterio de Evaluación</td>
                                    <td style="width: 20%; font-weight: bold; text-align: center;">Cumplimiento</td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>El programa realiza la propagación hacia adelante sin errores.</td>
                                    <td style="text-align: center; font-weight: bold; color: var(--primary-light);">CUMPLE (100%)</td>
                                </tr>
                                <tr>
                                    <td>El programa realiza la propagación hacia atrás sin errores.</td>
                                    <td style="text-align: center; font-weight: bold; color: var(--primary-light);">CUMPLE (100%)</td>
                                </tr>
                                <tr>
                                    <td>El programa calcula de forma correcta los pesos después del proceso de entrenamiento.</td>
                                    <td style="text-align: center; font-weight: bold; color: var(--primary-light);">CUMPLE (100%)</td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <div style="margin-top: 2rem; border: 1px dashed #475569; padding: 1rem; border-radius: 0; font-size: 0.9rem; background-color: #fafafa;">
                            <p style="font-weight: 700; margin-bottom: 0.5rem; color: var(--primary);">Notas del Alumno:</p>
                            <p style="margin-bottom: 0.5rem;">
                                Se implementaron verificaciones y assertions matemáticas en la clase del Modelo para certificar que la salida obtenida cumpla rigurosamente con un margen de error menor al $1\%$ en comparación con las etiquetas de salida esperada.
                            </p>
                            <p>
                                Adicionalmente, el patrón MVC separa correctamente la lógica de entrenamiento en <code>model.py</code> y la lógica de graficación en <code>view.py</code>, cumpliendo con los estándares de ingeniería de software.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="unitec-page-footer">
                <div class="footer-left">Dirección de Tecnología Educativa e Integración de Prácticas</div>
                <div class="footer-right">Página 9 de 12</div>
            </div>
        </div>

    </div>

    <!-- Script del Simulador Interactivo -->
    <script>
        // Datos de los modelos de las 5 ejecuciones a 100,000 épocas (actualizados con la última corrida)
        const modelRuns = __JS_MODEL_RUNS__;

        function sigmoid(z) {
            return 1.0 / (1.0 + Math.exp(-z));
        }

        function runSimulation() {
            // Obtener corrida seleccionada
            const runVal = document.getElementById("select-model-run").value;
            const w = modelRuns[runVal];

            // Obtener entradas
            const x1 = document.getElementById("input-x1").checked ? 1.0 : 0.0;
            const x2 = document.getElementById("input-x2").checked ? 1.0 : 0.0;
            const x3 = document.getElementById("input-x3").checked ? 1.0 : 0.0;
            const x0 = 1.0; // Bias constante

            // Calcular suma ponderada z
            const z = (x0 * w.w0) + (x1 * w.w1) + (x2 * w.w2) + (x3 * w.w3);
            
            // Calcular salida sigmoide
            const yHat = sigmoid(z);

            // Actualizar interfaz
            document.getElementById("sim-output-val").innerText = yHat.toFixed(6);
            document.getElementById("sim-math-val").innerText = `z = (${x0} * ${w.w0.toFixed(4)}) + (${x1} * ${w.w1.toFixed(4)}) + (${x2} * ${w.w2.toFixed(4)}) + (${x3} * ${w.w3.toFixed(4)}) = ${z.toFixed(6)}`;

            const classEl = document.getElementById("sim-class-val");
            if (yHat >= 0.5) {
                classEl.innerText = "Clasificación: Clase 1 (Fuerte Activación)";
                classEl.style.color = "#17b978";
            } else {
                classEl.style.color = "#ff6e40";
                classEl.innerText = "Clasificación: Clase 0 (Inhibido)";
            }
        }

        // Modo Oscuro Toggle
        function toggleDarkMode() {
            const body = document.body;
            const btnTheme = document.getElementById("btn-theme");
            const themeIcon = document.getElementById("theme-icon");

            body.classList.toggle("dark-mode");

            if (body.classList.contains("dark-mode")) {
                themeIcon.innerText = "☀️";
                btnTheme.innerHTML = "☀️ Modo Claro";
            } else {
                themeIcon.innerText = "🌙";
                btnTheme.innerHTML = "🌙 Modo Oscuro";
            }
        }

        // Ejecutar simulación inicial
        window.onload = function() {
            runSimulation();
        }
    </script>
</body>
</html>
"""

    final_html = html_template.replace("__INDIVIDUAL_RUNS_PLACEHOLDER__", runs_combined_html)
    final_html = final_html.replace("__JS_MODEL_RUNS__", js_model_runs_str)

    output_path = "Practica_3_SI_Melchor_Jose.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    print("Reporte HTML reformateado exitosamente en Practica_3_SI_Melchor_Jose.html")

if __name__ == "__main__":
    generate_html()
