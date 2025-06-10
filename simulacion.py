import numpy as np

# --- Parámetros del sistema ---
area_tanque = 2.0              # Área de la base de los tanques (m²)
coef_transferencia = 0.5       # K1: coeficiente de transferencia entre tanques
coef_descarga = 1.0            # K2: coeficiente de descarga del segundo tanque
gravedad = 9.8                 # Aceleración gravitatoria (m/s²)
paso_tiempo = 0.1              # Paso de integración (s)
tiempo_total = 1000             # Duración total de la simulación (s)

# --- Vector de tiempo ---
tiempo = np.arange(0, tiempo_total + paso_tiempo, paso_tiempo)

# --- Condiciones iniciales ---
# Entrada constante
altura1_const_euler = [1000.0]  # Altura inicial en tanque 1 (Euler, entrada constante)
altura2_const_euler = [0.0]     # Altura inicial en tanque 2 (Euler, entrada constante)
altura1_const_rk = [1000.0]    # Altura inicial en tanque 1 (Runge-Kutta, entrada constante)
altura2_const_rk = [0.0]       # Altura inicial en tanque 2 (Runge-Kutta, entrada constante)
flujo_constante = [20.0] * len(tiempo)  # Flujo constante de entrada
caudal_salida_const_euler = []   # Salida del segundo tanque (Euler, flujo constante)
caudal_salida_const_rk = []     # Salida del segundo tanque (Runge-Kutta, flujo constante)

# Entrada variable
altura1_var_euler = [1000.0]    # Altura inicial en tanque 1 (Euler, entrada variable)
altura2_var_euler = [0.0]       # Altura inicial en tanque 2 (Euler, entrada variable)
altura1_var_rk = [1000.0]      # Altura inicial en tanque 1 (Runge-Kutta, entrada variable)
altura2_var_rk = [0.0]         # Altura inicial en tanque 2 (Runge-Kutta, entrada variable)
flujo_variable_total = []        # Flujo variable de entrada
caudal_salida_var_euler = []     # Salida del segundo tanque (Euler, flujo variable)
caudal_salida_var_rk = []       # Salida del segundo tanque (Runge-Kutta, flujo variable)

# --- Función para el flujo de entrada variable ---
def calcular_flujo_variable(t):
    return 10 + 10 * np.sin(0.1 * t)

# --- Función para el flujo de entrada variable ---
def calcular_flujo_variable_ejer_5(t):
    return 20.0 + 10.0 * np.sin(0.2 * t)  # Como en Ejercicio 5

# --- Derivadas del sistema ---
def derivadas(t, h1, h2, flujo_entrada):
    dh1_dt = (flujo_entrada(t) - coef_transferencia * h1) / area_tanque
    dh2_dt = (coef_transferencia * h1 - coef_descarga * np.sqrt(max(0, gravedad * h2))) / area_tanque
    return dh1_dt, dh2_dt

