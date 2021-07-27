import csv
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
    else:
        nombre = input("cual es el nombre del archivo?")
        open(nombre,'w')#falta agregar diferentes tipos de archivo
