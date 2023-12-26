from client import db_client
import bson
def create_fac_tmp(wa_id: str, items: list, cliente: str = None):
    data = {"wa_id": wa_id, "items": items, "cliente": cliente}
    db_client.fac_tmp.insert_one(data)


def agg_pre_fac_tmp(wa_id: str, precio: str):
    items = list(db_client.fac_tmp.find_one({'wa_id':wa_id})["items"])
    items[-1] = items[-1]+" "+precio
    print("--",items)
    
    # Verificar si el primer elemento de 'items' es una lista
    db_client.fac_tmp.update_one({'wa_id': wa_id}, {'$set': {'items': items}})
    
def agg_sab_fac_tmp(wa_id: str, item: str):
    db_client.fac_tmp.update_one({'wa_id':wa_id},{'$push': {'items': item}})

def agg_client_fac_tmp(wa_id: str, cliente: str):
    db_client.fac_tmp.update_one({'wa_id':wa_id},{'$set': {'cliente': cliente}})

def read_fac_tmp_db(wa_id:str):
    #devuelve el json de la factura en tmp
    fac = db_client.fac_tmp.find_one({"wa_id":wa_id})
    print("---readfactmp",fac)
    return fac

def delete_fac_tmp(wa_id: str):
    db_client.fac_tmp.delete_one({"wa_id":wa_id})
    
def create_fac(wa_id: str, items: list, cliente: str):
    data = {"wa_id": wa_id, "items": items, "cliente": cliente}
    db_client.facturas.insert_one(data)
    print("---createfac:",data)

def search_client(wa_id:str):
    client = db_client.clients.find_one({"num":wa_id})
    print("---searchclient:",client)
    return client

def agg_name_client(wa_id:str,name:str):
    db_client.clients.update_one({'num':wa_id},{'$set': {'name': name}})
    print("---aggnameclient",name)
    
def change_client_status(wa_id:str,status:str):
    db_client.clients.update_one({'num':wa_id},{'$set': {'status': status}})
    print("se modifica status:", status)

def create_client(wa_id: str,status:str,cliente: str = None,):
    data = {"num": wa_id, "name": cliente,"status":status}
    db_client.clients.insert_one(data)


def del_item(wa_id:str,item:str):
    result = db_client.fac_tmp.update_one({"wa_id": wa_id}, {"$pull": {"items": item}})
    print(f"Documents matched: {result.matched_count}")
    print(f"Documents modified: {result.modified_count}")




# del_item("584126905101","mora mediano 1.50")


# delete_fac_tmp("PRUEBA2-584126905101")
# create_fac_tmp("wa100",["cereza"])
# agg_sab_fac_tmp("wa100","melon")
# agg_pre_fac_tmp("wa100","1$")
# agg_client_fac_tmp("584126905101","saara")
# agg_name_client("584126905101","pepe")
# read_fac_tmp_db("584126905101")
