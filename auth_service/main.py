from fastapi import FastAPI
from app.routes.user_routes import UserRoutes
from app.middlewares.exception import ExceptionHandlerMiddleware
from app.middlewares.timer import RequestProcessMiddleware

import uvicorn

class App():

    def __init__(self):
        self.the_api = FastAPI()

    def initialize(self):
        self.user_routes = UserRoutes()
        self.the_api.include_router(self.user_routes.routes)

the_app = App()
the_app.initialize()
the_app.the_api.add_middleware(ExceptionHandlerMiddleware)
the_app.the_api.add_middleware(RequestProcessMiddleware)

if __name__ == '__main__':
    uvicorn.run("main:the_app.the_api", host='0.0.0.0', port=8100, reload=True)
