from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int = Field()
    username: str = Field(...)
    full_name: str = Field(default='test user')
    email: EmailStr = Field(...)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'username': 'spacecat',
                'full_name': 'test user',
                'email': 'test@test.com'
            }
        }


class UserInDB(User):
    hashed_password: str
