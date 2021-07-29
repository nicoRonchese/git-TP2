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
    '''
    POST:imprime en la terminal todas las carpetas de la carpeta en la que uno se encuentra,
    si en la carpeta actual hay carpetas repetira el proceso pero con un | para indicar que son subcarpetas.
    ests se hara nuevamente 
    '''
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
    '''
    PRE:archivo carpeta debe ser una str de valor: carpeta o archivo
    POST:crea un archivo o carpeta sin repetir nombre con los ya existentes en el directorio
    '''
    direccion = os.getcwd()
    lista = os.listdir(direccion)
    nombre = input("cual es el nombre de la %s?"%archivo_carpeta)
    while nombre in lista:
        nombre = input("cual es el nombre de la %s?"%archivo_carpeta)
    if archivo_carpeta == "carpeta":
        os.mkdir(nombre)
    else:
        extencion = input("indeque la exrencion del archivo(.csv,.json,.bin):")
        archivo = nombre+extencion
        if extencion == (".csv" or ".json"):
            open(archivo,'w')
        else:
            open(archivo,'wb')

def lector_de_archivos_cvs(datos:list,archivo:str)->None:
   '''
   PRE:Datos debe ser una lista vacia y
   archivo debe ser una str que representa un archivo csv en la misma carpeta
   POST:Datos tendra toda la informacion en el archivo csv separada por lineas
   '''
   with open(archivo,'r', newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        next(csv_reader) 
        for row in csv_reader:
            str(row).split(",")
            datos.append(row)

def creador_de_carpetas_evaluacion(datos_docente:list,datos_alumnos:list,datos_docente_alumno :list,direccion:str)->None:
    '''
    PRE:datos_docente, datos_alumnos y datos_docente_alumno deben ser listas con datos previamente obtenidosy 
    direccion una str con la direccion de la carpeta actual
    POST:crea carpetas con diferentes niveles de anidacion. Primero una con los docentes con alumnos asigandos,
    luego una carpeta para los no asignados donde se divide entre docentes y alumnos 
    '''
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

def asignacion_archivos(asunto_mail:str,datos_docente_alumno:list)->None:
    '''
    PRE:datos_docente_alumno debe ser una lista con datos previamente obtenidos y 
    asunto mail debe ser un str de formato : 'nombre evaluacion'-padron-apellido,nombre
    deben haberse ya creado las carpetas de evaluacion
    POST:mueve los archivos a su carpeta correspondiente
    '''
    asunto_mail = asunto_mail.split("-")
    nombre_alumno = asunto_mail[3]
    nombre_docente = ""
    for fila in datos_docente_alumno:
        if fila[1] == nombre_alumno:
            nombre_docente = fila[0]
    direccion = os.getcwd()
    if not (nombre_docente == ""):
        direccion = os.path.join(asunto_mail[1],nombre_docente,nombre_alumno)
    else:
        direccion = os.path.join(asunto_mail[1],"sin asignar","alumnos",nombre_alumno)
    nombre_archivo = asunto_mail[2]+"-"+asunto_mail[3]
    shutil.move(nombre_archivo, direccion)

def api_de_gmail(asunto_archivos_csv:list,asuntos_archivos_mails:list)->None:
    '''
   PRE:Recibe las listas para en ellas guardar los asuntos de los csv y de los mails
   POST:Lee lso mensajes que lista del gmail del usuario para en ellos poder encontrar los nombres en los asuntos que previamente se especificaron, es decir que si el asunto no contiene para los csv(1ra_Evaluación) y para las entregas(Entregas), no va a poder leer el mail para poder descargar los archivos dentro de los mails, decodificarlos y luego extraerlos de sus archivos.zip.Al final elimina el mail que se está analizando para que no lo vuelva a buscar la próxima vez que se quiera actualizar las entregas. 
    '''
    servicio=obtener_servicio()
    results = servicio.users().messages().list(userId='me',q='after:2021/07/29',labelIds=['INBOX']).execute()
    mensajes = results.get('messages', id)
    for mensaje in mensajes:
        results_2 = servicio.users().messages().get(userId='me',id=mensaje.get('id')).execute()   
        asunto_del_mail=results_2['payload']['headers']
        for i in range(len(asunto_del_mail)):
            if asunto_del_mail[i]['name']=='Subject':
                encontro_el_asunto=asunto_del_mail[i]['value']
        asunto_del_mail_dividido=encontro_el_asunto.split('-')
        encontro_evaluaciones=True
        while 'Entrega' in asunto_del_mail_dividido and encontro_evaluaciones==True:
                results_3=servicio.users().messages().attachments().get(userId='me',messageId=results_2.get('id'),id=(results_2['payload']['parts'][1]['body']['attachmentId'])).execute()
                zip=results_3['data']
                descomprimir_archivos(zip)
                asuntos_archivos_mails.append(encontro_el_asunto)
                encontro_evaluaciones=False                    
        else:
            if '1ra_Evaluación'in asunto_del_mail_dividido:
                results_3=servicio.users().messages().attachments().get(userId='me',messageId=results_2.get('id'),id=(results_2['payload']['parts'][1]['body']['attachmentId'])).execute()
                zip=results_3['data']
                descomprimir_archivos(zip)
                asunto_archivos_csv.append(encontro_el_asunto)
        borrar_mensaje=servicio.users().messages().delete(userId='me',id=results_2.get('id')).execute()        
    

def descomprimir_archivos(zip:str)->None:
    '''
    PRE:Recibe el url de un archivo .zip.
    POST:Crea un archivo .zip para escribir en él el archivo que se encuentra en el mail, lo decodifica y después extrae el contenido de ese archivo. 
    '''
    with open('Archivos.zip','wb') as archivo_zip:
                archivo_zip.write(base64.urlsafe_b64decode(zip))  
    descomprimir_archivo_zip=zipfile.ZipFile('Archivos.zip','r')
    descomprimir_archivo_zip.extractall()    
def main():
    datos_docente=list()
    datos_alumnos=list()
    datos_docente_alumno =list()    
    asunto_archivos_csv=list()
    asuntos_archivos_mails=list()
    opciones = [
      "Listar archivos de la carpeta actual",
      "Crear una carpeta",
      "Crear un archivo",
      "Generar carpetas de una evaluacion",
      "Actualizar entregas de alumnos via mail.",
      "salir"
      ]
    api_de_gmail(asunto_archivos_csv,asuntos_archivos_mails)
    opcion = ingresar_opcion(opciones)
    while not opcion == 6:
        if opcion==1:
            listar_carpetas_archivos()
        elif opcion==2:
            crear_archivo_carpeta("carpeta")
        elif opcion==3:
            crear_archivo_carpeta("archivo")
        elif opcion==4:
            print(asunto_archivos_csv)
            evaluacion = asunto_archivos_csv[0]
            direccion = os.getcwd()
            direccion = os.path.join(direccion,evaluacion)
            os.mkdir(evaluacion) 
            lector_de_archivos_cvs(datos_docente,"docentes.csv")
            lector_de_archivos_cvs(datos_alumnos,"alumnos.csv")
            lector_de_archivos_cvs(datos_docente_alumno,"docente-alumnos.csv")
            creador_de_carpetas_evaluacion(datos_docente,datos_alumnos,datos_docente_alumno,direccion)
        elif opcion==5:
            api_de_gmail(asunto_archivos_csv,asuntos_archivos_mails)
            for i in asuntos_archivos_mails:
                asignacion_archivos(i,datos_docente_alumno)
        opcion = ingresar_opcion(opciones)
               

main()
