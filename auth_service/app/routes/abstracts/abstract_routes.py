from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class AbstractRoutes:
    routes = APIRouter()

    def __init__(self):
        pass

    def handle_response(self, data):
        json_compatible_item_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_item_data)