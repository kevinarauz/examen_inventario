from swagger_server.utils.logging import log as logging
from swagger_server.repository.item_repository import ItemRepository
from swagger_server.models.item_model import Item

from pydantic import parse_obj_as
from typing import List

class ItemUseCase():

    def __init__(self):
        log = logging()
        self.item_repository = ItemRepository()
        self.log = log

    def save(self, request):
        response = None
        data = self.item_repository.create(request.dict())
        response = parse_obj_as(Item, data)
        return response
    
    def get_item(self, item_id):
        response = self.item_repository.get_by_id(item_id)
        data = None
        if response:
            data = parse_obj_as(Item, response[0])
        return data
    
    def get_paginated(self, page, size, name):
        response = self.item_repository.get_paginated(page, size, name)
        if not response:
            return []  # Retorna una lista vacía si no hay datos encontrados
        items= parse_obj_as(List[Item], response)
        return items
    
    def buy_product(self, request, item_id):
        response = self.item_repository.buy_product(request.dict(), item_id)
        return response