from fastapi import FastAPI,Request
from pydantic import BaseModel
from time import sleep
import services_old_old
from requests import get as requestsget
#from routers import products,users,basic_auth_users
app = FastAPI()

#routers
#app.include_router(products.router)
#app.include_router(users.router)
#app.include_router(basic_auth_users.router)

class User(BaseModel):
    entry: dict 
    changes: dict
    value: dict
    message: dict
    number: str
    messageId: str
    contacts: dict
    name: str
    text: str
    text_id: str
    wa_id: str


@app.get("/webhook")
async def api_data(request: Request):
    params = request.query_params
    response = int(params['hub.challenge'])
    return response

@app.post("/tlg")
async def url(request: Request):
    body_b = await request.json()
    print("---se recive: ", body_b) 
  


@app.post('/webhook')
async def recibir_mensajes(request: Request):
    
    body_b = await request.json()
    print("---se recive: ", body_b)
    entry: dict = body_b['entry'][0]
    changes: dict = entry['changes'][0]
    value: dict = changes['value']
    message: dict = value.get('messages', [None])[0]  # Usa el método get para manejar la ausencia de 'messages'
    
    if message is not None:
        number: dict = message['from']
        messageId: dict = message['id']
        text, text_id = services_old_old.obtener_Mensaje_whatsapp(message)
        contacts: dict = value['contacts'][0]
        name: dict = contacts['profile']['name']
        wa_id: dict = contacts['wa_id']
        mensaje = User(entry=entry, changes=changes, value=value, message=message, number=number, messageId=messageId, contacts=contacts, name=name, text=text, text_id=text_id,wa_id=wa_id)
        services_old_old.administrar_chatbot(mensaje)

    else:
        statuses = value["statuses"][0]
        status = statuses["status"]
        return print("---respuesta:",status)


# def administrar_chatbot(mensaje):
#     #print("---- ITEM Y PRECIO AFTER",process.env.ITEM,process.env.PRECIO)
#     # mensaje.text = mensaje.text.lower() #mensaje que envio el usuario el cual ya fue depurado por la funcion obtener mensaje
#     list_data = []
#     print("mensaje del usuario: ",mensaje.text)
#     markRead = markRead_Message(mensaje.messageId)
#     list_data.append(markRead)
#     sleep(2)

#     lista_saludos = ["hola","ey","ola","hey","saludos","buenas","buenas tardes","como estan","","","","","","",""]

#     if text in lista_saludos:
#         print("a")