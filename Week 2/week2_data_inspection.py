#!/usr/bin/env python
# coding: utf-8

# In[14]:


#Paso 1: Importación de librerias

#pandas: Librería para manejar tablas de datos (DataFrames)
#numpy: Para cálculos matemáticos y manejo de valores numéricos (como infinitos)
#matplotlib.pyplot: Para crear todas las visualizaciones y gráficos

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Esto es para que los gráficos salgan dentro del cuaderno
get_ipython().run_line_magic('matplotlib', 'inline')

# Configuración de estilo del gráfico
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['font.size'] = 12


# In[15]:


#Paso 2: Cargar el Dataset

# Cargamos el archivo que ya tienes en el panel izquierdo
# pd.read_csv: Lee el archivo de texto.
# sep='\s+': Indica que las columnas están separadas por uno o más espacios en blanco.
df = pd.read_csv('Pantheon+SH0ES.dat', sep='\s+')

# df.head(): Muestra las primeras 5 filas de la tabla para verificar que las columnas cargaron bien.
df.head()


# In[16]:


# Paso 3: Estadísticas de la muestra

#Contar total de supernovas (filas)
# len(df): Cuenta cuántas filas totales tiene la tabla (cada fila es una supernova).
total_sn = len(df)

# Identificar calibradores (aquellos donde IS_CALIBRATOR es 1)
# Filtramos la tabla original para crear una nueva que solo contenga los "calibradores".
# Los calibradores son SN en galaxias cercanas cuya distancia conocemos por Cefeidas.
calibradores = df[df['IS_CALIBRATOR'] == 1]
total_cal = len(calibradores)

print(f"--- RESUMEN DEL DATASET ---")
print(f"Número total de supernovas en la muestra: {total_sn}")
print(f"Número de supernovas calibradoras (Cefeidas): {total_cal}")
print(f"Número de supernovas no calibradoras: {total_sn - total_cal}")


# In[17]:


#Paso 4: Limpieza de datos

# Definimos las columnas escenciales para los cálculos de las próximas semanas
columnas_clave = ['zCMB', 'zHEL', 'm_b_corr', 'IS_CALIBRATOR']

# .isnull().sum(): Busca si hay celdas vacías (NaN) en el archivo y las suma por columna.
print("¿Hay valores nulos (vacíos) en las columnas clave?")
print(df[columnas_clave].isnull().sum())

# np.isfinite(...).all(): Verifica que no existan valores "infinitos" o errores de lectura.
# Esto asegura que el código no se rompa al hacer cálculos matemáticos después.
print("\n¿Son todos los valores numéricos finitos?")
print(np.isfinite(df[columnas_clave]).all())


# In[18]:


#Paso 5: Gráficas (escala lineal y logarítmica)

plt.figure()

# plt.scatter: Crea un gráfico de puntos. 
# Graficamos todas las supernovas en gris con transparencia (alpha=0.3) para ver la densidad.
# zCMB: Redshift corregido al fondo cósmico de microondas (eje X).
# m_b_corr: Magnitud aparente corregida (eje Y).

#Graficamos todas las supernovas en gris (para que no distraigan)
plt.scatter(df['zCMB'], df['m_b_corr'], s=10, alpha=0.3, color='gray', label='Pantheon+ SN')

#Resaltamos los calibradores en rojo
#Están concentrados en redshifts bajos
plt.scatter(calibradores['zCMB'], calibradores['m_b_corr'], s=25, color='red', label='Calibradores')

# Configuración del gráfico
plt.xscale('log') # Usamos escala logarítmica para ver mejor el rango de redshift

plt.xlabel('Redshift $z_{CMB}$ (escala log)')
plt.ylabel('Magnitud aparente corregida $m_{b,corr}$')
plt.title('Diagrama de Hubble Observacional: Pantheon+SH0ES')
plt.legend() #Muestra el cuadro de descripción (gris vs rojo)
plt.grid(True, which="both", ls="-", alpha=0.5) #Cuadrícula

plt.show() #Muestra el gráfico final


# In[20]:


#Paso 5: Gráficas (escala lineal y logarítmica)

plt.figure()

# plt.scatter: Crea un gráfico de puntos. 
# Graficamos todas las supernovas en gris con transparencia (alpha=0.3) para ver la densidad.
# zCMB: Redshift corregido al fondo cósmico de microondas (eje X).
# m_b_corr: Magnitud aparente corregida (eje Y).

#Graficamos todas las supernovas en gris (para que no distraigan)
plt.scatter(df['zCMB'], df['m_b_corr'], s=10, alpha=0.3, color='gray', label='Pantheon+ SN')

#Resaltamos los calibradores en rojo
#Están concentrados en redshifts bajos
plt.scatter(calibradores['zCMB'], calibradores['m_b_corr'], s=25, color='red', label='Calibradores')

# Configuración del gráfico
#plt.xscale('log') # Usamos escala logarítmica para ver mejor el rango de redshift

plt.xlabel('Redshift $z_{CMB}$ (escala lineal)')
plt.ylabel('Magnitud aparente corregida $m_{b,corr}$')
plt.title('Diagrama de Hubble Observacional: Pantheon+SH0ES')
plt.legend() #Muestra el cuadro de descripción (gris vs rojo)
plt.grid(True, which="both", ls="-", alpha=0.5) #Cuadrícula

plt.show() #Muestra el gráfico final


# In[ ]:




