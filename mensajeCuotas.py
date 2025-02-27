import libreria as lb
import pandas as pd
import argparse
import random
import json

B = '\033[0;m'
R = '\x1b[1;31m'
V = '\x1b[1;32m'
A = '\x1b[1;33m'

def positive_integer(value):
    valuei = int(value)
    if valuei <= 0:
        raise argparse.ArgumentTypeError("%s no es un entero positivo\n" % value)
    return valuei

class Cliente:
    def __init__(self, nombre, apellido, curso, telefono_mm, telefono_pp, activo, inscripcion_dic, dto_familiar):
        self.nombre = nombre
        self.apellido = apellido
        self.curso = curso
        self.telefono_mm = self.limpiar_telefono(str(telefono_mm))
        self.telefono_pp = self.limpiar_telefono(str(telefono_pp))
        self.activo = activo
        self.inscripcion_dic = inscripcion_dic
        self.dto_familiar = dto_familiar

    def limpiar_telefono(self, telefono):
        # Remover caracteres no numéricos
        telefono_limpio = ''.join(c for c in telefono if c.isdigit())
        return telefono_limpio

    def __str__(self):
        return (
            f"{V}Nombre{B}: {self.apellido} {self.nombre}, "
            f"{V}Curso{B}: {self.curso}, "
            f"{V}Teléfono Madre{B}: {'\x1B[41m' if self.telefono_mm == None else ''}{self.telefono_mm}{B}, "
            f"{V}Teléfono Padre{B}: {'\x1B[41m' if self.telefono_pp == None else ''}{self.telefono_pp}{B}, "
            f"{V}Activo?{B}: {self.activo}, "
            f"{V}dic?{B}: {self.inscripcion_dic}, "
            f"{V}dto Familiar?{B}: {self.dto_familiar}{B}"
        )

# Carga configuraciones
with open("config.json") as f:
    config = json.load(f)

telefono_instituto = config["TEL_INSTITUTO"]
alumnos_excluidos = config["ALUMNOS_EXCLUIDOS"]

# Crear instancias de la clase Cliente para cada fila en los datos combinados
clientes_raw = []
for index, row in lb.datos_clientes.iterrows():
    cliente = Cliente(
        row['NOMBRE'], 
        row['APELLIDO'], 
        row['CURSO'], 
        row['celular madre'], 
        row['celular padre'], 
        row['activo?'], 
        row['inscripción en dic?'], 
        row['dto familiar?']
    )
    clientes_raw.append(cliente)

# Filtra los clientes    
clientes_raw = [
    cliente for cliente in clientes_raw 
    if not pd.isnull(cliente.nombre)
    and not pd.isnull(cliente.apellido) 
    and not pd.isnull(cliente.curso) 
    and cliente.activo
    and not cliente.apellido in alumnos_excluidos
]

# Filtro de alumnos repetidos
clientes = []
vistos = set()

for cliente in clientes_raw:
    clave = (cliente.nombre, cliente.apellido)
    if clave not in vistos:
        clientes.append(cliente)
        vistos.add(clave)

# Correcciones manuales de la base
for cliente in clientes:
    if cliente.telefono_mm == '':
        cliente.telefono_mm = None
    if cliente.telefono_pp == '':
        cliente.telefono_pp = None

# F L A G S
parser = argparse.ArgumentParser(
            prog='Mensajes de Cuotas',
            description=
                " Extrae los clientes y sus respectivas cuotas de un .xlsx\n"
                " y manda a cada madre y padre un mensaje por Whatsapp Web",
            formatter_class=argparse.RawTextHelpFormatter)

# Grupo de Opciones Generales
general_group = parser.add_argument_group('Opciones Generales')
general_group.add_argument('-r', '--range', type=str, nargs=2, metavar='STR', 
                           help='ejecuta apartir del alumno ingresado')
general_group.add_argument('-p', '--print', action='store_true', 
                           help='imprime la lista de alumnos')

# Grupo de Opciones de Pruebas
test_group = parser.add_argument_group('Opciones de Pruebas')
test_group.add_argument('-t', '--test', type=positive_integer, nargs='?', metavar='INT', const=3, 
                             help='imprime las cuotas de INT alumnos aleatorios')
