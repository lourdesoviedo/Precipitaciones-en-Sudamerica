# Análisis Espacial y Temporal de Precipitaciones en Sudamérica

Proyecto desarrollado en el marco del **Laboratorio de Procesamiento de Información Meteorológica** (Licenciatura en Ciencias de la Atmósfera, FCEN - UBA).

El objetivo principal es el procesamiento, análisis estadístico y visualización de datos grillados multidimensionales de precipitación para caracterizar la variabilidad climática espacial y estacional en la región sudamericana.

---

## Objetivos y Alcance

- **Lectura y procesamiento de datos multidimensionales:** Manipulación de archivos en formato **NetCDF** provistos por la **NOAA**.
- **Análisis estadístico regional:** Cálculo y comparación de campos medios y desvíos estándar de precipitación a escala estacional y por subregiones.
- **Visualización geoespacial:** Generación de mapas climáticos y gráficos de diagnóstico para evaluar la distribución espacial y temporal de las lluvias.

---

## Herramientas y Librerías

El análisis se implementó en **Python**, utilizando el siguiente stack científico:

- **`netCDF4` / `xarray`**: Extracción y manejo de conjuntos de datos multidimensionales.
- **`pandas` & `numpy`**: Tratamiento numérico, estructuración y cálculos estadísticos matriciales.
- **`cartopy`**: Proyecciones cartográficas y mapeo geoespacial de variables climáticas.
- **`matplotlib`**: Generación de figuras, campos de contorno y gráficos de análisis estacional.

---

## Estructura del Repositorio

- `data/`: Información sobre fuentes y especificaciones de los datos de NOAA utilizados.
- `notebooks/` (o `scripts/`): Código fuente con el preprocesamiento, cálculo de estadísticas y generación de figuras.
- `figures/`: Salidas gráficas (mapas de precipitación media, desvíos y ciclos anuales).
