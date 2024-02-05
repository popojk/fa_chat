from fastapi import FastAPI

class App():

    def __init__(self):
        self.fast_app = FastAPI()

if __name__ == '__main__':
    app = App()
