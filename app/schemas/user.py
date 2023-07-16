from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Read from DB user pydantic schema"""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Create user pydantic schema"""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Update user pydantic schema"""
    pass
