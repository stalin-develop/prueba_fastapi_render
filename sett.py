#token access api meta
token = 'Pulzar'
whatsapp_token = 'stalinEAACZA28WmERoBOZBJIUzkGXcDhnZCZCbmnqo1GF6LgQqX2ZAm6oInfhxWm69VhhcMcVy4oEUSFpxcsEgisw6xJF3qxRDT3bIDlwFbRw3VZBqI8Bbi2QWLt5kxNKZCtNDKpTLEeAaRoZCqBQhOjgLDY2TmPqQU1ZAyk00yDfIBZAnOP5OO9lTKbW2J2OtZBtzaQCxk369BotoY2ac5dWvgKt'
whatsapp_url = 'https://graph.facebook.com/v17.0/126522520542374/messages'

foto_menu = "https://cdn.glitch.global/c048304a-b649-4511-a3d2-bbcddd36d857/menu_sno.jpeg?v=1695501917506"
foto_payment_mobile = "https://cdn.glitch.global/2692af79-0217-4995-96b3-7da94e2c294d/pago-movil.svg?v=1703168434977"

sabores_regulares = ["colita","pina","limon","parchita","guanabana","durazno","mora","zapote","nispero","fresa"] 
sabores_especiales = ['leche',"cafe","chocolate","chicha"]
sabores_premium = ["crema real","camba","coco","cocosette","oreo","ron pasas","nutella","pirulin","mani"]

TOKEN_TLG = "6827263744:AAFtsakWdxlWYP2-q0GdeSkYIiFfZ7CzEXQ"
CHAT_ID = 2005564517

# precios
tamanos = ["pequeño","mediano","grande","extra grande","gigante"]
precios_regulares = ["1.00","1.50","1.80","2.70","3.50"]
precios_especiales = ["1.40","2.00","2.50","3.50","4.50"]
precios_premium = ["1.80","2.40","3.00","4.30","5.50"]

def obtener_precios(tamanos,lista):
    precios = []
    for i, tamano in enumerate(tamanos):
        precios.append(tamano+" "+lista[i])
    return precios