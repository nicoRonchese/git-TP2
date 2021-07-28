from service_gmail import obtener_servicio
import base64
import zipfile
servicio=obtener_servicio()
fecha_de_hoy='Thu, 22 Jul 2021'
# Call the Gmail API
#https://gmail.googleapis.com/gmail/v1/users/{userId}/messages 
results = servicio.users().messages().list(userId='me',labelIds=['INBOX']).execute()
#https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{id}
#https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{messageId}/attachments/{id}
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
        with open('imagen.zip','wb') as archivo_zip:
            archivo_zip.write(base64.urlsafe_b64decode(zip))  
        descomprimir_archivo_zip=zipfile.ZipFile('imagen.zip','r')
        descomprimir_archivo_zip.extractall()


if not mensajes:
    print('No labels found.')
else:
    print('Messages:')
    for mensajes_gmail in mensajes:
        print(mensajes_gmail)
