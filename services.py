import sett
import httpx
from db.consultas import create_fac_tmp, agg_sab_fac_tmp, agg_pre_fac_tmp,agg_client_fac_tmp, read_fac_tmp_db,create_fac,delete_fac_tmp
from db.client import db_client


def obtener_Mensaje_whatsapp(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
        text_id = 'nothing'
        return text, text_id

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
        text_id = 'nothing'

    elif typeMessage == 'button':
        text = message['button']['text']
        text_id = 'nothing'

    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
        text_id = message['interactive']['list_reply']['id']

    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
        text_id = message['interactive']['button_reply']['id']

    else:
        text = 'mensaje no procesado'
        text_id = 'nothing'
        # print('ninguna de las anteriores')
    return text, text_id

def enviar_Mensaje_whatsapp(data):  # funcion para enviar mensaje
    whatsapp_token = sett.whatsapp_token
    whatsapp_url = sett.whatsapp_url
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + whatsapp_token}

    print("---se envia", data)
    response = httpx.post(whatsapp_url, data=data, headers=headers,)

def markRead_Message(messageId):
    data = (
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def text_Message(number, text):
    try:
        data = (
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                        "body": text
                }
            }
        )
        return data
    except Exception as e:
        print(e)

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = (
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }

    )
    return data

def img_Message(number, url):
    data = (
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "image",
            "image": {
                "link": url,
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )
    data = (
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Sabores",
                    "sections": [
                        {
                            "title": "Elige",
                            "rows": rows
                        },
                        # {
                        #     "title": title2,
                        #     "rows": rows2
                        # }
                    ]

                }
            }
        }
    )
    return data

def buscar_en_listas(valor, lista1, lista2, lista3):
    if valor in lista1:
        return lista1
    elif valor in lista2:
        return lista2
    elif valor in lista3:
        return lista3
    else:
        return None