test_group.add_argument('-st', '--single-test', type=str, nargs=2, metavar='STR', 
                             help='imprime el mensaje de un alumno en especifico')

# Grupo de Opciones de Coordenadas
coord_group = parser.add_argument_group('Opciones de Coordenadas')
coord_group.add_argument('-c', '--coordinates', type=int, nargs=2, metavar='INT', 
                             help='toma como parametro las cordenadas del mouse')
coord_group.add_argument('-pc', '--print-coordinates', action='store_true', 
                             help='imprime las cordenadas del puntero')

# Parsear los argumentos
args = parser.parse_args()

if args.test is not None and args.single_test is not None:
    parser.error("Las opciones -t y -st no pueden ser usadas al mismo tiempo")
if args.coordinates is not None and args.print_coordinates is not None:
    print(args.coordinates, args.print_coordinates)
    parser.error("Las opciones -c y -pc no pueden ser usadas al mismo tiempo") 

if args.range:
    encontrado = False
    for cliente in clientes[:-1]:
        if cliente.nombre == args.range[1].upper() and cliente.apellido == args.range[0].upper():
            encontrado = True
            clientes = clientes[clientes.index(cliente)+1:]
            break
    if not encontrado:
        parser.error(f'No se encontro el/la alumno/a {args.range[0]} {args.range[1]}')

if args.print:
    for cliente in clientes:
        print(cliente, '\n')
if args.print_coordinates:
    lb.conseguir_mouse()

mx, my = 971, 986
if args.coordinates:
    print('ahh')
    mx, my = args.coordinates[0], args.coordinates[1]

if args.test:
    clientes_aleatorios = random.sample(clientes, args.test)

    for cliente in clientes_aleatorios:
        cuota, cuota_dic = lb.calcular_cuota(cliente)
        print('')
        print(cliente)
        print("-----------------------------")
        print("Cuota normal:     ", '$', int(cuota))
        print("Cuota despues 15: ", '$', int(cuota_dic))
if args.single_test:
    for cliente in clientes:
        encontrado = False
        if cliente.nombre == args.single_test[1].upper() and cliente.apellido == args.single_test[0].upper():
            cuota, cuota_dic = lb.calcular_cuota(cliente)
            print('\n', cliente, '\n\n')
            print(lb.plantilla_mensaje_cuota(cliente.nombre, cliente.apellido, cliente.curso, cuota, cuota_dic, '\n'))
            encontrado = True
            break
    if not encontrado:
        print('\nNo se encontro al alumno')

# M A I N
if not args.test and not args.single_test and not args.print and not args.print_coordinates:
    for cliente in clientes:        
        cuota, cuota_dic = lb.calcular_cuota(cliente)
        mensaje = lb.plantilla_mensaje_cuota(cliente.nombre, cliente.apellido, cliente.curso, cuota, cuota_dic)
        
        print("\nMama:", cliente.apellido + ' ' + cliente.nombre + ' |', cliente.telefono_mm, end='', flush=True)
        if cliente.telefono_mm: 
            if len(str(cliente.telefono_mm)) != 10 or cliente.telefono_mm[0:3] != '341':
                print(A, " (*) El numero de telefono de la madre no parece ser valido", B, end='')
            #lb.mandar_mensaje(cliente.telefono_mm, mensaje, mx, my)

        print("\nPapa:", cliente.apellido + ' ' + cliente.nombre + ' |', cliente.telefono_pp, end='', flush=True)
        if cliente.telefono_pp:
            if len(str(cliente.telefono_pp)) != 10 or cliente.telefono_pp[0:3] != '341':
                print(A, " (*) El numero de telefono del padre no parece ser valido", B, end='')
            #lb.mandar_mensaje(cliente.telefono_pp, mensaje, mx, my)

        if not cliente.telefono_mm and not cliente.telefono_pp:
            print(R, '\n(*) No tiene telefono registrado, enviando a Carnaby', B, end='')
            #lb.mandar_mensaje(telefono_instituto, mensaje, mx, my)

        
        print('')
print('\n')
