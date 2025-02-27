import webbrowser as web
import pyautogui as pg
import pandas as pd
from time import sleep
from datetime import date
from calendar import month_name
import json
import locale
import re

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Carga configuraciones
with open("config.json") as f:
    config = json.load(f)

fichero = config["FICHERO"]["ubicacion"]
lista_precios = config["FICHERO"]["lista_precios"]

datos_clientes = pd.read_excel(fichero, sheet_name='listado maestro de alumnos', skiprows=3, usecols=lambda x: "Unnamed" not in x)
cuotas_clientes = pd.read_excel(fichero, sheet_name=lista_precios, skiprows=6, usecols=lambda x: "Unnamed" not in x)
dto_familiar = pd.read_excel(fichero, sheet_name=lista_precios).iloc[2, 2]


def mes_proximo():
    mes_actual = date.today().month
    if mes_actual == 12:
        mes_siguiente = 1
    else:
        mes_siguiente = mes_actual + 1

    return month_name[mes_siguiente].upper()

def plantilla_mensaje_cuota(nombre, apellido, curso, cuota_normal, cuota_despues_15, sl="%0A"):
    mensaje = (f"Estimadas familias: {sl}{sl}"
               f"A continuación les detallamos el valor de la cuota a partir del mes de *{mes_proximo()}*{sl}{sl}"
               f"🔸 *NOMBRE*: {nombre} {apellido}{sl}"
               f"🔸 *CURSO*: {curso}{sl}"
               f"➡️ *CUOTA*: (descuentos por inscripción diciembre y familia ya aplicados){sl}{sl}"
               f" *$ {int(cuota_normal)}*{sl} (*con bonificación* por pago del 1 al 15 de cada mes){sl}{sl}"
               f" *$ {int(cuota_despues_15)}*{sl} (después del 15 de cada mes){sl}{sl}{sl}"
               "*_Carnaby_*")
    
    return mensaje

def buscarv(valor_buscar, dataframe, columna_busqueda, columna_retorno):
    """
    Parámetros:
        valor_buscar (str): El valor que se quiere buscar en la columna.
        dataframe (DataFrame): El DataFrame de pandas donde se realizará la búsqueda.
        columna_busqueda (str): El nombre de la columna donde se buscará el valor.
        columna_retorno (str): El nombre de la columna cuyo valor se retornará cuando se encuentre una coincidencia.
    """
    for index, row in dataframe.iterrows():
        if row[columna_busqueda].lower() == valor_buscar:
            return row[columna_retorno]
    return None

def calcular_cuota(cliente):
    nombre_completo = cliente.nombre + ' ' + cliente.apellido
    
    if cliente.inscripcion_dic:
        cuota = buscarv(cliente.curso.lower().strip(), cuotas_clientes, 'CURSO', 'dto dic del 1 al 15')
        cuota_dic = buscarv(cliente.curso.lower().strip(), cuotas_clientes, 'CURSO', 'dto dic / pago dsp del día 15')   
    else:
        cuota = buscarv(cliente.curso.lower().strip(), cuotas_clientes, 'CURSO', 'lista del 1 al 15')
        cuota_dic = buscarv(cliente.curso.lower().strip(), cuotas_clientes, 'CURSO', 'NORMAL')
    
    if cliente.dto_familiar:
        cuota -= dto_familiar
        cuota_dic -= dto_familiar

    return cuota, cuota_dic

def conseguir_mouse():
    print('\nColoque el puntero en la barra de mensajes', flush=True, end='')
    sleep(.5)
    print('.', end='', flush=True)
    sleep(1)
    print('.', end='', flush=True)
    sleep(1)
    print('.')
    sleep(1.5)
    print(pg.position())

def mandar_mensaje(telefono, mensaje, x=953, y=964):
    web.open("https://web.whatsapp.com/send?phone=+54" + telefono + "&text=" + mensaje)
    sleep(10)
    pg.click(x,y)           # Hacer click en la caja de texto
    sleep(2.5)            
    pg.press('enter')       # Enviar mensaje 
    sleep(1.3)           
    pg.hotkey('ctrl', 'w')  # Cerrar la pestaña
    sleep(1)
    pg.press('enter')
    sleep(2)