def administrar_chatbot(mensaje):
    # print("---- ITEM Y PRECIO AFTER",process.env.ITEM,process.env.PRECIO)
    # mensaje que envio el usuario el cual ya fue depurado por la funcion obtener mensaje
    mensaje.text = mensaje.text.lower()
    list_data = []
    mark_Read = markRead_Message(mensaje.messageId)
    list_data.append(mark_Read)

    lista_saludos = ["hola", "ey", "ola", "hey", "saludos", "buenas",
                     "buenas tardes", "como estan", "", "", "", "", "", "", ""]
    try:
        fac_tmp_db = read_fac_tmp_db(mensaje.wa_id)
        if fac_tmp_db is None: 
            print("no hay factura")
        elif fac_tmp_db["cliente"] == "!":
            #aggregar posible confirmacion de nombre
            try:
                agg_client_fac_tmp(mensaje.wa_id, mensaje.text)
                fac_tmp_db = read_fac_tmp_db(mensaje.wa_id)
                cliente = fac_tmp_db["cliente"]
                items = fac_tmp_db["items"]
                fac_items_str = " ".join(items)
                print("---fac_items",fac_items_str)
                text = f"cliente:{cliente}\n---------------\n{fac_items_str}"
                print(text)
                textmessagedata = text_Message(mensaje.number, text)
                list_data.append(textmessagedata)

                body = "Ya estamos terminando verifique e informe"
                footer = "int C.A."
                options = ["PEDIR", "MODIFICAR"]

                replyButtonData = buttonReply_Message(
                    mensaje.number, options, body, footer, "sed10", mensaje.messageId)
                list_data.append(replyButtonData)
                
                
            except Exception as e:
                print("aqui hubo peo compadre",e)
        # if mensaje.text in lista_saludos:
        #     body = "Gracias por comunicarte con int Terraza 77🤗, podrias indicarnos que es lo que deseas?"
        #     footer = "int C.A."
        #     options = ["HACER UN PEDIDO", "REPORTAR UN PROBLEMA"]

        #     replyButtonData = buttonReply_Message(
        #         mensaje.number, options, body, footer, "sed1", mensaje.messageId)
        #     list_data.append(replyButtonData)
        # hacer un pedido
        if mensaje.text_id == 'sed1_btn_1':
            # hacer un pedido
            document = img_Message(mensaje.number, sett.foto_menu)
            list_data.append(document)

            body = "Aqui tienes nuestro menu cuando este listo para hacer tu pedido pulsa ¡PEDIR!"
            footer = "int C.A."
            options = ["PEDIR"]

            replyButtonData = buttonReply_Message(
                mensaje.number, options, body, footer, "sed2", mensaje.messageId)
            list_data.append(replyButtonData)

        if mensaje.text_id == 'sed1_btn_2':
            # reportar un problema
            text = 'problema reportado'
            textmessagedata = text_Message(mensaje.number, text)
            list_data.append(textmessagedata)
        # boton pedir
        if mensaje.text_id == 'sed2_btn_1':
            body = "Aqui puedes empezar a hacer tu pedido pulsa, ¡selecciona tu sabor preferido!"
            footer = "int C.A."
            options = ["SABORES REGULARES",
                       "SABORES ESPECIALES", "SABORES PREMIUM"]
            listReplyData = listReply_Message(
                mensaje.number, options, body, footer, "sed3", mensaje.messageId)
            list_data.append(listReplyData)

        # tipo de sabor
        if mensaje.text_id == 'sed3_row_1':
            # regulares
            body = "¡Selecciona tu preferido!"
            footer = "int C.A."
            options = ["Colita", "Pina", "Limon", "Parchita", "Guanabana"]
            # options2 =  ["Durazno","Mora","Zapote","Nispero","Fresa","Tamarindo","Mango"]
            listReplyData = listReply_Message(
                mensaje.number, options, body, footer, "sed4", mensaje.messageId)
            list_data.append(listReplyData)

        elif mensaje.text_id == 'sed3_row_2':
            # especiales
            body = "¡Selecciona tu preferido!"
            footer = "int C.A."
            options = sett.sabores_especiales
            listReplyData = listReply_Message(
                mensaje.number, options, body, footer, "sed5", mensaje.messageId)
            list_data.append(listReplyData)

        elif mensaje.text_id == 'sed3_row_3':
            # premium
            body = "¡Selecciona tu preferido!"
            footer = "int C.A."
            options = sett.sabores_premium
            listReplyData = listReply_Message(
                mensaje.number, options, body, footer, "sed6", mensaje.messageId)
            list_data.append(listReplyData)

        # eleccion sabores
        if mensaje.text_id.split("_")[0] == 'sed4':
            items_fac = read_fac_tmp_db(mensaje.wa_id)
            if items_fac is None:
                    print("no existe, se crea factura")
                    lista_mensaje = []
                    lista_mensaje.append(mensaje.text)
                    create_fac_tmp(mensaje.wa_id, lista_mensaje)
                    # se envia precio
                    if mensaje.text in sett.sabores_regulares:
                        body = "Que tamaño prefieres?"
                        footer = "int C.A."
                        options = sett.obtener_precios(
                                    sett.tamanos, sett.precios_regulares)
                        listReplyData = listReply_Message(
                                    mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                        list_data.append(listReplyData)
                        
            elif items_fac["items"][-1] in sett.sabores_regulares and mensaje.text in sett.sabores_regulares:
                    print("dos veces sabores")
                    # enviar precio
                    ult_sab = items_fac["items"][-1]
                    text = f"por favor ingrese el precio para el ultimo sabor ingresado: {ult_sab}"
                    textmessagedata = text_Message(mensaje.number, text)
                    list_data.append(textmessagedata)
                    body = "Que tamaño prefieres?"
                    footer = "int C.A."
                    options = sett.obtener_precios(
                        sett.tamanos, sett.precios_regulares)
                    listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                    list_data.append(listReplyData)
            
            elif mensaje.text in sett.sabores_regulares:
                    agg_sab_fac_tmp(mensaje.wa_id, mensaje.text)

                    body = "Que tamaño prefieres?"
                    footer = "int C.A."
                    options = sett.obtener_precios(
                                sett.tamanos, sett.precios_regulares)
                    listReplyData = listReply_Message(
                                mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                    list_data.append(listReplyData)

        if mensaje.text_id.split("_")[0] == 'sed5':
            items_fac = read_fac_tmp_db(mensaje.wa_id)
            if items_fac is None:
                print("no existe, se crea factura")
                lista_mensaje = []
                lista_mensaje.append(mensaje.text)
                create_fac_tmp(mensaje.wa_id, lista_mensaje)
                # se envia precio
                if mensaje.text in sett.sabores_especiales:
                        body = "Que tamaño prefieres?"
                        footer = "int C.A."
                        options = sett.obtener_precios(
                                    sett.tamanos, sett.precios_regulares)
                        listReplyData = listReply_Message(
                                    mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                        list_data.append(listReplyData)
            
            elif items_fac["items"][-1] in sett.sabores_especiales and mensaje.text in sett.sabores_especiales:
                    print("dos veces sabores")
                    # enviar precio
                    ult_sab = items_fac["items"][-1]
                    text = f"por favor ingrese el precio para el ultimo sabor ingresado: {ult_sab}"
                    textmessagedata = text_Message(mensaje.number, text)
                    list_data.append(textmessagedata)
                    body = "Que tamaño prefieres?"
                    footer = "int C.A."
                    options = sett.obtener_precios(
                        sett.tamanos, sett.precios_especiales)
                    listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                    list_data.append(listReplyData)
            elif mensaje.text in sett.sabores_especiales:
                agg_sab_fac_tmp(mensaje.wa_id, mensaje.text)

                body = "Que tamaño prefieres?"
                footer = "int C.A."
                options = sett.obtener_precios(
                        sett.tamanos, sett.precios_especiales)
                listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                list_data.append(listReplyData)
                    
        if mensaje.text_id.split("_")[0] == 'sed6':
            items_fac = read_fac_tmp_db(mensaje.wa_id)
            if items_fac is None:
                print("no existe, se crea factura")
                lista_mensaje = []
                lista_mensaje.append(mensaje.text)
                create_fac_tmp(mensaje.wa_id, lista_mensaje)
                # se envia precio
                if mensaje.text in sett.sabores_premium:
                        body = "Que tamaño prefieres?"
                        footer = "int C.A."
                        options = sett.obtener_precios(
                                    sett.tamanos, sett.precios_regulares)
                        listReplyData = listReply_Message(
                                    mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                        list_data.append(listReplyData)
            
            elif items_fac["items"][-1] in sett.sabores_premium and mensaje.text in sett.sabores_premium:
                    print("dos veces sabores")
                    ult_sab = items_fac["items"][-1]
                    text = f"por favor ingrese el precio para el ultimo sabor ingresado: {ult_sab}"
                    # text = f"por favor ingrese el precio para el ultimo sabor ingresado: error"
                    textmessagedata = text_Message(mensaje.number, text)
                    list_data.append(textmessagedata)
                    body = "Que tamaño prefieres?"
                    footer = "int C.A."
                    options = sett.obtener_precios(
                        sett.tamanos, sett.precios_premium)
                    listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                    list_data.append(listReplyData)

            if mensaje.text in sett.sabores_premium:
                agg_sab_fac_tmp(mensaje.wa_id, mensaje.text)
                body = "Que tamaño prefieres?"
                footer = "int C.A."
                options = sett.obtener_precios(
                        sett.tamanos, sett.precios_premium)
                listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                list_data.append(listReplyData)
                    #seleccion precios
        
        if mensaje.text_id.split("_")[0] == 'sed7':
            # aqui vamos a validar que exista un sabor agregado y si existe agregar precio correspondiente
            items_fac = read_fac_tmp_db(mensaje.wa_id)["items"]

            # aqui validamos que el ultimo mensaje este dentro de regulares
            if items_fac[-1] in sett.sabores_regulares:
                print("entro en sabores regulares")
                if mensaje.text in sett.obtener_precios(sett.tamanos, sett.precios_regulares):
                    print("el precio coincide")
                    agg_pre_fac_tmp(mensaje.wa_id, mensaje.text)
                    body = "Estas listo?"
                    footer = "int C.A."
                    options = ["AGREGAR OTRO", "TERMINAR PEDIDO"]

                    replyButtonData = buttonReply_Message(
                        mensaje.number, options, body, footer, "sed8", mensaje.messageId)
                    list_data.append(replyButtonData)
                else:
                    print("el precio no coincide")
                    items_fac = read_fac_tmp_db(mensaje.wa_id)["items"]
                    text = f"por favor ingrese el precio para el ultimo sabor ingresado {items_fac[-1]}"
                    textmessagedata = text_Message(mensaje.number, text)
                    list_data.append(textmessagedata)
                    body = "Que tamaño prefieres?"
                    footer = "int C.A."
                    options = sett.obtener_precios(
                        sett.tamanos, sett.precios_regulares)
                    listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                    list_data.append(listReplyData)
            # aqui validamos que el ultimo mensaje este dentro de especiales
            if items_fac[-1] in sett.sabores_especiales:
                if mensaje.text in sett.obtener_precios(sett.tamanos, sett.precios_especiales):
                    agg_pre_fac_tmp(mensaje.wa_id, mensaje.text)
                    body = "Estas listo?"
                    footer = "int C.A."
                    options = ["AGREGAR OTRO", "TERMINAR PEDIDO"]

                    replyButtonData = buttonReply_Message(
                        mensaje.number, options, body, footer, "sed8", mensaje.messageId)
                    list_data.append(replyButtonData)
                else:
                    text = f"por favor ingrese el precio para el ultimo sabor ingresado {items_fac[-1]}"
                    textmessagedata = text_Message(mensaje.number, text)
                    list_data.append(textmessagedata)
                    body = "Que tamaño prefieres?"
                    footer = "int C.A."
                    options = sett.obtener_precios(
                        sett.tamanos, sett.precios_especiales)
                    listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                    list_data.append(listReplyData)
            # aqui validamos que el ultimo mensaje este dentro de premium
            if items_fac[-1] in sett.sabores_premium:
                if mensaje.text in sett.obtener_precios(sett.tamanos, sett.precios_premium):
                    agg_pre_fac_tmp(mensaje.wa_id, mensaje.text)
                    body = "Estas listo?"
                    footer = "int C.A."
                    options = ["AGREGAR OTRO", "TERMINAR PEDIDO"]

                    replyButtonData = buttonReply_Message(
                        mensaje.number, options, body, footer, "sed8", mensaje.messageId)
                    list_data.append(replyButtonData)
                else:
                    text = f"por favor ingrese el precio para el ultimo sabor ingresado {items_fac[-1]}"
                    textmessagedata = text_Message(mensaje.number, text)
                    list_data.append(textmessagedata)
                    body = "Que tamaño prefieres?"
                    footer = "int C.A."
                    options = sett.obtener_precios(
                        sett.tamanos, sett.precios_premium)
                    listReplyData = listReply_Message(
                        mensaje.number, options, body, footer, "sed7", mensaje.messageId)
                    list_data.append(listReplyData)
            # aqui validamos que el ultimo mensaje no este en en ninguna de las anteriores nuevamente para imprimir el mensaje de seleccion de sabor
            if items_fac[-1] not in sett.sabores_especiales and items_fac[-1] not in sett.sabores_regulares and items_fac[-1] not in sett.sabores_premium:
                text = f"por favor elija un sabor"
                textmessagedata = text_Message(mensaje.number, text)
                list_data.append(textmessagedata)
                body = "Aqui puedes empezar ahacer tu pedido pulsa, ¡selecciona tu sabor preferido!"
                footer = "int C.A."
                options = ["SABORES REGULARES",
                           "SABORES ESPECIALES", "SABORES PREMIUM"]
                listReplyData = listReply_Message(
                    mensaje.number, options, body, footer, "sed3", mensaje.messageId)
                list_data.append(listReplyData)
        #seleccion continuar modificar
        if mensaje.text_id == 'sed8_btn_1':
            mensaje.text = "pedir"
            mensaje.text_id = "sed2_btn_1"
            administrar_chatbot(mensaje)

        if mensaje.text_id == 'sed8_btn_2':

            mensaje.text = 'por favor confirme que este todo en su pedido'
            textmessagedata = text_Message(mensaje.number, mensaje.text)
            list_data.append(textmessagedata)

            items_fac = read_fac_tmp_db(mensaje.wa_id)["items"]
            fac = "\n".join(items_fac)
            textmessagedata = text_Message(mensaje.number, str(fac))
            list_data.append(textmessagedata)
            # print("---FAC", fac)

            body = "Estas listo?"
            footer = "int C.A."
            options = ["CONFIRMAR PEDIDO"]
            replyButtonData = buttonReply_Message(
                mensaje.number, options, body, footer, "sed9", mensaje.messageId)
            list_data.append(replyButtonData)

            # backend.insert(read_item_fac_tmp("fac_tmp.txt"))
        
        #datos factura
        if mensaje.text_id == "sed9_btn_1":
            mensaje.text = 'nos podria indicar su nombre?'
            textmessagedata = text_Message(mensaje.number, mensaje.text)
            list_data.append(textmessagedata)

            agg_client_fac_tmp(mensaje.wa_id, "!")

        if mensaje.text_id == "sed10_btn_1":
            #creado factura
            factura = read_fac_tmp_db(mensaje.wa_id)
            create_fac(factura["wa_id"],factura["items"],factura["cliente"])
            #borrar factura vieja
            delete_fac_tmp(mensaje.wa_id)            
            mensaje.text = 'su pedido ha sido concretado, espere su delivery'
            textmessagedata = text_Message(mensaje.number, mensaje.text)
            list_data.append(textmessagedata)


    except Exception as e:
        error = 'algo salio mal, except'
        print(e, error)

    for item in list_data:
        enviar_Mensaje_whatsapp(item)
