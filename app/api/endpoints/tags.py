from enum import Enum


class Tag(str, Enum):
    CREATE: str = 'Create'
    COMMON_USERS: str = 'Common users'
    SUPERUSERS: str = 'Superusers'
    REMOVE: str = 'Remove'
    RETRIEVE: str = 'Retrieve'
    UNAUTHORIZED: str = 'Unauthorized'
    UPDATE: str = 'Update'
