from pydantic import BaseModel, field_validator

class UserSchema(BaseModel):
    name: str
    password: str

    @field_validator('name')
    def name_cannot_be_null(cls, v):
        if v is None:
            raise ValueError('Name cannot be null!')
        return v
    
    @field_validator('password')
    def password_cannot_be_null(cls, v):
        if v is None:
            raise ValueError('Password cannot be null!')
        return v

class LoginSchema(BaseModel):
    username: str
    password:str

    @field_validator('username')
    def username_cannot_be_null(cls, v):
        if v is None:
            raise ValueError('Username cannot be null!')
        return v
    
    @field_validator('password')
    def password_cannot_be_null(cls, v):
        if v is None:
            raise ValueError('Password cannot be null!')
        return v

class AuthenticateSchema(BaseModel):
    jwt: str

    @field_validator('jwt')
    def jwt_cannot_be_null(cls, v):
        if v is None:
            raise ValueError('JWT cannot be null!')
        return v    