# --- Simulación temporal ---
for i in range(1, len(tiempo)):
    # Flujo de entrada variable en este instante
    flujo_entrada_var = calcular_flujo_variable(tiempo[i-1])
    flujo_variable_total.append(flujo_entrada_var)

    # --- Entrada constante Euler ---
    h1_anterior_c_euler = altura1_const_euler[-1]
    h2_anterior_c_euler = altura2_const_euler[-1]
    
    # Derivadas de las alturas (ecuaciones diferenciales)
    derivada_h1_c_euler, derivada_h2_c_euler = derivadas(tiempo[i-1], h1_anterior_c_euler, h2_anterior_c_euler, lambda t: 20.0)

    # Actualización de alturas Euler
    altura1_const_euler.append(h1_anterior_c_euler + paso_tiempo * derivada_h1_c_euler)
    altura2_const_euler.append(h2_anterior_c_euler + paso_tiempo * derivada_h2_c_euler)

    # Caudal de salida para entrada constante Euler
    caudal_salida_const_euler.append(coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_c_euler)))

    # --- Entrada constante (Runge-Kutta) ---
    h1_anterior_c_rk = altura1_const_rk[-1]
    h2_anterior_c_rk = altura2_const_rk[-1]
    # k1
    k1_h1_c, k1_h2_c = derivadas(tiempo[i-1], h1_anterior_c_rk, h2_anterior_c_rk, lambda t: 20.0)
    # k2
    k2_h1_c, k2_h2_c = derivadas(tiempo[i-1] + paso_tiempo/2, 
                                 h1_anterior_c_rk + (paso_tiempo/2) * k1_h1_c, 
                                 h2_anterior_c_rk + (paso_tiempo/2) * k1_h2_c, 
                                 lambda t: 20.0)
    # k3
    k3_h1_c, k3_h2_c = derivadas(tiempo[i-1] + paso_tiempo/2, 
                                 h1_anterior_c_rk + (paso_tiempo/2) * k2_h1_c, 
                                 h2_anterior_c_rk + (paso_tiempo/2) * k2_h2_c, 
                                 lambda t: 20.0)
    # k4
    k4_h1_c, k4_h2_c = derivadas(tiempo[i-1] + paso_tiempo, 
                                 h1_anterior_c_rk + paso_tiempo * k3_h1_c, 
                                 h2_anterior_c_rk + paso_tiempo * k3_h2_c, 
                                 lambda t: 20.0)
    # Actualización
    h1_new_c_rk = h1_anterior_c_rk + (paso_tiempo/6) * (k1_h1_c + 2*k2_h1_c + 2*k3_h1_c + k4_h1_c)
    h2_new_c_rk = h2_anterior_c_rk + (paso_tiempo/6) * (k1_h2_c + 2*k2_h2_c + 2*k3_h2_c + k4_h2_c)
    altura1_const_rk.append(max(0, h1_new_c_rk))
    altura2_const_rk.append(max(0, h2_new_c_rk))
    caudal_salida_const_rk.append(coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_c_rk)))

    # --- Entrada variable Euler ---
    h1_anterior_v_euler = altura1_var_euler[-1]
    h2_anterior_v_euler = altura2_var_euler[-1]

    derivada_h1_v_euler, derivada_h2_v_euler = derivadas(tiempo[i-1], h1_anterior_v_euler, h2_anterior_v_euler, calcular_flujo_variable)

    altura1_var_euler.append(h1_anterior_v_euler + paso_tiempo * derivada_h1_v_euler)
    altura2_var_euler.append(h2_anterior_v_euler + paso_tiempo * derivada_h2_v_euler)

    # Caudal de salida para entrada variable Euler
    caudal_salida_var_euler.append(coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_v_euler)))

    # --- Entrada variable (Runge-Kutta) ---
    h1_anterior_v_rk = altura1_var_rk[-1]
    h2_anterior_v_rk = altura2_var_rk[-1]
    # k1
    k1_h1_v, k1_h2_v = derivadas(tiempo[i-1], h1_anterior_v_rk, h2_anterior_v_rk, calcular_flujo_variable)
    # k2
    k2_h1_v, k2_h2_v = derivadas(tiempo[i-1] + paso_tiempo/2, 
                                 h1_anterior_v_rk + (paso_tiempo/2) * k1_h1_v, 
                                 h2_anterior_v_rk + (paso_tiempo/2) * k1_h2_v, 
                                 calcular_flujo_variable)
    # k3
    k3_h1_v, k3_h2_v = derivadas(tiempo[i-1] + paso_tiempo/2, 
                                 h1_anterior_v_rk + (paso_tiempo/2) * k2_h1_v, 
                                 h2_anterior_v_rk + (paso_tiempo/2) * k2_h2_v, 
                                 calcular_flujo_variable)
    # k4
    k4_h1_v, k4_h2_v = derivadas(tiempo[i-1] + paso_tiempo, 
                                 h1_anterior_v_rk + paso_tiempo * k3_h1_v, 
                                 h2_anterior_v_rk + paso_tiempo * k3_h2_v, 
                                 calcular_flujo_variable)
    # Actualización
    h1_new_v_rk = h1_anterior_v_rk + (paso_tiempo/6) * (k1_h1_v + 2*k2_h1_v + 2*k3_h1_v + k4_h1_v)
    h2_new_v_rk = h2_anterior_v_rk + (paso_tiempo/6) * (k1_h2_v + 2*k2_h2_v + 2*k3_h2_v + k4_h2_v)
    altura1_var_rk.append(max(0, h1_new_v_rk))
    altura2_var_rk.append(max(0, h2_new_v_rk))
    caudal_salida_var_rk.append(coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_v_rk)))

# Agregar último valor de flujo y caudal para cerrar los arrays
flujo_variable_total.append(calcular_flujo_variable(tiempo[-1]))
caudal_salida_var_euler.append(coef_descarga * np.sqrt(max(0, gravedad * altura2_var_euler[-1])))
caudal_salida_const_euler.append(coef_descarga * np.sqrt(max(0, gravedad * altura2_const_euler[-1])))
caudal_salida_var_rk.append(coef_descarga * np.sqrt(max(0, gravedad * altura2_var_rk[-1])))
caudal_salida_const_rk.append(coef_descarga * np.sqrt(max(0, gravedad * altura2_const_rk[-1])))

# --- Guardar datos en archivos para Gnuplot ---
# Archivo para h1(t)
with open('h1_data.dat', 'w') as f:
    f.write("# tiempo h1_const_euler h1_const_rk h1_var_euler h1_var_rk\n")
    for i in range(len(tiempo)):
        f.write(f"{tiempo[i]:.4f} {altura1_const_euler[i]:.4f} {altura1_const_rk[i]:.4f} {altura1_var_euler[i]:.4f} {altura1_var_rk[i]:.4f}\n")

# Archivo para h2(t)
with open('h2_data.dat', 'w') as f:
    f.write("# tiempo h2_const_euler h2_const_rk h2_var_euler h2_var_rk\n")
    for i in range(len(tiempo)):
        f.write(f"{tiempo[i]:.4f} {altura2_const_euler[i]:.4f} {altura2_const_rk[i]:.4f} {altura2_var_euler[i]:.4f} {altura2_var_rk[i]:.4f}\n")

# Archivo para flujo de entrada
with open('flujo_entrada.dat', 'w') as f:
    f.write("# tiempo flujo_constante flujo_variable\n")
    for i in range(len(tiempo)):
        f.write(f"{tiempo[i]:.4f} {flujo_constante[i]:.4f} {flujo_variable_total[i]:.4f}\n")

# Archivo para caudal de salida
with open('caudal_salida.dat', 'w') as f:
    f.write("# tiempo caudal_const_euler caudal_const_rk caudal_var_euler caudal_var_rk\n")
    for i in range(len(tiempo)):
        f.write(f"{tiempo[i]:.4f} {caudal_salida_const_euler[i]:.4f} {caudal_salida_const_rk[i]:.4f} {caudal_salida_var_euler[i]:.4f} {caudal_salida_var_rk[i]:.4f}\n")

print("Datos guardados en 'h1_data.dat', 'h2_data.dat', 'flujo_entrada.dat' y 'caudal_salida.dat'.")