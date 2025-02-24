# WhatsApp AutoMessenger para Instituto de Inglés 📩

Este programa automatiza el envío de mensajes de WhatsApp a los padres de los estudiantes de un instituto de inglés, permitiendo enviar recordatorios de pagos, notas y otras notificaciones de manera eficiente.

Por el momento, está estructurado para un mensaje y una planilla de cálculo en específico.

> [!TIP]
> La librería _pyautogui_ puede generar un error al ejecutar el programa. Para esto, es necesario ejecutar `xhost +` antes.

## ✨ Características

✅ Envío automático de mensajes personalizados a través de WhatsApp.  
✅ Importación de datos desde archivos Excel o una base de datos.  
✅ Configuración flexible mediante un archivo `config.json`.  

## Uso
```bash
usage: Mensajes de Cuotas [-h] [-r STR STR] [-p] [-t [INT]] [-st STR STR] [-c INT INT] [-pc]

 Extrae los clientes y sus respectivas cuotas de un .xlsx
 y manda a cada madre y padre un mensaje por Whatsapp Web

options:
  -h, --help            show this help message and exit

Opciones Generales:
  -r STR STR, --range STR STR
                        ejecuta apartir del alumno ingresado
  -p, --print           imprime la lista de alumnos

Opciones de Pruebas:
  -t [INT], --test [INT]
                        imprime las cuotas de INT alumnos aleatorios
  -st STR STR, --single-test STR STR
                        imprime el mensaje de un alumno en especifico

Opciones de Coordenadas:
  -c INT INT, --coordinates INT INT
                        toma como parametro las cordenadas del mouse
  -pc, --print-coordinates
                        imprime las cordenadas del puntero
```

## ⚙️ Dependencias

* _pandas_: Manejo de planillas de cálculo.
* _pyautogui_: Interacción con el puntero del sistema.

### Instalación
```bash
pip install pandas pyautogui
```

## 🛠️ Formato del `config.json`

El archivo `config.json` permite definir la ubicación del fichero de datos, el número de teléfono del instituto y una lista de alumnos excluidos del envío. Asegúrate de completar este archivo antes de ejecutar el programa.

### 📋 **Ejemplo de `config.json`**
```json
{
    "FICHERO": {
        "ubicacion": "./archivo.xlsx",
        "lista_precios": "Nombre de la hoja dentro del archivo Excel"
    },
    "TEL_INSTITUTO": 3410000000,
    "ALUMNOS_EXCLUIDOS": ["apellidos"]
}
```
  ```

