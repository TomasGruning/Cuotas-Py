import webbrowser as web
import pandas as pd
from time import sleep
from datetime import date
from calendar import month_name
import locale
import json
import re

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Carga configuraciones
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

fichero = config["FICHERO"]["ubicacion"]
lista_precios = config["FICHERO"]["lista_precios"]

cuotas_clientes = pd.read_excel(fichero, sheet_name=lista_precios, skiprows=6, usecols=lambda x: "Unnamed" not in x)
dto_familiar = pd.read_excel(fichero, sheet_name=lista_precios).iloc[2, 2]


def mes_proximo():
    mes_actual = date.today().month
    if mes_actual == 12:
        mes_siguiente = 1
    else:
        mes_siguiente = mes_actual + 1

    return month_name[mes_siguiente].upper()

def plantilla_mensaje_cuota(nombre, apellido, curso, cuota_normal, cuota_despues_15):
    mensaje = (f"Estimadas familias: \n\n"
               f"A continuación les detallamos el valor de la cuota a partir del mes de *marzo*\n\n"
               f"🔸 *NOMBRE*: {nombre} {apellido}\n"
               f"🔸 *CURSO*: {curso}\n"
               f"➡️ *CUOTA*: (descuentos por inscripción diciembre y familia ya aplicados)\n\n"
               f" *$ {int(cuota_normal)}*\n (*con bonificación* por pago del 1 al 15 de cada mes; *marzo excepcionalmente hasta 21/03*)\n\n"
               f" *$ {int(cuota_despues_15)}*\n (después del 15 de cada mes)\n\n"
               "Las cuotas pueden ser abonadas en efectivo o por transferencia bancaria. Si se elige esta última modalidad, solicitar CBU o ALIAS en administración. ‼️NO OLVIDAR enviar comprobante de la transferencia al celular del instituto 📱(153575345)\n\n"
               "Ante cualquier duda o inquietud, les pedimos que lo comuniquen a administración.\n\n\n"
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
