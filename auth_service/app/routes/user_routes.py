from routes.abstracts.abstract_routes import AbstractRoutes
from services.file_services import FileServices
from services.user_services import UserServices
from fastapi import File, UploadFile, Body


class UserRoutes(AbstractRoutes):

    def __init__(self):

        self.file_services = FileServices()
        self.user_services = UserServices()

        self.routes.add_api_route(
            '/api/users', self.register, methods=['POST']
        )
        self.routes.add_api_route(
            '/api/users/upload', self.upload_file, methods=['POST'])
        self.routes.add_api_route(
            '/api/users/login', self.login, methods=['POST']
        )

    def register(self, data: dict = Body(...,
                                         title='Request Body',
                                         )):
        new_user = self.user_services.register(data)
        return self.handle_response(new_user)
    
    def login(self, data: dict = Body(...,
                                         title='Request Body',
                                         )):
        user = self.user_services.login(data['username'], data['password'])
        return self.handle_response(user)

    async def upload_file(self, file: UploadFile = File(...)):
        avatar_path = await self.file_services(file)
