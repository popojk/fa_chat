from fastapi import FastAPI

import uvicorn

class App():

    def __init__(self):
        self.the_api = FastAPI()

    def initialize(self):
        pass

the_app = App()
the_app.initialize()
api = the_app.the_api

if __name__ == '__main__':
    uvicorn.run("main:the_app.the_api", host='0.0.0.0', port=8200, reload=True)