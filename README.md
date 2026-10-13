# MaderNova S. A. — Proyecto de Ciencia de Datos (Semana 8)

## Objetivo y preguntas de investigación
Analizar 200 registros de producción y distribución entre 2025-01-01 y 2025-07-19 para comparar plantas, cuantificar pérdidas y estudiar la logística. ¿Qué plantas presentan más merma? ¿Qué canales concentran ventas? ¿Cómo varía el despacho? ¿Qué problemas de calidad presenta el dataset?

## Metodología
1. Cargar el Excel original sin modificarlo.
2. Normalizar fechas, tipos y calcular tasas de merma, consumo específico y productividad.
3. Auditar nulos, duplicados, rangos, valores negativos e IQR.
4. Calcular indicadores por planta con NumPy y Joblib y asociación Spearman con SciPy.
5. Exportar dos archivos departamentales y dashboard PNG/HTML.
6. Documentar limitaciones y publicar versiones mediante Git.

## Resultados
- Volumen total: 53.020,00 m³; merma total: 4.620,00 m³ (8,71 %).
- Ventas: 47329 unidades; despacho medio: 6,14 días.
- Planta Sur: merma 8,05 %; Centro: 9,44 %; Norte: 8,72 %.
- Spearman volumen-consumo: rho=-0.027, p=0.703; no se observa asociación monotónica significativa en la muestra.
- Calidad: cero nulos, duplicados completos, valores negativos o extremos IQR en las seis variables numéricas originales.

## Ejecución
```bash
python -m pip install -r requirements.txt
python ejecutar.py
```
Ejecutar desde la raíz del proyecto. El script regenera CSV, métricas y gráficos. Para abrir el notebook: `jupyter notebook notebooks/analisis_madernova.ipynb`.

## Estructura
- `data/`: fuente original y datos procesados.
- `src/analisis.py`: funciones modulares NumPy, SciPy y Joblib.
- `ejecutar.py`: flujo reproducible.
- `notebooks/`: cuaderno demostrativo.
- `dashboards/`: gráficos PNG y dashboard HTML interactivo.
- `resultados/`: exportaciones de Producción y Comercial, métricas JSON y resumen de plantas.
- `documentacion/`: explicación técnica y control de versiones.

## Calidad y limitaciones
No hay fechas prometidas, objetivos de producción, precios, costos ni inventarios; por ello no se pueden medir atrasos contractuales, rentabilidad o quiebres de stock. Las ventas se expresan en unidades y la producción en m³, por lo que no deben compararse directamente. El archivo registra una observación diaria con planta variable: no es una serie diaria completa por planta. La relación estadística no prueba causalidad. Los umbrales operacionales requieren validación con la empresa.

## Colaboración y GitHub
Repositorio preparado para subir, pero **no publicado automáticamente**. Crear un repositorio vacío en GitHub y ejecutar:
```bash
git init
git add .
git commit -m "Proyecto MaderNova semana 8"
git branch -M main
git remote add origin https://github.com/USUARIO/madernova-ciencia-datos.git
git push -u origin main
```
Sustituir `USUARIO` por el usuario real y adjuntar la URL verdadera al informe. Para trabajo en equipo: ramas por cambio, commits descriptivos, pull requests y revisión.

## Fuentes
- IACC. (s. f.). *Ciencia de Datos. Semana 8. Tarea* [Guía de evaluación].
- NumPy Developers. (s. f.). *NumPy documentation*. https://numpy.org/doc/
- SciPy Community. (s. f.). *SciPy documentation*. https://docs.scipy.org/doc/scipy/
- Joblib Developers. (s. f.). *Joblib documentation*. https://joblib.readthedocs.io/
