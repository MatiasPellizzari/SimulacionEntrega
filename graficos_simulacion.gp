# plot_tanks.gp
set terminal pngcairo size 1200,800 enhanced font 'Verdana,10'
set output 'tanks_simulation.png'

# Configurar el diseño 2x2
set multiplot layout 2,2 title "Simulación de Tanques Acoplados" font ",16"

# Estilo general
set grid
set style line 1 lc rgb '#FF0000' lt 1 lw 2 dt 2  # Constante Euler (rojo, discontinuo)
set style line 2 lc rgb '#FF0000' lt 1 lw 2       # Constante Runge-Kutta (rojo, continuo)
set style line 3 lc rgb '#0000FF' lt 1 lw 2 dt 2  # Variable Euler (azul, discontinuo)
set style line 4 lc rgb '#0000FF' lt 1 lw 2       # Variable Runge-Kutta (azul, continuo)
set style line 5 lc rgb '#00FF00' lt 1 lw 2       # Flujo constante (verde, continuo)

# Gráfico 1: Altura del Tanque 1 (h1)
set title "Altura del Tanque 1 (h1)"
set xlabel "Tiempo (s)"
set ylabel "Altura (m)"
plot 'h1_data.dat' using 1:2 with lines ls 1 title 'Constante Euler', \
     'h1_data.dat' using 1:3 with lines ls 2 title 'Constante Runge-Kutta', \
     'h1_data.dat' using 1:4 with lines ls 3 title 'Variable Euler', \
     'h1_data.dat' using 1:5 with lines ls 4 title 'Variable Runge-Kutta'

# Gráfico 2: Altura del Tanque 2 (h2)
set title "Altura del Tanque 2 (h2)"
set xlabel "Tiempo (s)"
set ylabel "Altura (m)"
plot 'h2_data.dat' using 1:2 with lines ls 1 title 'Constante Euler', \
     'h2_data.dat' using 1:3 with lines ls 2 title 'Constante Runge-Kutta', \
     'h2_data.dat' using 1:4 with lines ls 3 title 'Variable Euler', \
     'h2_data.dat' using 1:5 with lines ls 4 title 'Variable Runge-Kutta'

# Gráfico 3: Flujo de Entrada
set title "Flujo de Entrada"
set xlabel "Tiempo (s)"
set ylabel "Flujo (m³/s)"
plot 'flujo_entrada.dat' using 1:2 with lines ls 5 title 'Constante', \
     'flujo_entrada.dat' using 1:3 with lines ls 4 title 'Variable'

# Gráfico 4: Caudal de Salida del Tanque 2
set title "Caudal de Salida del Tanque 2"
set xlabel "Tiempo (s)"
set ylabel "Caudal (m³/s)"
plot 'caudal_salida.dat' using 1:2 with lines ls 1 title 'Constante Euler', \
     'caudal_salida.dat' using 1:3 with lines ls 2 title 'Constante Runge-Kutta', \
     'caudal_salida.dat' using 1:4 with lines ls 3 title 'Variable Euler', \
     'caudal_salida.dat' using 1:5 with lines ls 4 title 'Variable Runge-Kutta'

# Finalizar multiplot
unset multiplot