import csv
import os
def lector_de_archivos_cvs(datos:list,archivo:str)->None:
    with open(archivo,'r', newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        next(csv_reader) 
        for row in csv_reader:
            str(row).split(",")
            datos.append(row)
def creador_de_carpetas_evaluacion(datos_docente:list,datos_alumnos:list,datos_docente_alumno :list,direccion:str)->None:
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


def main()->None:
    evaluacion ="evaluaciones"#vendria el asunto del mail
    direccion = os.getcwd()
    direccion = os.path.join(direccion,evaluacion)
    os.mkdir(evaluacion)   
    datos_docente=list()
    datos_alumnos=list()
    datos_docente_alumno =list()
    lector_de_archivos_cvs(datos_docente,"docentes.csv")
    lector_de_archivos_cvs(datos_alumnos,"alumnos.csv")
    lector_de_archivos_cvs(datos_docente_alumno,"docente-alumnos.csv")
    creador_de_carpetas_evaluacion(datos_docente,datos_alumnos,datos_docente_alumno,direccion)


main()