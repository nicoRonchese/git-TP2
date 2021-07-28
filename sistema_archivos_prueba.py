import shutil
import os
def listar_carpetas_archivos()->None:
    #acortar en lo posible
    direccion = os.getcwd()
    lista = os.listdir(direccion)
    for carpeta in lista:
        print(carpeta)
        direccion1= os.path.join(direccion,carpeta)
        if  os.path.isdir(direccion1):
            lista1 = os.listdir(direccion1)
            for carpeta1 in lista1:
                print("|",carpeta1)
                direccion2= os.path.join(direccion1,carpeta1)
                if  os.path.isdir(direccion2):
                    lista2 = os.listdir(direccion2)
                    for carpeta2 in lista2:
                        print(" |",carpeta2)
def crear_archivo_carpeta(archivo_carpeta:str)->None:
    if archivo_carpeta == "carpeta":
        nombre = input("cual es el nombre de la carpeta?")
        os.mkdir(nombre)
    else:#falta agregar diferentes tipos de archivo
        nombre = input("cual es el nombre del archivo?")
        extencion = input("indeque la exrencion del archivo(.csv,.json,.bin):")
        archivo = nombre+extencion
        if extencion == (".csv" or ".json"):
            open(archivo,'w')
        else:
            open(archivo,'wb')
def asignacion_archivos(asunto_mail:str,datos_docente_alumno:list,datos_alumnos:list)->None:#falta recibir el mail
    for fila in datos_alumnos:
        if fila[1] == asunto_mail:
            nombre_alumno = fila[0]
    for fila in datos_docente_alumno:
        if fila[1] == nombre_alumno:
            nombre_docente = fila[0]
    direccion = os.getcwd()
    direccion = os.path.join("evaluacion",nombre_docente,nombre_alumno)#falta agregar el nombre de la evaluacion
    shutil.move("nombre_archivo", direccion)
