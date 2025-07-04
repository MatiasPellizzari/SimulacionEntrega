# SimulacionEntrega
README.txt
==========

Simulación de Tanques Acoplados
===============================

Archivos Incluidos
-----------------
- `simulacion.py`: Script de Python que realiza la simulación y genera archivos de datos.
- `graficos_simulacion.gp`: Script de Gnuplot que crea los gráficos a partir de los datos generados.
- `README.txt`: Este archivo con instrucciones.

Archivos Generados
-----------------
- `h1_data.dat`: Datos de altura del tanque 1 (h1) para los métodos Euler y Runge-Kutta, con entrada constante y variable.
- `h2_data.dat`: Datos de altura del tanque 2 (h2) para los mismos casos.
- `flujo_entrada.dat`: Datos del flujo de entrada constante y variable.
- `caudal_salida.dat`: Datos del caudal de salida del tanque 2.
- `tanks_simulation.png`: Imagen PNG con los gráficos (generada por Gnuplot).

Instrucciones de Compilación y Ejecución
---------------------------------------

1. **Configurar el Entorno**
   - Asegúrate de tener Python, gnuplot y NumPy instalados:
     ```bash
     python --version
     pip install numpy
     ```
   - Verifica que Gnuplot esté instalado:
     ```bash
     gnuplot --version
     ```

2. **Ejecutar la Simulación**
   - Abre una terminal en el directorio donde están los archivos.
   - Ejecuta el script de Python:
     ```bash
     python simulacion.py
     ```
   - Esto generará los archivos de datos: `h1_data.dat`, `h2_data.dat`, `flujo_entrada.dat` y `caudal_salida.dat`.

3. **Generar los Gráficos**
   - En la misma terminal, ejecuta el script de Gnuplot:
     ```bash
     gnuplot graficos_simulacion.gp
     ```
   - Esto generará `tanks_simulation.png`, una imagen con cuatro gráficos:
     - Altura del tanque 1 (h1) vs. tiempo.
     - Altura del tanque 2 (h2) vs. tiempo.
     - Flujo de entrada vs. tiempo.
     - Caudal de salida del tanque 2 vs. tiempo.


Notas Adicionales
----------------
- **Tiempo de Ejecución**: La simulación con `tiempo_total = 1000` y `paso_tiempo = 0.1` genera 10001 puntos, lo que puede ser lento en sistemas con poca memoria. Reducir `tiempo_total` acelera el proceso.
- **Formato de Salida**: Para generar gráficos en otro formato (e.g., PDF, SVG), edita `graficos_simulacion.gp`:
  - PDF: `set terminal pdfcairo size 12in,8in; set output 'tanks_simulation.pdf'`
  - SVG: `set terminal svg size 1200,800; set output 'tanks_simulation.svg'`
- **Visualización Interactiva**: Para ver los gráficos sin guardar un archivo, elimina las líneas `set terminal` y `set output` en `graficos_simulacion.gp` y ejecuta `gnuplot graficos_simulacion.gp`.