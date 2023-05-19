from pydantic import BaseModel
from typing import Union

class Item(BaseModel):
    id: int
    name: Union[str, None]
    description: Union[str, None]
    stock: Union[int, None]
    price: Union[float, None]

class ItemRequest(BaseModel):
    name: Union[str, None]
    description: Union[str, None]
    stock: Union[int, None]
    price: Union[float, None]

class ItemBuyRequest(BaseModel):
    itemId: Union[int, None]
    cantidadProducto: Union[int, None]