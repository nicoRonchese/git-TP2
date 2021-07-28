import os
import csv
import shutil
from service_gmail import obtener_servicio
import base64
import zipfile
 
def ingresar_opcion(opciones: list)->int:
    opcion = 0
    for x in range(len(opciones)):
        print(f"{x + 1} - {opciones[x]}")
    opcion = input("Ingrese una opción: ")
    while not ((opcion.isnumeric) and (int(opcion)<= len(opciones)+1)):
        opcion :input("Ingrese una opción: ")
    return int(opcion)

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

def lector_de_archivos_cvs(datos:list,archivo:str)->None:
    with open(archivo,'r', newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        next(csv_reader) 
        for row in csv_reader:
            str(row).split(",")
            datos.append(row)

def creador_de_carpetas_evaluacion(datos_docente:list,datos_alumnos:list,datos_docente_alumno :list,direccion:str)->None:
    #acortar en lo posible
    alumnos_asignados =list()
    for i in range(len(datos_docente_alumno)):
        if len(datos_docente_alumno[i]) == 2:
            direccion_docentes_alumnos = os.path.join(direccion,datos_docente_alumno[i][0],datos_docente_alumno[i][1])
            os.makedirs(direccion_docentes_alumnos,exist_ok=True)
    organizacion_docentes = os.listdir(direccion)
    for i in range(len(datos_docente)):
        if not(datos_docente[i][0] in organizacion_docentes):
            direccion_docentes_sin_asignar= os.path.join(direccion,"sin asignar","docentes",datos_docente[i][0])
            os.makedirs(direccion_docentes_sin_asignar,exist_ok=True)
    for j in range(len(datos_docente_alumno)):
        alumnos_asignados.append(datos_docente_alumno[j][1])
    for i in range(len(datos_alumnos)):
        if not(datos_alumnos[i][0] in alumnos_asignados):
            dirreccion_alumnos_sin_asignar = os.path.join(direccion,"sin asignar","alumnos",datos_alumnos[i][0])
            os.makedirs(dirreccion_alumnos_sin_asignar,exist_ok=True)

def asignacion_archivos(asunto_mail:str,datos_docente_alumno:list,datos_alumnos:list)->None:
    #falta recibir el mail
    for fila in datos_alumnos:
        if fila[1] == asunto_mail:
            nombre_alumno = fila[0]
    for fila in datos_docente_alumno:
        if fila[1] == nombre_alumno:
            nombre_docente = fila[0]
    direccion = os.getcwd()
    direccion = os.path.join("evaluacion",nombre_docente,nombre_alumno)#falta agregar el nombre de la evaluacion
    shutil.move("nombre_archivo", direccion)#cambiar nombre_archivo por lo que reciba por mail

def api_de_gmail()->None:
    servicio=obtener_servicio()
    results = servicio.users().messages().list(userId='me',labelIds=['INBOX']).execute()
    mensajes = results.get('messages', id)
    for mensaje in mensajes:
        results_2 = servicio.users().messages().get(userId='me',id=mensaje.get('id')).execute()   
        asunto_del_mail=results_2['payload']['headers']
        for i in range(len(asunto_del_mail)):
            if asunto_del_mail[i]['name']=='Subject':
                encontro_el_asunto=asunto_del_mail[i]['value']
        asunto_del_mail_dividido=encontro_el_asunto.split('-')
        if '1ra_Evaluación' in asunto_del_mail_dividido:
            results_3=servicio.users().messages().attachments().get(userId='me',messageId=results_2.get('id'),id=(results_2['payload']['parts'][1]['body']['attachmentId'])).execute()
            zip=results_3['data']
            with open('Parciales.zip','wb') as archivo_zip:
                archivo_zip.write(base64.urlsafe_b64decode(zip))  
            descomprimir_archivo_zip=zipfile.ZipFile('Parciales.zip','r')
            descomprimir_archivo_zip.extractall()
        borrar_mensaje=servicio.users().messages().delete(userId='me',id=results_2.get('id')).execute()

def main():
    datos_docente=list()
    datos_alumnos=list()
    datos_docente_alumno =list()
    evaluacion ="evaluaciones"#vendria el asunto del mail
    direccion = os.getcwd()
    direccion = os.path.join(direccion,evaluacion)
    os.mkdir(evaluacion) 
    opciones = [
      "Listar archivos de la carpeta actual",
      "Crear una carpeta",
      "Crear un archivo",
      "Generar carpetas de una evaluacion",
      "Actualizar entregas de alumnos via mail.",
      "salir"
      ]
    opcion = ingresar_opcion(opciones)
    while not opcion == 6:
        if opcion==1:
            listar_carpetas_archivos()
        elif opcion==2:
            crear_archivo_carpeta("carpeta")
        elif opcion==3:
            crear_archivo_carpeta("archivo")
        elif opcion==4:
            lector_de_archivos_cvs(datos_docente,"docentes.csv")
            lector_de_archivos_cvs(datos_alumnos,"alumnos.csv")
            lector_de_archivos_cvs(datos_docente_alumno,"docente-alumnos.csv")
            creador_de_carpetas_evaluacion(datos_docente,datos_alumnos,datos_docente_alumno,direccion)
        elif opcion==5:
            api_de_gmail()
        opcion = ingresar_opcion(opciones)
               

main()