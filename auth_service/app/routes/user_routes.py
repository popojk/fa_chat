from app.routes.abstracts.abstract_routes import AbstractRoutes
from app.services.file_services import FileServices
from app.services.user_services import UserServices
from app.schemas.user_schema import UserSchema, LoginSchema, AuthenticateSchema
from fastapi import File, UploadFile
from fastapi.params import Body


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
        self.routes.add_api_route(
            '/api/users/authenticate', self.authenticate, methods=['POST']
        )

    def register(self, data: UserSchema):
        new_user = self.user_services.register(data.model_dump())
        return self.handle_response(new_user)

    def login(self, data: LoginSchema):
        user_data = data.model_dump()
        jwt = self.user_services.login(user_data['username'], user_data['password'])
        return self.handle_response(jwt)

    def authenticate(self, data: AuthenticateSchema):
        auth_data = data.model_dump()
        jwt = auth_data['jwt']
        user = self.user_services.authenticate(jwt)
        return self.handle_response(user)

    async def upload_file(self, file: UploadFile = File(...)):
        avatar_path = await self.file_services(file)
