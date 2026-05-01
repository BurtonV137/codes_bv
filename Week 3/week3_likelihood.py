#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize

c = 299792.458 # Velocidad de la luz


# In[15]:


def E_func(z, Omega_m):
    return np.sqrt(Omega_m * (1 + z)**3 + (1 - Omega_m))

def integrando(z, Omega_m):
    return 1.0 / E_func(z, Omega_m)

def dist_luminosidad(z_hel, z_cmb, Omega_m, H0):
    integral, _ = quad(integrando, 0, z_cmb, args=(Omega_m,))
    return (1 + z_hel) * (c / H0) * integral


# In[16]:


df = pd.read_csv('Pantheon+SH0ES.dat', sep='\s+')


# In[17]:


# Función para calcular mu teórico (basada en la semana 1)
def mu_teorico(z_hel, z_cmb, Omega_m, H0):
    # Nota: Usamos z_cmb para la integral (expansión) 
    # y z_hel para el factor (1+z) de la distancia de luminosidad
    dL = dist_luminosidad(z_hel, z_cmb, Omega_m, H0)
    return 5 * np.log10(dL) + 25

# Tarea 1 y 2: Predicción del modelo
def modelo_prediccion(df, Omega_m, H0, Mb):
    # Creamos un array de ceros del mismo tamaño que el dataframe
    m_b_th = np.zeros(len(df))

    # Creamos la máscara (filtro) para saber quién es calibrador
    # Esto devuelve una serie de True y False
    es_calibrador = df['IS_CALIBRATOR'] == 1

    # --- CASO 1: Calibradores ---
    # Usamos .values para que Pandas nos de los números puros y no se confunda
    m_b_th[es_calibrador] = Mb + df.loc[es_calibrador, 'CEPH_DIST'].values

    # --- CASO 2: Cosmología (Supernovas lejanas) ---
    # El símbolo ~ significa "lo contrario", es decir, donde NO es calibrador
    no_es_calibrador = ~es_calibrador

    # Extraemos los redshifts como arrays de numpy para evitar el error de "Truth Value"
    z_hel_vals = df.loc[no_es_calibrador, 'zHEL'].values
    z_cmb_vals = df.loc[no_es_calibrador, 'zCMB'].values

    # Calculamos mu para cada z usando una lista de comprensión (más seguro)
    mu_vals = np.array([mu_teorico(zh, zc, Omega_m, H0) for zh, zc in zip(z_hel_vals, z_cmb_vals)])

    m_b_th[no_es_calibrador] = Mb + mu_vals

    return m_b_th


# In[18]:


def calcular_chi2(params, df):
    # params es una lista [Omega_m, H0, Mb]
    Om, H0, Mb = params

    # Predicción del modelo
    m_th = modelo_prediccion(df, Om, H0, Mb)

    # Observación (usamos la columna m_b_corr de la semana 2)
    m_obs = df['m_b_corr']

    # Error (esta semana usamos uno simplificado, ej. 0.1 o el error del archivo)
    sigma = 0.1 # Valor aproximado para la semana 3

    # Fórmula: Suma de ((obs - th)^2 / sigma^2)
    residuos = (m_obs - m_th)**2 / sigma**2
    return np.sum(residuos)


# In[19]:


from scipy.optimize import minimize

# Valores iniciales para empezar a buscar
# Omega_m ~ 0.3, H0 ~ 70, Mb ~ -19.2
p0 = [0.3, 70, -19.2]

# Minimizamos el Chi2
resultado = minimize(calcular_chi2, p0, args=(df,), method='Nelder-Mead')

Om_best, H0_best, Mb_best = resultado.x

print(f"--- RESULTADOS PRELIMINARES SEMANA 3 ---")
print(f"Omega_m óptimo: {Om_best:.3f}")
print(f"H0 óptimo: {H0_best:.2f}")
print(f"Mb (Magnitud Absoluta): {Mb_best:.3f}")
print(f"Chi2 mínimo: {resultado.fun:.2f}")

