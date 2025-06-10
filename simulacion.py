import numpy as np
import matplotlib.pyplot as plt

# --- Parámetros del sistema ---
area_tanque = 2.0              # Área de la base de los tanques (m²)
coef_transferencia = 0.5       # K1: coeficiente de transferencia entre tanques
coef_descarga = 1.0            # K2: coeficiente de descarga del segundo tanque
gravedad = 9.8                 # Aceleración gravitatoria (m/s²)
paso_tiempo = 0.1              # Paso de integración (s)
tiempo_total = 100             # Duración total de la simulación (s)

# --- Vector de tiempo ---
tiempo = np.arange(0, tiempo_total + paso_tiempo, paso_tiempo)

# --- Condiciones iniciales ---
altura1_const = [1000.0]       # Altura inicial en tanque 1 (entrada constante)
altura2_const = [0.0]          # Altura inicial en tanque 2 (entrada constante)
flujo_constante = [20.0] * len(tiempo)  # Flujo constante de entrada
caudal_salida_const = []       # Salida del segundo tanque (flujo constante)

altura1_var = [1000.0]         # Altura inicial en tanque 1 (entrada variable)
altura2_var = [0.0]            # Altura inicial en tanque 2 (entrada variable)
flujo_variable_total = []      # Flujo variable de entrada
caudal_salida_var = []         # Salida del segundo tanque (flujo variable)

# --- Función para el flujo de entrada variable ---
def calcular_flujo_variable(t):
    return 10 + 10 * np.sin(0.1 * t)

# --- Simulación temporal ---
for i in range(1, len(tiempo)):
    # Flujo de entrada variable en este instante
    flujo_entrada_var = calcular_flujo_variable(tiempo[i-1])
    flujo_variable_total.append(flujo_entrada_var)

    # --- Entrada constante ---
    h1_anterior_c = altura1_const[-1]
    h2_anterior_c = altura2_const[-1]
    
    # Derivadas de las alturas (ecuaciones diferenciales)
    derivada_h1_c = (1 / area_tanque) * (flujo_constante[i-1] - coef_transferencia * h1_anterior_c)
    derivada_h2_c = (1 / area_tanque) * (coef_transferencia * h1_anterior_c - coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_c)))

    # Actualización de alturas
    altura1_const.append(h1_anterior_c + paso_tiempo * derivada_h1_c)
    altura2_const.append(h2_anterior_c + paso_tiempo * derivada_h2_c)

    # Caudal de salida para entrada constante
    caudal_salida_const.append(coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_c)))

    # --- Entrada variable ---
    h1_anterior_v = altura1_var[-1]
    h2_anterior_v = altura2_var[-1]

    derivada_h1_v = (1 / area_tanque) * (flujo_entrada_var - coef_transferencia * h1_anterior_v)
    derivada_h2_v = (1 / area_tanque) * (coef_transferencia * h1_anterior_v - coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_v)))

    altura1_var.append(h1_anterior_v + paso_tiempo * derivada_h1_v)
    altura2_var.append(h2_anterior_v + paso_tiempo * derivada_h2_v)

    # Caudal de salida para entrada variable
    caudal_salida_var.append(coef_descarga * np.sqrt(max(0, gravedad * h2_anterior_v)))

# Agregar último valor de flujo y caudal para cerrar los arrays
flujo_variable_total.append(calcular_flujo_variable(tiempo[-1]))
caudal_salida_var.append(coef_descarga * np.sqrt(max(0, gravedad * altura2_var[-1])))
caudal_salida_const.append(coef_descarga * np.sqrt(max(0, gravedad * altura2_const[-1])))

# --- Gráficos ---
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Simulación de Tanques Acoplados', fontsize=16)

# Altura h1(t)
axs[0, 0].plot(tiempo, altura1_const, label='Entrada Constante')
axs[0, 0].plot(tiempo, altura1_var, label='Entrada Variable')
axs[0, 0].set_title('Altura del Tanque 1 (h1)')
axs[0, 0].legend()

# Altura h2(t)
axs[0, 1].plot(tiempo, altura2_const, label='Entrada Constante')
axs[0, 1].plot(tiempo, altura2_var, label='Entrada Variable')
axs[0, 1].set_title('Altura del Tanque 2 (h2)')
axs[0, 1].legend()

# Flujo de entrada
axs[1, 0].plot(tiempo, flujo_constante, label='Constante')
axs[1, 0].plot(tiempo, flujo_variable_total, label='Variable')
axs[1, 0].set_title('Flujo de Entrada F(t)')
axs[1, 0].legend()

# Caudal de salida
axs[1, 1].plot(tiempo, caudal_salida_const, label='Constante')
axs[1, 1].plot(tiempo, caudal_salida_var, label='Variable')
axs[1, 1].set_title('Caudal de Salida Q(t)')
axs[1, 1].legend()

# Etiquetas y formato
for ax in axs.flat:
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Valor')
    ax.grid(True)

plt.tight_layout()
plt.show()