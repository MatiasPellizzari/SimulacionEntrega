import numpy as np
import matplotlib.pyplot as plt

# Parámetros
A = 2
K1 = 0.5
K2 = 1
g = 9.8
h = 0.1  # paso de integración
t_max = 100  # tiempo de simulación

# Tiempo
t = np.arange(0, t_max + h, h)

# Condiciones iniciales
h1_const = [1000]
h2_const = [0]
F_const = [20] * len(t)  # flujo constante
Q_salida_const = []

h1_var = [1000]
h2_var = [0]
F_var = []  # flujo variable
Q_salida_var = []

# Funciones auxiliares
def flujo_variable(tiempo):
    return 10 + 10 * np.sin(0.1 * tiempo)

# Simulación
for i in range(1, len(t)):
    # Flujo de entrada
    Fv = flujo_variable(t[i-1])
    F_var.append(Fv)

    # Entrada constante
    f_ent_c = F_const[i-1]
    h1_c = h1_const[-1]
    h2_c = h2_const[-1]
    dh1dt_c = (1/A) * (f_ent_c - K1 * h1_c)
    dh2dt_c = (1/A) * (K1 * h1_c - K2 * np.sqrt(max(0, g * h2_c)))
    h1_const.append(h1_c + h * dh1dt_c)
    h2_const.append(h2_c + h * dh2dt_c)
    Q_salida_const.append(K2 * np.sqrt(max(0, g * h2_c)))

    # Entrada variable
    h1_v = h1_var[-1]
    h2_v = h2_var[-1]
    dh1dt_v = (1/A) * (Fv - K1 * h1_v)
    dh2dt_v = (1/A) * (K1 * h1_v - K2 * np.sqrt(max(0, g * h2_v)))
    h1_var.append(h1_v + h * dh1dt_v)
    h2_var.append(h2_v + h * dh2dt_v)
    Q_salida_var.append(K2 * np.sqrt(max(0, g * h2_v)))

# Agregar último valor de Fentrada y Qsalida para entrada variable
F_var.append(flujo_variable(t[-1]))
Q_salida_var.append(K2 * np.sqrt(max(0, g * h2_var[-1])))
Q_salida_const.append(K2 * np.sqrt(max(0, g * h2_const[-1])))

# --- Gráficas ---
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Simulación de tanques acoplados', fontsize=16)

axs[0, 0].plot(t, h1_const, label='Constante')
axs[0, 0].plot(t, h1_var, label='Variable')
axs[0, 0].set_title('Altura h1(t)')
axs[0, 0].legend()

axs[0, 1].plot(t, h2_const, label='Constante')
axs[0, 1].plot(t, h2_var, label='Variable')
axs[0, 1].set_title('Altura h2(t)')
axs[0, 1].legend()

axs[1, 0].plot(t, F_const, label='Constante')
axs[1, 0].plot(t, F_var, label='Variable')
axs[1, 0].set_title('Flujo de entrada Fentrada(t)')
axs[1, 0].legend()

axs[1, 1].plot(t, Q_salida_const, label='Constante')
axs[1, 1].plot(t, Q_salida_var, label='Variable')
axs[1, 1].set_title('Caudal de salida Q(t)')
axs[1, 1].legend()

for ax in axs.flat:
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Valor')
    ax.grid(True)

plt.tight_layout()
plt.show()