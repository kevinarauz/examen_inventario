from swagger_server.resources.postgres_db import PostgresClient
import json

class ItemRepository():

    def create(self, body):
        response = None
        with PostgresClient() as client:
            response = client.execute_insert('"ITEM"',body)
        return response 
    
    def get_by_id(self, item_id):
        response = None
        with PostgresClient() as client:
            query_select = f'SELECT * FROM "ITEM" WHERE ID={item_id}'
            response = client.execute_query(query_select)
        return response
        
    def get_paginated(self, page, size, name):
        with PostgresClient() as client:
            table = '"ITEM"'
            query = f"SELECT * FROM {table} WHERE name like '%{name}%'"
            response = client.execute_query_paginated(query, page, size)
            return response
    
    def buy_product(self, request, item_id):
        response = None
        with PostgresClient() as client:
            # Verificar si el item existe
            #query_select_id = f'SELECT COUNT(*) FROM "ITEM" WHERE ID={item_id}'
            #item_exists = client.execute_query(query_select_id)
            item_exists = self.get_by_id(item_id)
            #if item_exists[0]['count'] == 0:
            if item_exists is None:
                response = {
                    "message": "El ID del item no existe."
                }
            else:
                # Obtener el item actual
                query_select = f'SELECT * FROM "ITEM" WHERE ID={item_id}'
                current_item = client.execute_query(query_select)

                if current_item:
                    current_stock = current_item[0]['stock']

                    if current_stock == 0:
                        # El stock ya es cero, no se puede comprar más
                        response = {
                            "message": "El stock de este item es cero. No se puede realizar la compra."
                        }
                    elif request['cantidadProducto'] > current_stock:
                        # La cantidad a comprar es mayor al stock disponible
                        response = {
                            "message": "La cantidad a comprar es mayor al stock disponible."
                        }
                    else:
                        # Actualizar la cantidad del stock
                        new_stock = current_stock - request['cantidadProducto']
                        data_update = {
                            "stock": new_stock
                        }
                        client.execute_update('"ITEM"', data_update, 'id = ' + str(item_id))

                        # Obtener el item actualizado
                        query_select_updated = f'SELECT * FROM "ITEM" WHERE ID={item_id}'
                        updated_item = client.execute_query(query_select_updated)

                        response = updated_item[0]

        return response